"""
Document Store on Google Firestore.
"""

from __future__ import annotations

__all__ = ["GoogleFirestore"]

from typing import Any

from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud import firestore
from google.cloud.firestore import (
    ExistsOption,
    async_transactional,
    transactional,
)
from google.cloud.firestore_v1.base_query import And as AndFilter
from google.cloud.firestore_v1.base_query import BaseFilter, FieldFilter
from google.cloud.firestore_v1.base_query import Or as OrFilter

from verse.core import Context, NCall, Operation, Response
from verse.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    PreconditionFailedError,
)
from verse.internal.storage_core import (
    ItemProcessor,
    ParameterParser,
    QueryProcessor,
    StoreFunctionName,
    StoreOperation,
    StoreOperationParser,
    StoreProvider,
    Validator,
)
from verse.ql import (
    And,
    Comparison,
    ComparisonOp,
    Expression,
    Field,
    Function,
    FunctionNamespace,
    Or,
    OrderBy,
    OrderByDirection,
    Select,
    Update,
    UpdateOp,
    Value,
)

from .._helper import (
    build_item_from_parts,
    build_item_from_value,
    build_query_result,
    get_collection_config,
)
from .._models import DocumentCollectionConfig


class GoogleFirestore(StoreProvider):
    collection: str | None = None
    project: str
    database: str | None
    service_account_info: str | None = None
    service_account_file: str | None = None
    access_token: str | None = None
    id_map_field: str | dict | None
    pk_map_field: str | dict | None
    etag_embed_field: str | dict | None
    suppress_fields: list[str] | None = None
    nparams: dict[str, Any] = dict()

    _credential: Any
    _db_client: Any
    _adb_client: Any
    _collection_cache: dict[str, FirestoreCollection]
    _acollection_cache: dict[str, FirestoreCollection]

    def __init__(
        self,
        project: str,
        database: str | None = "(default)",
        collection: str | None = None,
        service_account_info: str | None = None,
        service_account_file: str | None = None,
        access_token: str | None = None,
        id_map_field: str | dict | None = "id",
        pk_map_field: str | dict | None = "pk",
        etag_embed_field: str | dict | None = "_etag",
        suppress_fields: list[str] | None = None,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            project:
                Google project name.
            database:
                Firestore database name.
            collection:
                Firestore collection name which
                maps to document store collection.
            service_account_info:
                Google service account info with serialized credentials.
            service_account_file:
                Google service account file with credentials.
            access_token:
                Google access token.
            id_map_field:
                Field in the document to map into id.
                To specify for multiple collections, use a dictionary
                where the key is the collection name and the value
                is the field.
            pk_map_field:
                Field in the document to map into pk.
                To specify for multiple collections, use a dictionary
                where the key is the collection name and the value
                is the field.
            etag_embed_field:
                Field to store the generated ETAG value.
                To specify for multiple collections, use a dictionary
                where the key is the collection name and the value
                is the field.
            suppress_fields:
                List of fields to supress when results are returned.
            nparams:
                Native params to Google Firestore client.
        """
        self.project = project
        self.database = database
        self.collection = collection
        self.service_account_info = service_account_info
        self.service_account_file = service_account_file
        self.access_token = access_token
        self.id_map_field = id_map_field
        self.pk_map_field = pk_map_field
        self.etag_embed_field = etag_embed_field
        self.suppress_fields = suppress_fields
        self.nparams = nparams

        self._credential = None
        self._db_client = None
        self._adb_client = None
        self._collection_cache = dict()
        self._acollection_cache = dict()

    def init(self, context: Context | None = None) -> None:
        if self._db_client is not None:
            return

        from google.cloud.firestore import Client

        (
            self._credentials,
            self._db_client,
        ) = self._init_credentials_client(Client)

    async def ainit(self, context: Context | None = None) -> None:
        if self._adb_client is not None:
            return

        from google.cloud.firestore import AsyncClient

        (
            self._credentials,
            self._adb_client,
        ) = self._init_credentials_client(AsyncClient)

    def _init_credentials_client(self, client: Any):

        from verse.internal.storage_common._google import get_credentials

        credentials = get_credentials(
            self.service_account_info,
            self.service_account_file,
            self.access_token,
        )
        args = {
            "project": self.project,
            "database": self.database,
        }
        if credentials is not None:
            args["credentials"] = credentials
        args = args | self.nparams
        firestore_client: Any = client(**args)
        return credentials, firestore_client

    def _get_collection_name(
        self, op_parser: StoreOperationParser
    ) -> str | None:
        collection_name = (
            op_parser.get_operation_parsers()[0].get_collection_name()
            if op_parser.op_equals(StoreOperation.BATCH)
            else op_parser.get_collection_name()
        )
        db_collection = (
            collection_name if collection_name is not None else self.collection
        )
        return db_collection

    def _get_collections(
        self, op_parser: StoreOperationParser
    ) -> list[FirestoreCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[FirestoreCollection] = []
            for single_op_parser in op_parser.get_operation_parsers():
                collections.extend(self._get_collections(single_op_parser))
            return collections
        db_collection = self._get_collection_name(op_parser)
        if db_collection is None:
            raise BadRequestError("Collection name must be specified")
        if db_collection in self._collection_cache:
            return [self._collection_cache[db_collection]]
        client = self._db_client.collection(db_collection)
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, db_collection
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, db_collection
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, db_collection
        )
        col = FirestoreCollection(
            client,
            ClientHelper,
            self._db_client,
            id_map_field,
            pk_map_field,
            etag_embed_field,
            self.suppress_fields,
        )
        self._collection_cache[db_collection] = col
        return [col]

    async def _aget_collections(
        self, op_parser: StoreOperationParser
    ) -> list[FirestoreCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[FirestoreCollection] = []
            for single_op_parser in op_parser.get_operation_parsers():
                collections.extend(
                    await self._aget_collections(single_op_parser)
                )
            return collections
        db_collection = self._get_collection_name(op_parser)
        if db_collection is None:
            raise BadRequestError("Collection name must be specified")
        if db_collection in self._acollection_cache:
            return [self._acollection_cache[db_collection]]
        client = self._adb_client.collection(db_collection)
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, db_collection
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, db_collection
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, db_collection
        )
        col = FirestoreCollection(
            client,
            AsyncClientHelper,
            self._adb_client,
            id_map_field,
            pk_map_field,
            etag_embed_field,
            self.suppress_fields,
        )
        self._acollection_cache[db_collection] = col
        return [col]

    def _validate(self, op_parser: StoreOperationParser):
        if op_parser.op_equals(StoreOperation.BATCH):
            Validator.validate_batch(
                op_parser.get_operation_parsers(),
                allowed_ops=[StoreOperation.PUT, StoreOperation.DELETE],
                single_collection=True,
            )

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        self.init(context=context)
        op_parser = self.get_op_parser(operation)
        self._validate(op_parser)
        collections = self._get_collections(op_parser)
        ncall, state = self._get_ncall(
            op_parser, collections, ResourceHelper(self._db_client)
        )
        if ncall is None:
            return super().run(operation)
        nresult = ncall.invoke()
        result = self._convert_nresult(
            nresult,
            state,
            op_parser,
            collections,
        )
        return Response(result=result, native=dict(result=nresult, call=ncall))

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        await self.ainit(context=context)
        op_parser = self.get_op_parser(operation)
        self._validate(op_parser)
        collections = await self._aget_collections(op_parser)
        ncall, state = self._get_ncall(
            op_parser, collections, AsyncResourceHelper(self._adb_client)
        )
        if ncall is None:
            return await super().arun(operation)
        nresult = await ncall.ainvoke()
        result = self._convert_nresult(
            nresult,
            state,
            op_parser,
            collections,
        )
        return Response(result=result, native=dict(result=nresult, call=ncall))

    def _get_ncall(
        self,
        op_parser: StoreOperationParser,
        collections: list[FirestoreCollection],
        resource_helper: Any,
    ) -> tuple[NCall | None, dict | None]:
        if len(collections) == 1:
            converter = collections[0].converter
            client = collections[0].client
            helper = collections[0].helper
            db_client = collections[0].db_client
        call = None
        state = None
        nargs = op_parser.get_nargs()
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            args: dict = {
                "collection": self._get_collection_name(op_parser),
                "config": get_collection_config(op_parser),
                "exists": op_parser.get_where_exists(),
                "nargs": nargs,
            }
            call = NCall(resource_helper.create_collection, args)
        # DROP COLLECTION
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            args = {
                "collection": self._get_collection_name(op_parser),
                "exists": op_parser.get_where_exists(),
                "nargs": nargs,
            }
            call = NCall(resource_helper.drop_collection, args)
        # LIST COLLECTION
        elif op_parser.op_equals(StoreOperation.LIST_COLLECTIONS):
            args = {"nargs": nargs}
            call = NCall(resource_helper.list_collections, args)
        # GET
        if op_parser.op_equals(StoreOperation.GET):
            args = converter.convert_get(op_parser.get_key())
            call = NCall(
                client.document(args["id"]).get,
                None,
                nargs,
                {None: NotFoundError},
            )
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            args, state, func, id = converter.convert_put(
                op_parser.get_key(),
                op_parser.get_value(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            if func == "set":
                call = NCall(
                    client.document(id).set,
                    args,
                    nargs,
                )
            elif func == "create":
                call = NCall(
                    client.document(id).create,
                    args,
                    nargs,
                    {AlreadyExists: PreconditionFailedError},
                )
            elif func == "helper":
                args["transaction"] = db_client.transaction()
                call = NCall(helper.put, args)
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            (args, state, func, id) = converter.convert_update(
                op_parser.get_key(),
                op_parser.get_set(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
                op_parser.get_returning(),
            )
            if func == "update":
                call = NCall(
                    client.document(id).update,
                    args,
                    nargs,
                    {NotFound: NotFoundError},
                )
            elif func == "helper":
                args["transaction"] = db_client.transaction()
                call = NCall(helper.update, args)
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            args, func, id = converter.convert_delete(
                op_parser.get_key(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            if func == "delete":
                call = NCall(
                    client.document(id).delete,
                    args,
                    nargs,
                    {NotFound: NotFoundError},
                )
            elif func == "helper":
                args["transaction"] = db_client.transaction()
                call = NCall(helper.delete, args)
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            args = converter.convert_query(
                client=client,
                select=op_parser.get_select(),
                where=op_parser.get_where(),
                order_by=op_parser.get_order_by(),
                limit=op_parser.get_limit(),
                offset=op_parser.get_offset(),
            )
            args = {"call": args["query"].stream, "args": None, "nargs": nargs}
            call = NCall(helper.query, args)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            args = converter.convert_count(
                client=client,
                where=op_parser.get_where(),
            )
            call = NCall(args["query"].get, None, nargs)
        # BATCH
        elif op_parser.op_equals(StoreOperation.BATCH):
            args, state = converter.convert_batch(
                op_parser.get_operation_parsers()
            )
            args["bulk_writer"] = db_client.bulk_writer()
            call = NCall(helper.batch, args, None)
        # TRANSACT
        elif op_parser.op_equals(StoreOperation.TRANSACT):
            args, state = OperationConverter.convert_transact(
                op_parser.get_operation_parsers(),
                [col.converter for col in collections],
            )
            args["transaction"] = resource_helper.db_client.transaction()
            call = NCall(resource_helper.transact, args, None)
        # CLOSE
        elif op_parser.op_equals(StoreOperation.CLOSE):
            args = {"nargs": nargs}
            call = NCall(resource_helper.close, args)
        return call, state

    def _convert_nresult(
        self,
        nresult: Any,
        state: dict | None,
        op_parser: StoreOperationParser,
        collections: list[FirestoreCollection],
    ) -> Any:
        if len(collections) == 1:
            processor = collections[0].processor
        result: Any = None
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            result = None
        # DROP COLLECTION
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            result = None
        # LIST COLLECTION
        elif op_parser.op_equals(StoreOperation.LIST_COLLECTIONS):
            result = nresult
        # GET
        if op_parser.op_equals(StoreOperation.GET):
            if nresult is None or nresult.to_dict() is None:
                raise NotFoundError
            result = build_item_from_value(
                processor=processor,
                value=nresult.to_dict(),
                include_value=True,
            )
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            result = build_item_from_value(
                processor=processor,
                value=state["value"] if state is not None else None,
            )
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            if isinstance(nresult, dict):
                result = build_item_from_value(
                    processor=processor, value=nresult, include_value=True
                )
            else:
                key = op_parser.get_key()
                result = build_item_from_parts(
                    processor=processor,
                    key=key,
                    etag=(
                        state["etag"]
                        if state is not None and "etag" in state
                        else None
                    ),
                )
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            result = None
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            items: list = []
            for item in nresult:
                items.append(
                    build_item_from_value(
                        processor=processor,
                        value=item.to_dict(),
                        include_value=True,
                    )
                )
            result = build_query_result(items)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            result = nresult[0][0].value
        # BATCH
        elif op_parser.op_equals(StoreOperation.BATCH):
            result = []
            if state is not None:
                for st in state["values"]:
                    if st is not None:
                        result.append(
                            build_item_from_value(
                                processor=processor,
                                value=st["value"],
                            )
                        )
                    else:
                        result.append(None)
        # TRANSACT
        elif op_parser.op_equals(StoreOperation.TRANSACT):
            result = []
            op_parsers = op_parser.get_operation_parsers()
            for i in range(0, len(op_parsers)):
                if state is not None:
                    st = state["values"][i]
                result.append(
                    self._convert_nresult(
                        nresult[i], st, op_parsers[i], [collections[i]]
                    )
                )
        return result


class OperationConverter:
    processor: ItemProcessor
    client: Any

    def __init__(self, processor: ItemProcessor, client: Any):
        self.processor = processor
        self.client = client

    @staticmethod
    def convert_transact(
        op_parsers: list[StoreOperationParser],
        converters: list[OperationConverter],
    ) -> tuple[dict, dict]:
        ops: list = []
        states: list = []
        for i in range(0, len(op_parsers)):
            op_parser = op_parsers[i]
            converter = converters[i]
            if op_parser.op_equals(StoreOperation.PUT):
                args, state, func, id = converter.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(
                    {
                        "op": StoreOperation.PUT,
                        "id": id,
                        "func": func,
                        "args": args,
                        "client": converter.client,
                        "processor": converter.processor,
                    }
                )
                states.append(state)
            elif op_parser.op_equals(StoreOperation.UPDATE):
                (args, state, func, id) = converter.convert_update(
                    op_parser.get_key(),
                    op_parser.get_set(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                    op_parser.get_returning(),
                )
                ops.append(
                    {
                        "op": StoreOperation.UPDATE,
                        "id": id,
                        "func": func,
                        "args": args,
                        "client": converter.client,
                        "processor": converter.processor,
                    }
                )
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args, func, id = converter.convert_delete(
                    op_parser.get_key(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(
                    {
                        "op": StoreOperation.DELETE,
                        "id": id,
                        "func": func,
                        "args": args,
                        "client": converter.client,
                        "processor": converter.processor,
                    }
                )
                states.append(None)
        return {"ops": ops}, {"values": states}

    def convert_batch(
        self, op_parsers: list[StoreOperationParser]
    ) -> tuple[dict, dict]:
        ops: list = []
        states: list = []
        for op_parser in op_parsers:
            if op_parser.op_equals(StoreOperation.PUT):
                args, state, func, id = self.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(
                    {
                        "op": StoreOperation.PUT,
                        "id": id,
                        "document": args["document_data"],
                    }
                )
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args, func, id = self.convert_delete(
                    op_parser.get_key(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append({"op": StoreOperation.DELETE, "id": id})
                states.append(None)
        return {"ops": ops}, {"values": states}

    def convert_get(self, key: Value) -> dict:
        id = self.processor.get_id_from_key(key)
        return {"id": id}

    def convert_put(
        self,
        key: Value,
        value: dict,
        where: Expression | None,
        exists: bool | None,
    ) -> tuple[dict, dict | None, str, Value]:
        document = self.processor.add_embed_fields(value, key)
        if key is not None:
            id = self.processor.get_id_from_key(key)
        else:
            id = self.processor.get_id_from_value(document)
        if where is None:
            args: dict = {"document_data": document}
            func = "set"
        elif exists is False:
            args = {"document_data": document}
            func = "create"
        elif where is not None:
            args = {
                "id": id,
                "document_data": document,
                "where": where,
            }
            func = "helper"
        return args, {"value": document}, func, id

    def convert_update(
        self,
        key: Value,
        set: Update,
        where: Expression | None,
        exists: bool | None,
        returning: bool | None,
    ) -> tuple[dict, dict | None, str, Value]:
        state = None
        id = self.processor.get_id_from_key(key=key)
        if self.processor.needs_local_etag():
            etag = self.processor.generate_etag()
            set = self.processor.add_etag_update(set, etag)
            state = {"etag": etag}
        field_updates = self.convert_update_ops(set)
        if (where is None or exists is True) and returning is None:
            args: dict = {
                "field_updates": field_updates,
            }
            func = "update"
        elif where is not None or returning is not None:
            args = {
                "id": id,
                "field_updates": field_updates,
                "where": where,
                "update": set,
                "returning": returning,
            }
            func = "helper"
        return args, state, func, id

    def convert_delete(
        self, key: Value, where: Expression | None, exists: bool | None
    ) -> tuple[dict, str, Value]:
        id = self.processor.get_id_from_key(key=key)
        if where is None or exists is True:
            args = {"option": ExistsOption(exists=True)}
            func = "delete"
        else:
            args = {
                "id": id,
                "where": where,
            }
            func = "helper"
        return args, func, id

    def convert_query(
        self,
        client: Any,
        select: Select | None = None,
        where: Expression | None = None,
        order_by: OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict:
        query = client
        if select is not None:
            query = self.convert_select(query, select)
        if where is not None:
            filter = self.convert_where(where)
            query = query.where(filter=filter)
        if order_by is not None:
            query = self.convert_order_by(query, order_by)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return {"query": query}

    def convert_count(
        self, client: Any, where: Expression | None = None
    ) -> dict:
        query = client
        if where is not None:
            filter = self.convert_where(where)
            query = query.where(filter=filter)
        query = query.count()
        return {"query": query}

    def convert_field(self, field: Field | str) -> str:
        path: str
        if isinstance(field, str):
            path = field
        elif isinstance(field, Field):
            path = field.path
        return self.processor.resolve_field(path)

    def convert_where(self, expr: Expression | None) -> BaseFilter:
        if isinstance(expr, Function):
            return self.convert_func(expr)
        if isinstance(expr, Comparison):
            field = None
            field_value = None
            if isinstance(expr.lexpr, Field):
                field = self.convert_field(expr.lexpr)
                field_value = expr.rexpr
            elif isinstance(expr.rexpr, Field):
                field = self.convert_field(expr.rexpr)
                field_value = expr.lexpr
            else:
                raise BadRequestError(f"Comparison {expr} not supported")
            op = expr.op.value
            if expr.op == ComparisonOp.EQ:
                op = "=="
            if expr.op == ComparisonOp.IN:
                op = "in"
            elif expr.op == ComparisonOp.NIN:
                op = "not-in"
            if expr.op == ComparisonOp.BETWEEN and isinstance(
                field_value, list
            ):
                return AndFilter(
                    [
                        FieldFilter(field, ">=", field_value[0]),
                        FieldFilter(field, "<=", field_value[1]),
                    ],
                )
            return FieldFilter(field, op, field_value)
        if isinstance(expr, And):
            return AndFilter(
                [
                    self.convert_where(expr.lexpr),
                    self.convert_where(expr.rexpr),
                ]
            )
        if isinstance(expr, Or):
            return OrFilter(
                [
                    self.convert_where(expr.lexpr),
                    self.convert_where(expr.rexpr),
                ]
            )
        raise BadRequestError(f"Expression {expr!r} not supported")

    def convert_func(self, expr: Function) -> BaseFilter:
        namespace = expr.namespace
        name = expr.name
        args = expr.args
        if namespace == FunctionNamespace.BUILTIN:
            if name == StoreFunctionName.STARTS_WITH:
                field = self.convert_field(args[0])
                value = args[1]
                return AndFilter(
                    [
                        FieldFilter(field, ">=", value),
                        FieldFilter(field, "<=", str(value) + "~"),
                    ],
                )
            if name == StoreFunctionName.ARRAY_CONTAINS:
                field = self.convert_field(args[0])
                value = args[1]
                return FieldFilter(field, "array_contains", value)
            if name == StoreFunctionName.ARRAY_CONTAINS_ANY:
                field = self.convert_field(args[0])
                value = args[1]
                return FieldFilter(field, "array_contains_any", value)
        raise BadRequestError(f"Function {name} not supported")

    def convert_order_by(self, query, order_by: OrderBy):
        for term in order_by.terms:
            args = {"field_path": self.convert_field(term.field)}
            if term.direction is not None:
                if term.direction == OrderByDirection.ASC:
                    args["direction"] = "ASCENDING"
                elif term.direction == OrderByDirection.DESC:
                    args["direction"] = "DESCENDING"
            return query.order_by(**args)

    def convert_select(self, query, select: Select):
        if len(select.terms) == 0:
            return query
        field_paths = []
        for term in select.terms:
            field_path = self.convert_field(term.field)
            field_paths.append(field_path)
        return query.select(field_paths)

    def convert_update_ops(self, update: Update) -> dict:
        field_updates = {}
        for operation in update.operations:
            field = self.processor.resolve_field(operation.field)
            if operation.op == UpdateOp.PUT:
                field_updates[field] = operation.args[0]
            elif operation.op == UpdateOp.INSERT:
                field_updates[field] = operation.args[0]
            elif operation.op == UpdateOp.DELETE:
                field_updates[field] = firestore.DELETE_FIELD
            elif operation.op == UpdateOp.INCREMENT:
                field_updates[field] = firestore.Increment(operation.args[0])
            elif operation.op == UpdateOp.ARRAY_UNION:
                field_updates[field] = firestore.ArrayUnion(operation.args[0])
            elif operation.op == UpdateOp.ARRAY_REMOVE:
                field_updates[field] = firestore.ArrayRemove(operation.args[0])
            else:
                raise BadRequestError("Update operation not supported")
        return field_updates


class ResourceHelper:
    db_client: Any

    def __init__(self, db_client):
        self.db_client = db_client

    def create_collection(
        self,
        collection: str,
        config: DocumentCollectionConfig | None,
        exists: bool | None,
        nargs: Any,
    ):
        pass

    def drop_collection(
        self,
        collection: str,
        exists: bool | None,
        nargs: Any,
    ):
        batch_size = 100
        docs = self.db_client.collection(collection).list_documents(
            page_size=batch_size
        )
        deleted = 0

        for doc in docs:
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self.drop_collection(collection, exists, nargs)

    def list_collections(self, nargs) -> Any:
        nresult = []
        response = NCall(self.db_client.collections, None, nargs).invoke()
        for item in response:
            nresult.append(item.id)
        return nresult

    def transact(self, transaction: Any, ops: list[dict]) -> Any:
        return ResourceHelper.run_transaction(transaction, ops)

    @transactional
    def run_transaction(transaction: Any, ops: list[dict]) -> Any:
        result: list = []
        documents = []
        for op in ops:
            client = op["client"]
            processor = op["processor"]
            if op["func"] == "helper":
                where = op["args"]["where"]
                snapshot = client.document(op["id"]).get(
                    transaction=transaction
                )
                document = snapshot.to_dict()
                if not QueryProcessor.eval_expr(
                    document, where, processor.resolve_field
                ):
                    raise ConflictError
                documents.append(document)
            else:
                documents.append(None)
        try:
            for i in range(0, len(ops)):
                op = ops[i]
                client = op["client"]
                processor = op["processor"]
                ref = client.document(op["id"])
                if op["op"] == StoreOperation.PUT:
                    if op["func"] == "create":
                        transaction.create(
                            reference=ref,
                            document_data=op["args"]["document_data"],
                        )
                    else:
                        transaction.set(
                            reference=ref,
                            document_data=op["args"]["document_data"],
                        )
                    result.append(None)
                elif op["op"] == StoreOperation.UPDATE:
                    transaction.update(
                        reference=ref,
                        field_updates=op["args"]["field_updates"],
                    )
                    if "returning" in op["args"]:
                        returning = op["args"]["returning"]
                        if returning is False:
                            result.append(documents[i])
                        elif returning is True:
                            result.append(
                                QueryProcessor.update_item(
                                    documents[i],
                                    op["args"]["update"],
                                    processor.resolve_field,
                                )
                            )
                        else:
                            result.append(None)
                elif op["op"] == StoreOperation.DELETE:
                    if op["func"] == "delete":
                        transaction.delete(
                            reference=ref, option=ExistsOption(exists=True)
                        )
                    else:
                        transaction.delete(reference=ref)
                    result.append(None)
        except Exception:
            raise ConflictError
        return result

    def close(self, nargs: Any) -> Any:
        pass


class AsyncResourceHelper:
    db_client: Any

    def __init__(self, db_client):
        self.db_client = db_client

    async def create_collection(
        self,
        collection: str,
        config: DocumentCollectionConfig | None,
        exists: bool | None,
        nargs: Any,
    ):
        pass

    async def drop_collection(
        self,
        collection: str,
        exists: bool | None,
        nargs: Any,
    ):
        batch_size = 100
        docs = self.db_client.collection(collection).list_documents(
            page_size=batch_size
        )
        deleted = 0

        async for doc in docs:
            await doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return await self.drop_collection(collection, exists, nargs)

    async def list_collections(self, nargs) -> Any:
        nresult = []
        response = NCall(self.db_client.collections, None, nargs).invoke()
        async for item in response:
            nresult.append(item.id)
        return nresult

    async def transact(self, transaction: Any, ops: list[dict]) -> Any:
        return await AsyncResourceHelper.run_transaction(transaction, ops)

    @async_transactional
    async def run_transaction(transaction: Any, ops: list[dict]) -> Any:
        result: list = []
        documents = []
        for op in ops:
            client = op["client"]
            processor = op["processor"]
            if op["func"] == "helper":
                where = op["args"]["where"]
                snapshot = await client.document(op["id"]).get(
                    transaction=transaction
                )
                document = snapshot.to_dict()
                if not QueryProcessor.eval_expr(
                    document, where, processor.resolve_field
                ):
                    raise ConflictError
                documents.append(document)
            else:
                documents.append(None)
        try:
            for i in range(0, len(ops)):
                op = ops[i]
                client = op["client"]
                processor = op["processor"]
                ref = client.document(op["id"])
                if op["op"] == StoreOperation.PUT:
                    if op["func"] == "create":
                        transaction.create(
                            reference=ref,
                            document_data=op["args"]["document_data"],
                        )
                    else:
                        transaction.set(
                            reference=ref,
                            document_data=op["args"]["document_data"],
                        )
                    result.append(None)
                elif op["op"] == StoreOperation.UPDATE:
                    transaction.update(
                        reference=ref,
                        field_updates=op["args"]["field_updates"],
                    )
                    if "returning" in op["args"]:
                        returning = op["args"]["returning"]
                        if returning is False:
                            result.append(documents[i])
                        elif returning is True:
                            result.append(
                                QueryProcessor.update_item(
                                    documents[i],
                                    op["args"]["update"],
                                    processor.resolve_field,
                                )
                            )
                        else:
                            result.append(None)
                elif op["op"] == StoreOperation.DELETE:
                    if op["func"] == "delete":
                        transaction.delete(
                            reference=ref, option=ExistsOption(exists=True)
                        )
                    else:
                        transaction.delete(reference=ref)
                    result.append(None)
        except Exception:
            raise ConflictError
        return result

    async def close(self, nargs: Any) -> Any:
        pass


class ClientHelper:
    client: Any
    processor: ItemProcessor

    def __init__(self, client: Any, processor: ItemProcessor):
        self.client = client
        self.processor = processor

    def put(self, transaction, id, document_data, where) -> dict:
        doc_ref = self.client.document(id)
        result, doc = ClientHelper.run_conditional_op_in_transaction(
            transaction,
            transaction.set,
            {"reference": doc_ref, "document_data": document_data},
            where,
            doc_ref,
            self.processor.resolve_field,
            True,
        )
        if result is None:
            if where is None:
                raise NotFoundError
            else:
                raise PreconditionFailedError
        if result is False:
            raise PreconditionFailedError
        return document_data

    def update(
        self,
        transaction,
        id,
        field_updates,
        where,
        update: Update,
        returning: bool | None,
    ) -> dict | None:
        doc_ref = self.client.document(id)
        result, doc = ClientHelper.run_conditional_op_in_transaction(
            transaction,
            transaction.update,
            {"reference": doc_ref, "field_updates": field_updates},
            where,
            doc_ref,
            self.processor.resolve_field,
            returning is None,
        )
        if result is None:
            if where is None:
                raise NotFoundError
            else:
                raise PreconditionFailedError
        if result is False:
            raise PreconditionFailedError
        if returning is None:
            return None
        if returning is False:
            return doc
        return QueryProcessor.update_item(
            doc, update, self.processor.resolve_field
        )

    def delete(self, transaction, id, where) -> None:
        doc_ref = self.client.document(id)
        result, doc = ClientHelper.run_conditional_op_in_transaction(
            transaction,
            transaction.delete,
            {"reference": doc_ref},
            where,
            doc_ref,
            self.processor.resolve_field,
            True,
        )
        if result is None:
            if where is None:
                raise NotFoundError
            else:
                raise PreconditionFailedError
        if result is False:
            raise PreconditionFailedError
        return None

    def query(self, call, args, nargs) -> Any:
        nresult = NCall(call, args, nargs).invoke()
        return nresult

    def batch(self, bulk_writer: Any, ops: list[dict]) -> Any:
        for op in ops:
            if op["op"] == StoreOperation.PUT:
                bulk_writer.set(self.client.document(op["id"]), op["document"])
            elif op["op"] == StoreOperation.DELETE:
                bulk_writer.delete(self.client.document(op["id"]))
        bulk_writer.close()

    def close(self, nargs: Any) -> Any:
        pass

    @transactional
    def run_conditional_op_in_transaction(
        transaction,
        op,
        args,
        where,
        doc_ref,
        special_field_resolver,
        project_get,
    ) -> tuple:
        if project_get:
            fields = QueryProcessor.extract_filter_fields(
                where, special_field_resolver
            )
            snapshot = doc_ref.get(field_paths=fields, transaction=transaction)
        else:
            snapshot = doc_ref.get(transaction=transaction)
        document = snapshot.to_dict()
        try:
            condition_result = QueryProcessor.eval_expr(
                document, where, special_field_resolver
            )
        except Exception:
            if document is None:
                return None, None
            raise
        if condition_result:
            op(**args)
            return True, document
        if document is None:
            return None, None
        return False, document


class AsyncClientHelper:
    client: Any
    processor: ItemProcessor

    def __init__(self, client: Any, processor: ItemProcessor):
        self.client = client
        self.processor = processor

    async def put(self, transaction, id, document_data, where) -> dict:
        doc_ref = self.client.document(id)
        (
            result,
            doc,
        ) = await AsyncClientHelper.run_conditional_op_in_transaction(
            transaction,
            transaction.set,
            {"reference": doc_ref, "document_data": document_data},
            where,
            doc_ref,
            self.processor.resolve_field,
            True,
        )
        if result is None:
            if where is None:
                raise NotFoundError
            else:
                raise PreconditionFailedError
        if result is False:
            raise PreconditionFailedError
        return document_data

    async def update(
        self,
        transaction,
        id,
        field_updates,
        where,
        update: Update,
        returning: bool | None,
    ) -> dict | None:
        doc_ref = self.client.document(id)
        (
            result,
            doc,
        ) = await AsyncClientHelper.run_conditional_op_in_transaction(
            transaction,
            transaction.update,
            {"reference": doc_ref, "field_updates": field_updates},
            where,
            doc_ref,
            self.processor.resolve_field,
            returning is None,
        )
        if result is None:
            if where is None:
                raise NotFoundError
            else:
                raise PreconditionFailedError
        if result is False:
            raise PreconditionFailedError
        if returning is None:
            return None
        if returning is False:
            return doc
        return QueryProcessor.update_item(
            doc, update, self.processor.resolve_field
        )

    async def delete(self, transaction, id, where) -> None:
        doc_ref = self.client.document(id)
        (
            result,
            doc,
        ) = await AsyncClientHelper.run_conditional_op_in_transaction(
            transaction,
            transaction.delete,
            {"reference": doc_ref},
            where,
            doc_ref,
            self.processor.resolve_field,
            True,
        )
        if result is None:
            if where is None:
                raise NotFoundError
            else:
                raise PreconditionFailedError
        if result is False:
            raise PreconditionFailedError
        return None

    async def query(self, call, args, nargs) -> Any:
        response = NCall(call, args, nargs).invoke()
        nresult = []
        async for item in response:
            nresult.append(item)
        return nresult

    async def batch(self, bulk_writer: Any, ops: list[dict]) -> Any:
        for op in ops:
            if op["op"] == StoreOperation.PUT:
                bulk_writer.set(self.client.document(op["id"]), op["document"])
            elif op["op"] == StoreOperation.DELETE:
                bulk_writer.delete(self.client.document(op["id"]))
        bulk_writer.close()

    async def close(self, nargs: Any) -> Any:
        pass

    @async_transactional
    async def run_conditional_op_in_transaction(
        transaction,
        op,
        args,
        where,
        doc_ref,
        special_field_resolver,
        project_get,
    ) -> tuple:
        if project_get:
            fields = QueryProcessor.extract_filter_fields(
                where, special_field_resolver
            )
            snapshot = await doc_ref.get(
                field_paths=fields, transaction=transaction
            )
        else:
            snapshot = await doc_ref.get(transaction=transaction)
        document = snapshot.to_dict()
        try:
            condition_result = QueryProcessor.eval_expr(
                document, where, special_field_resolver
            )
        except Exception:
            if document is None:
                return None, None
            raise
        if condition_result:
            op(**args)
            return True, document
        if document is None:
            return None, None
        return False, document


class FirestoreCollection:
    client: Any
    helper: Any
    db_client: Any
    converter: OperationConverter
    processor: ItemProcessor

    def __init__(
        self,
        client: Any,
        helper_type: Any,
        db_client: Any,
        id_map_field: str | None,
        pk_map_field: str | None,
        etag_embed_field: str | None,
        suppress_fields: list[str] | None,
    ) -> None:
        self.client = client
        self.processor = ItemProcessor(
            etag_embed_field=etag_embed_field,
            id_map_field=id_map_field,
            pk_map_field=pk_map_field,
            local_etag=True,
            suppress_fields=suppress_fields,
        )
        self.converter = OperationConverter(self.processor, client)
        self.helper = helper_type(client, self.processor)
        self.db_client = db_client
