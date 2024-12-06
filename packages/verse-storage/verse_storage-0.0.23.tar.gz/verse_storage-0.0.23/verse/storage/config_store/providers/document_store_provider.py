"""
Config Store on top of Document Store.
"""

from __future__ import annotations

__all__ = ["DocumentStoreProvider"]

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from verse.core import Component, Context, Operation, Response
from verse.internal.storage_core import (
    ItemProcessor,
    StoreFunction,
    StoreOperation,
    StoreOperationParser,
    StoreProvider,
)
from verse.ql import And, Comparison, ComparisonOp, Expression, Field

from .._helper import QueryArgs, get_query_args, normalize_label
from .._models import ConfigItem, ConfigKey, ConfigList, ConfigProperties


@dataclass
class ConfigDocument:
    id: str
    pk: str
    tenant_id: str
    config_id: str
    label: str
    value: str
    metadata: dict | None
    updated_time: int

    def to_dict(self):
        return self.__dict__


class DocumentStoreProvider(StoreProvider):
    store: Component
    tenant_id: str

    _init: bool
    _ainit: bool
    _processor: ItemProcessor
    _converter: OperationConverter

    def __init__(
        self,
        store: Component,
        tenant_id: str = "default",
        **kwargs,
    ):
        """Initialize.

        Args:
            store:
                Document Store component.
            tenant_id:
                Tenant id for multi-tenancy, defaults to "default".
        """
        self.store = store
        self.tenant_id = tenant_id

        self._init = False
        self._ainit = False
        self._client = None
        self._aclient = None
        self._processor = ItemProcessor()
        self._converter = OperationConverter(self.tenant_id)

    def init(self, context: Context | None = None) -> None:
        if self._init:
            return
        self.store.init(context=context)
        self._init = True

    async def ainit(self, context: Context | None = None) -> None:
        if self._ainit:
            return
        await self.store.ainit(context=context)
        self._ainit = True

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        self.init(context=context)
        op_parser = self.get_op_parser(operation)
        ncall = self._get_operation(op_parser, self._converter)
        if ncall is None:
            return super().run(operation)
        nresult = self.store.run(operation=ncall, context=context)
        result = self._convert_nresult(nresult, op_parser, self._processor)
        return Response(result=result, native=dict(result=nresult, call=ncall))

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        await self.ainit(context=context)
        op_parser = self.get_op_parser(operation)
        ncall = self._get_operation(op_parser, self._converter)
        if ncall is None:
            return await super().arun(operation)
        nresult = await self.store.arun(operation=ncall, context=context)
        result = self._convert_nresult(nresult, op_parser, self._processor)
        return Response(result=result, native=dict(result=nresult, call=ncall))

    def _get_operation(
        self, op_parser: StoreOperationParser, converter: OperationConverter
    ):
        # GET
        if op_parser.op_equals(StoreOperation.GET):
            id = op_parser.get_id_as_str()
            label = normalize_label(op_parser.get_label())
            return StoreOperation.get(key=converter.convert_key(id, label))
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            id = op_parser.get_id_as_str()
            value = op_parser.get_value()
            label = normalize_label(op_parser.get_label())
            metadata = op_parser.get_metadata()
            return StoreOperation.put(
                value=ConfigDocument(
                    id=converter.convert_id(id, label),
                    pk=converter.convert_pk(),
                    tenant_id=self.tenant_id,
                    config_id=id,
                    label=label,
                    value=value,
                    metadata=metadata,
                    updated_time=int(time.time()),
                ).to_dict()
            )
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            id = op_parser.get_id_as_str()
            label = normalize_label(op_parser.get_label())
            return StoreOperation.delete(key=converter.convert_key(id, label))
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            where = converter.convert_filter(get_query_args(op_parser))
            return StoreOperation.query(where=where)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            where = converter.convert_filter(get_query_args(op_parser))
            return StoreOperation.count(where=where)
        # CLOSE
        elif op_parser.op_equals(StoreOperation.CLOSE):
            return StoreOperation.close()
        else:
            return None

    def _convert_nresult(
        self,
        nresult: Any,
        op_parser: StoreOperationParser,
        processor: ItemProcessor,
    ) -> Any:
        result: Any = None
        nresult = nresult.result

        def convert_item(item):
            return ConfigItem(
                key=ConfigKey(
                    id=item.value["config_id"], label=item.value["label"]
                ),
                value=item.value["value"],
                metadata=item.value["metadata"],
                properties=ConfigProperties(
                    updated_time=Helper.convert_to_datetime(
                        item.value["updated_time"]
                    )
                ),
            )

        # GET
        if op_parser.op_equals(StoreOperation.GET):
            result = convert_item(nresult)
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            result = ConfigItem(
                key=ConfigKey(
                    id=op_parser.get_id_as_str(),
                    label=normalize_label(op_parser.get_label()),
                ),
                value=op_parser.get_value(),
            )
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            result = None
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            items = []
            for item in nresult.items:
                items.append(convert_item(item))
            items = sorted(items, key=lambda x: (x.key.label, x.key.id))
            result = ConfigList(items=items)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            result = nresult
        return result


class Helper:
    @staticmethod
    def convert_to_datetime(timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp).astimezone()


class OperationConverter:
    tenant_id: str

    def __init__(self, tenant_id: str, **kwargs: Any):
        self.tenant_id = tenant_id

    def convert_id(self, id: str, label: str):
        return f"{self.tenant_id}:{id.replace('/', '$')}:{label}"

    def convert_pk(self):
        return self.tenant_id

    def convert_key(self, id: str, label: str):
        key = dict()
        key["$id"] = self.convert_id(id, label)
        key["$pk"] = self.convert_pk()
        return key

    def convert_filter(self, query_args: QueryArgs) -> Expression:
        where: Expression = Comparison(
            lexpr=Field(path="$pk"),
            op=ComparisonOp.EQ,
            rexpr=self.tenant_id,
        )
        if query_args.id_filter:
            where = And(
                lexpr=StoreFunction.starts_with(
                    "config_id",
                    query_args.id_filter,
                ),
                rexpr=where,
            )
        if query_args.label_filter is not None:
            where = And(
                lexpr=Comparison(
                    lexpr=Field(path="label"),
                    op=ComparisonOp.EQ,
                    rexpr=query_args.label_filter,
                ),
                rexpr=where,
            )
        return where
