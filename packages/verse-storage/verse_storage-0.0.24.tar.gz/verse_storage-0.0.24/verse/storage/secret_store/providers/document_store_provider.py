"""
Secret Store on top of Document Store.
"""

from __future__ import annotations

__all__ = ["DocumentStoreProvider"]


import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from verse.core import Component, Context, NCall, Operation, Response
from verse.core.exceptions import (
    BadRequestError,
    NotFoundError,
    PreconditionFailedError,
)
from verse.internal.storage_core import (
    ItemProcessor,
    QueryProcessor,
    StoreFunction,
    StoreOperation,
    StoreOperationParser,
    StoreProvider,
)
from verse.ql import (
    And,
    Comparison,
    ComparisonOp,
    Field,
    OrderBy,
    OrderByTerm,
    Update,
)

from .._models import (
    SecretItem,
    SecretKey,
    SecretList,
    SecretProperties,
    SecretVersion,
)

SECRET = "secret"
VERSION = "version"


@dataclass
class SecretDocument:
    id: str
    pk: str
    tenant_id: str
    secret_id: str
    version: str
    metadata: dict | None
    value: str
    created_time: int
    type: str = SECRET

    def to_dict(self):
        return self.__dict__


@dataclass
class VersionDocument:
    id: str
    pk: str
    tenant_id: str
    secret_id: str
    version: str
    value: str
    created_time: int
    type: str = VERSION

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
        ncall, state = self._get_operation(
            op_parser,
            self._converter,
            ClientHelper(self.store, self._converter),
        )
        if ncall is None:
            return super().run(operation)
        if isinstance(ncall, NCall):
            operation = ncall.invoke()
        else:
            operation = ncall
        nresult = self.store.run(operation=operation, context=context)
        result = self._convert_nresult(
            nresult, state, op_parser, self._processor
        )
        return Response(result=result, native=dict(result=nresult, call=ncall))

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        await self.ainit(context=context)
        op_parser = self.get_op_parser(operation)
        ncall, state = self._get_operation(
            op_parser,
            self._converter,
            AsyncClientHelper(self.store, self._converter),
        )
        if ncall is None:
            return await super().arun(operation)
        if isinstance(ncall, NCall):
            operation = await ncall.ainvoke()
        else:
            operation = ncall
        nresult = await self.store.arun(operation=operation, context=context)
        result = self._convert_nresult(
            nresult, state, op_parser, self._processor
        )
        return Response(result=result, native=dict(result=nresult, call=ncall))

    def _get_operation(
        self,
        op_parser: StoreOperationParser,
        converter: OperationConverter,
        helper: Any,
    ) -> tuple[Operation | NCall | None, dict | None]:
        operation: NCall | Operation | None = None
        state: dict | None = None
        # GET value
        if (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_value_attribute()
        ):
            id = op_parser.get_id_as_str()
            version = op_parser.get_version()
            operation = converter.convert_get(id, version)
        # GET metadata
        elif (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_metadata_attribute()
        ):
            id = op_parser.get_id_as_str()
            operation = converter.convert_get_metadata(id)
        # GET versions
        elif (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_versions_attribute()
        ):
            id = op_parser.get_id_as_str()
            operation = converter.convert_get_versions(id)
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            id = op_parser.get_id_as_str()
            value = op_parser.get_value()
            metadata: dict | None = op_parser.get_metadata()
            metadata = {} if metadata is None else metadata
            exists = op_parser.get_where_exists()
            version = str(uuid.uuid4())
            created_time = int(time.time())
            args: dict[str, Any] = {
                "id": id,
                "value": value,
                "metadata": metadata,
                "exists": exists,
                "version": version,
                "created_time": created_time,
            }
            operation = NCall(helper.put, args)
            state = {"version": version}
        # UPDATE value
        elif (
            op_parser.op_equals(StoreOperation.UPDATE)
            and op_parser.is_value_update()
        ):
            id = op_parser.get_id_as_str()
            value = op_parser.get_updated_value()
            version = str(uuid.uuid4())
            created_time = int(time.time())
            args = {
                "id": id,
                "value": value,
                "version": version,
                "created_time": created_time,
            }
            operation = NCall(helper.update_value, args)
            state = {"version": version}
        # UPDATE metadata
        elif (
            op_parser.op_equals(StoreOperation.UPDATE)
            and op_parser.is_metadata_update()
        ):
            id = op_parser.get_id_as_str()
            metadata = op_parser.get_updated_metadata()
            metadata = {} if metadata is None else metadata
            operation = converter.convert_update_metadata(id, metadata)
            state = {"metadata": metadata}
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            id = op_parser.get_id_as_str()
            args = {"id": id}
            operation = NCall(helper.delete, args)
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            operation = converter.convert_query()
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            operation = converter.convert_query()
        # CLOSE
        elif op_parser.op_equals(StoreOperation.CLOSE):
            operation = StoreOperation.close()
        return operation, state

    def _convert_nresult(
        self,
        nresult: Any,
        state: dict | None,
        op_parser: StoreOperationParser,
        processor: ItemProcessor,
    ) -> Any:
        result: Any = None
        nresult = nresult.result
        # GET value
        if (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_value_attribute()
        ):
            result = SecretItem(
                key=SecretKey(
                    id=nresult.value["secret_id"],
                    version=nresult.value["version"],
                ),
                value=nresult.value["value"],
            )
        # GET metadata
        elif (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_metadata_attribute()
        ):
            result = SecretItem(
                key=SecretKey(id=nresult.value["secret_id"]),
                metadata=nresult.value["metadata"],
                properties=SecretProperties(
                    created_time=Helper.convert_to_datetime(
                        nresult.value["created_time"]
                    )
                ),
            )
        # GET versions
        elif (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_versions_attribute()
        ):
            versions: list = []
            for item in nresult.items:
                id = item.value["secret_id"]
                versions.append(
                    SecretVersion(
                        version=item.value["version"],
                        created_time=Helper.convert_to_datetime(
                            item.value["created_time"]
                        ),
                    )
                )
            if len(versions) == 0:
                raise NotFoundError
            versions = sorted(
                versions,
                key=lambda s: s.created_time,
                reverse=True,
            )
            return SecretItem(key=SecretKey(id=id), versions=versions)
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            result = SecretItem(
                key=SecretKey(
                    id=op_parser.get_id_as_str(),
                    version=state["version"] if state is not None else None,
                )
            )
        # UPDATE value
        elif (
            op_parser.op_equals(StoreOperation.UPDATE)
            and op_parser.is_value_update()
        ):
            result = SecretItem(
                key=SecretKey(
                    id=op_parser.get_id_as_str(),
                    version=state["version"] if state is not None else None,
                )
            )
        # UPDATE metadata
        elif (
            op_parser.op_equals(StoreOperation.UPDATE)
            and op_parser.is_metadata_update()
        ):
            result = SecretItem(
                key=SecretKey(id=op_parser.get_id_as_str()),
                metadata=state["metadata"] if state is not None else None,
            )
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            result = None
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            items = []
            for item in nresult.items:
                items.append(
                    SecretItem(
                        key=SecretKey(id=item.value["secret_id"]),
                        metadata=item.value["metadata"],
                        properties=SecretProperties(
                            created_time=Helper.convert_to_datetime(
                                item.value["created_time"]
                            )
                        ),
                    )
                )
            order_by = (
                op_parser.get_order_by()
                if op_parser.get_order_by() is not None
                else OrderBy(terms=[OrderByTerm(field="$id")])
            )
            items = QueryProcessor.query_items(
                items=items,
                select=op_parser.get_select(),
                where=op_parser.get_where(),
                order_by=order_by,
                limit=op_parser.get_limit(),
                offset=op_parser.get_offset(),
                field_resolver=processor.resolve_root_field,
            )
            result = SecretList(items=items)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            items = []
            for item in nresult.items:
                items.append(
                    SecretItem(
                        key=SecretKey(id=item.value["secret_id"]),
                        metadata=item.value["metadata"],
                        properties=SecretProperties(
                            created_time=Helper.convert_to_datetime(
                                item.value["created_time"]
                            )
                        ),
                    )
                )
            result = QueryProcessor.count_items(
                items=items,
                where=op_parser.get_where(),
                field_resolver=processor.resolve_root_field,
            )
        return result


class Helper:
    @staticmethod
    def convert_to_datetime(timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp).astimezone()


class ClientHelper:
    store: Component
    converter: OperationConverter

    def __init__(
        self,
        store: Component,
        converter: OperationConverter,
    ):
        self.store = store
        self.converter = converter

    def put(
        self,
        id: str,
        value: str,
        metadata: dict | None,
        exists: bool | None,
        version: str,
        created_time: int,
    ) -> Operation:
        get_result = None
        try:
            get_response = self.store.run(
                StoreOperation.get(key=self.converter.convert_item_key(id))
            )
            get_result = get_response.result
            if exists is False:
                raise PreconditionFailedError
        except NotFoundError:
            pass
        if exists is True and get_result is None:
            raise PreconditionFailedError

        return self.converter.convert_put(
            id, value, version, metadata, created_time, get_result
        )

    def update_value(
        self,
        id: str,
        value: str,
        version: str,
        created_time: int,
    ) -> Operation:
        get_response = self.store.run(
            StoreOperation.get(key=self.converter.convert_item_key(id))
        )
        get_result = get_response.result
        return self.converter.convert_update_value(
            id, value, version, created_time, get_result
        )

    def delete(self, id: str) -> Operation:
        response = self.store.run(self.converter.convert_query_secret(id))
        if response is not None and response.result is not None:
            if len(response.result.items) == 0:
                raise NotFoundError
            return self.converter.convert_delete(response.result.items)
        raise BadRequestError("Unexcepted response")


class AsyncClientHelper:
    store: Component
    converter: OperationConverter

    def __init__(
        self,
        store: Component,
        converter: OperationConverter,
    ):
        self.store = store
        self.converter = converter

    async def put(
        self,
        id: str,
        value: str,
        metadata: dict | None,
        exists: bool | None,
        version: str,
        created_time: int,
    ) -> Operation:
        get_result = None
        try:
            get_response = await self.store.arun(
                StoreOperation.get(key=self.converter.convert_item_key(id))
            )
            get_result = get_response.result
            if exists is False:
                raise PreconditionFailedError
        except NotFoundError:
            pass
        if exists is True and get_result is None:
            raise PreconditionFailedError

        return self.converter.convert_put(
            id, value, version, metadata, created_time, get_result
        )

    async def update_value(
        self,
        id: str,
        value: str,
        version: str,
        created_time: int,
    ) -> Operation:
        get_response = await self.store.arun(
            StoreOperation.get(key=self.converter.convert_item_key(id))
        )
        get_result = get_response.result
        return self.converter.convert_update_value(
            id, value, version, created_time, get_result
        )

    async def delete(self, id: str) -> Operation:
        response = await self.store.arun(
            self.converter.convert_query_secret(id)
        )
        if response is not None and response.result is not None:
            if len(response.result.items) == 0:
                raise NotFoundError
            return self.converter.convert_delete(response.result.items)
        raise BadRequestError("Unexcepted response")


class OperationConverter:
    tenant_id: str

    def __init__(self, tenant_id: str, **kwargs: Any):
        self.tenant_id = tenant_id

    def convert_secret_id(self, id: str):
        return f"{SECRET}-{self.tenant_id}-{id}"

    def convert_version_id(self, id: str, version: str | None = None):
        vid = f"{VERSION}-{self.tenant_id}-{id}"
        if version is not None:
            vid = f"{vid}-{version}"
        return vid

    def convert_pk(self):
        return self.tenant_id

    def convert_item_key(self, id: str):
        key = dict()
        key["$id"] = self.convert_secret_id(id)
        key["$pk"] = self.convert_pk()
        return key

    def convert_version_key(self, id: str, version: str | None = None):
        key = dict()
        key["$id"] = self.convert_version_id(id, version)
        key["$pk"] = self.convert_pk()
        return key

    def convert_query(self) -> Operation:
        return StoreOperation.query(
            where=And(
                lexpr=Comparison(
                    lexpr=Field(path="$pk"),
                    op=ComparisonOp.EQ,
                    rexpr=self.tenant_id,
                ),
                rexpr=Comparison(
                    lexpr=Field(path="type"),
                    op=ComparisonOp.EQ,
                    rexpr=SECRET,
                ),
            )
        )

    def convert_query_secret(self, id: str) -> Operation:
        return StoreOperation.query(
            where=And(
                lexpr=Comparison(
                    lexpr=Field(path="$pk"),
                    op=ComparisonOp.EQ,
                    rexpr=self.tenant_id,
                ),
                rexpr=Comparison(
                    lexpr=Field(path="secret_id"),
                    op=ComparisonOp.EQ,
                    rexpr=id,
                ),
            )
        )

    def convert_get(self, id: str, version: str | None) -> Operation:
        if version is None:
            return StoreOperation.get(key=self.convert_item_key(id))
        else:
            return StoreOperation.get(
                key=self.convert_version_key(id, version)
            )

    def convert_get_metadata(self, id: str) -> Operation:
        return StoreOperation.get(key=self.convert_item_key(id))

    def convert_get_versions(self, id: str) -> Operation:
        return StoreOperation.query(
            where=And(
                lexpr=And(
                    lexpr=Comparison(
                        lexpr=Field(path="$pk"),
                        op=ComparisonOp.EQ,
                        rexpr=self.tenant_id,
                    ),
                    rexpr=Comparison(
                        lexpr=Field(path="type"),
                        op=ComparisonOp.EQ,
                        rexpr=VERSION,
                    ),
                ),
                rexpr=Comparison(
                    lexpr=Field(path="secret_id"),
                    op=ComparisonOp.EQ,
                    rexpr=id,
                ),
            )
        )

    def convert_put(
        self,
        id: str,
        value: str,
        version: str,
        metadata: dict | None,
        created_time: int,
        get_result: Any,
    ) -> Operation:
        operations = []
        if get_result is not None:
            if get_result.properties.etag is not None:
                where = Comparison(
                    lexpr=Field(path="$etag"),
                    op=ComparisonOp.EQ,
                    rexpr=get_result.properties.etag,
                )
            else:
                where = Comparison(
                    lexpr=Field(path="version"),
                    op=ComparisonOp.EQ,
                    rexpr=get_result.value["version"],
                )
            update = Update()
            update.put("metadata", metadata)
            update.put("version", version)
            update.put("value", value)
            operations.append(
                StoreOperation.update(
                    key=self.convert_item_key(id), set=update, where=where
                )
            )
        else:
            operations.append(
                StoreOperation.put(
                    value=SecretDocument(
                        id=self.convert_secret_id(id),
                        pk=self.convert_pk(),
                        tenant_id=self.tenant_id,
                        secret_id=id,
                        version=version,
                        metadata=metadata,
                        value=value,
                        created_time=created_time,
                    ).to_dict(),
                    where=StoreFunction.not_exists(),
                )
            )
        operations.append(
            StoreOperation.put(
                value=VersionDocument(
                    id=self.convert_version_id(id, version),
                    pk=self.convert_pk(),
                    tenant_id=self.tenant_id,
                    secret_id=id,
                    version=version,
                    value=value,
                    created_time=created_time,
                ).to_dict()
            )
        )
        return StoreOperation.transact(operations)

    def convert_update_value(
        self,
        id: str,
        value: str,
        version: str,
        created_time: int,
        get_result: Any,
    ) -> Operation:
        operations = []
        if get_result.properties.etag is not None:
            where = Comparison(
                lexpr=Field(path="$etag"),
                op=ComparisonOp.EQ,
                rexpr=get_result.properties.etag,
            )
        else:
            where = Comparison(
                lexpr=Field(path="version"),
                op=ComparisonOp.EQ,
                rexpr=get_result.value["version"],
            )
        update = Update()
        update.put("version", version)
        update.put("value", value)
        operations.append(
            StoreOperation.update(
                key=self.convert_item_key(id), set=update, where=where
            )
        )
        operations.append(
            StoreOperation.put(
                value=VersionDocument(
                    id=self.convert_version_id(id, version),
                    pk=self.convert_pk(),
                    tenant_id=self.tenant_id,
                    secret_id=id,
                    version=version,
                    value=value,
                    created_time=created_time,
                ).to_dict()
            )
        )
        return StoreOperation.transact(operations)

    def convert_update_metadata(
        self, id: str, metadata: dict | None
    ) -> Operation:
        update = Update()
        update.put("metadata", metadata)
        return StoreOperation.update(key=self.convert_item_key(id), set=update)

    def convert_delete(self, items: list[Any]):
        operations = []
        for item in items:
            if item.value["type"] == SECRET:
                if item.properties.etag is not None:
                    where = Comparison(
                        lexpr=Field(path="$etag"),
                        op=ComparisonOp.EQ,
                        rexpr=item.properties.etag,
                    )
                else:
                    where = Comparison(
                        lexpr=Field(path="version"),
                        op=ComparisonOp.EQ,
                        rexpr=item.value["version"],
                    )
                operations.append(
                    StoreOperation.delete(key=item.key, where=where)
                )
            else:
                operations.append(StoreOperation.delete(key=item.key))
        return StoreOperation.transact(operations)
