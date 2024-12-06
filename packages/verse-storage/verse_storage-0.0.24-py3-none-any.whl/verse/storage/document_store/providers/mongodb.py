"""
Document Store on MongoDB.
"""

from __future__ import annotations

__all__ = ["MongoDB"]

import re
from typing import Any

from pymongo import DeleteOne, ReplaceOne
from pymongo.errors import CollectionInvalid, DuplicateKeyError

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
    Not,
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
from .._models import DocumentCollectionConfig, DocumentFieldType


class MongoDB(StoreProvider):
    collection: str | None
    uri: str
    database: str
    id_map_field: str | dict | None
    pk_map_field: str | dict | None
    etag_embed_field: str | dict | None
    suppress_fields: list[str] | None
    nparams: dict[str, Any]

    _mongo_client: Any
    _amongo_client: Any
    _database_client: Any
    _adatabase_client: Any
    _collection_cache: dict[str, MongoDBCollection]
    _acollection_cache: dict[str, MongoDBCollection]

    def __init__(
        self,
        uri: str,
        database: str,
        collection: str | None = None,
        id_map_field: str | dict | None = "id",
        pk_map_field: str | dict | None = "pk",
        etag_embed_field: str | dict | None = "_etag",
        suppress_fields: list[str] | None = None,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            uri:
                URI to MongoDB instance which embeds the credentials.
            database:
                MongoDB database name.
            collection:
                MongoDB collection name mapped to document store collection.
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
                Native parameters to pymongo client.
        """
        self.uri = uri
        self.database = database
        self.collection = collection
        self.id_map_field = id_map_field
        self.pk_map_field = pk_map_field
        self.etag_embed_field = etag_embed_field
        self.suppress_fields = suppress_fields
        self.nparams = nparams

        self._mongo_client = None
        self._amongo_client = None
        self._database_client = None
        self._adatabase_client = None
        self._collection_cache = dict()
        self._acollection_cache = dict()

    def init(self, context: Context | None = None) -> None:
        if self._mongo_client is not None:
            return

        from pymongo import MongoClient
        from pymongo.server_api import ServerApi

        self._mongo_client = MongoClient(
            self.uri,
            server_api=ServerApi("1"),
            **self.nparams,
        )
        self._database_client = self._mongo_client[self.database]

    async def ainit(self, context: Context | None = None) -> None:
        if self._amongo_client is not None:
            return

        import motor.motor_asyncio

        self._amongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            self.uri,
            **self.nparams,
        )
        self._adatabase_client = self._amongo_client[self.database]

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
    ) -> list[MongoDBCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[MongoDBCollection] = []
            for single_op_parser in op_parser.get_operation_parsers():
                collections.extend(self._get_collections(single_op_parser))
            return collections
        db_collection = self._get_collection_name(op_parser)
        if db_collection is None:
            raise BadRequestError("Collection name must be specified")
        if db_collection in self._collection_cache:
            return [self._collection_cache[db_collection]]
        self._database_client = self._mongo_client[self.database]
        client = self._database_client[db_collection]
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, db_collection
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, db_collection
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, db_collection
        )
        col = MongoDBCollection(
            client,
            ClientHelper,
            id_map_field,
            pk_map_field,
            etag_embed_field,
            self.suppress_fields,
        )
        self._collection_cache[db_collection] = col
        return [col]

    async def _aget_collections(
        self, op_parser: StoreOperationParser
    ) -> list[MongoDBCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[MongoDBCollection] = []
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
        self._adatabase_client = self._amongo_client[self.database]
        client = self._adatabase_client[db_collection]
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, db_collection
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, db_collection
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, db_collection
        )
        col = MongoDBCollection(
            client,
            AsyncClientHelper,
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
            op_parser,
            collections,
            ResourceHelper(self._mongo_client, self._database_client),
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
        op_parser = StoreOperationParser(operation)
        self._validate(op_parser)
        collections = await self._aget_collections(op_parser)
        ncall, state = self._get_ncall(
            op_parser,
            collections,
            AsyncResourceHelper(self._amongo_client, self._adatabase_client),
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
        collections: list[MongoDBCollection],
        resource_helper: Any,
    ) -> tuple[NCall | None, dict | None]:
        if len(collections) == 1:
            converter = collections[0].converter
            client = collections[0].client
            helper = collections[0].helper
        call = None
        state = None
        nargs = op_parser.get_nargs()
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            args = {
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
            call = NCall(client.find_one, args, nargs)
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            args, state, func = converter.convert_put(
                op_parser.get_key(),
                op_parser.get_value(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            if func == "replace_one":
                call = NCall(client.replace_one, args, nargs)
            elif func == "insert_one":
                call = NCall(
                    client.insert_one,
                    args,
                    nargs,
                    {DuplicateKeyError: PreconditionFailedError},
                )
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            (args, state, func) = converter.convert_update(
                op_parser.get_key(),
                op_parser.get_set(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
                op_parser.get_returning(),
            )
            if func == "update_one":
                call = NCall(client.update_one, args, nargs)
            elif func == "find_one_and_update":
                call = NCall(client.find_one_and_update, args, nargs)
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            args = converter.convert_delete(
                op_parser.get_key(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            call = NCall(client.delete_one, args, nargs)
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            args = converter.convert_query(
                select=op_parser.get_select(),
                where=op_parser.get_where(),
                order_by=op_parser.get_order_by(),
                limit=op_parser.get_limit(),
                offset=op_parser.get_offset(),
            )
            args = {"args": args, "nargs": nargs}
            call = NCall(helper.query, args)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            args = converter.convert_count(
                where=op_parser.get_where(),
            )
            call = NCall(client.count_documents, args, nargs)
        # BATCH
        elif op_parser.op_equals(StoreOperation.BATCH):
            args, state = converter.convert_batch(
                op_parser.get_operation_parsers()
            )
            call = NCall(helper.batch, args, None)
        # TRANSACT
        elif op_parser.op_equals(StoreOperation.TRANSACT):
            args, state = OperationConverter.convert_transact(
                op_parser.get_operation_parsers(),
                [col.converter for col in collections],
            )
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
        collections: list[MongoDBCollection],
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
            if nresult is None:
                raise NotFoundError
            result = build_item_from_value(
                processor=processor,
                value=nresult,
                include_value=True,
            )
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            where = op_parser.get_where()
            exists = op_parser.get_where_exists()
            if exists is False:
                pass
            elif where is not None:
                if nresult.matched_count == 0:
                    raise PreconditionFailedError
            result = build_item_from_value(
                processor=processor,
                value=state["value"] if state is not None else None,
            )
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            where = op_parser.get_where()
            returning = op_parser.get_returning()
            if where is None:
                if returning is None:
                    if nresult.matched_count == 0:
                        raise NotFoundError
                else:
                    if nresult is None:
                        raise NotFoundError
            elif where is not None:
                if returning is None:
                    if nresult.matched_count == 0:
                        raise PreconditionFailedError
                else:
                    if nresult is None:
                        raise PreconditionFailedError
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
            where = op_parser.get_where()
            if where is None:
                if nresult.deleted_count == 0:
                    raise NotFoundError
            elif where is not None:
                if nresult.deleted_count == 0:
                    raise PreconditionFailedError
            result = None
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            items: list = []
            for item in nresult:
                items.append(
                    build_item_from_value(
                        processor=processor, value=item, include_value=True
                    )
                )
            result = build_query_result(items)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            result = nresult
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
                args, state, func = converter.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(
                    {"func": func, "args": args, "client": converter.client}
                )
                states.append(state)
            elif op_parser.op_equals(StoreOperation.UPDATE):
                (args, state, func) = converter.convert_update(
                    op_parser.get_key(),
                    op_parser.get_set(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                    op_parser.get_returning(),
                )
                ops.append(
                    {"func": func, "args": args, "client": converter.client}
                )
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args = converter.convert_delete(
                    op_parser.get_key(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(
                    {
                        "func": "delete_one",
                        "args": args,
                        "client": converter.client,
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
                args, state, func = self.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(ReplaceOne(**args))
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args = self.convert_delete(
                    op_parser.get_key(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(DeleteOne(**args))
                states.append(None)
        return {"ops": ops}, {"values": states}

    def convert_get(self, key: Value) -> dict:
        filter = self.processor.get_key_from_key(key)
        args = {"filter": filter}
        return args

    def convert_put(
        self,
        key: Value,
        value: dict,
        where: Expression | None,
        exists: bool | None,
    ) -> tuple[dict, dict | None, str]:
        document = self.processor.add_embed_fields(value, key)
        if key is not None:
            filter = self.processor.get_key_from_key(key)
        else:
            filter = self.processor.get_key_from_value(document)
        if where is None:
            args = {
                "filter": filter,
                "replacement": document,
                "upsert": True,
            }
            func = "replace_one"
        elif exists is False:
            args = {"document": document}
            func = "insert_one"
        elif exists is True:
            args = {
                "filter": filter,
                "replacement": document,
            }
            func = "replace_one"
        elif where is not None:
            where_filter = self.convert_expr(where)
            and_filter = {"$and": [filter, where_filter]}
            args = {
                "filter": and_filter,
                "replacement": document,
            }
            func = "replace_one"
        return args, {"value": document}, func

    def convert_update(
        self,
        key: Value,
        set: Update,
        where: Expression | None,
        exists: bool | None,
        returning: bool | None,
    ) -> tuple[dict, dict | None, str]:
        state = None
        filter = self.processor.get_key_from_key(key)
        if self.processor.needs_local_etag():
            etag = self.processor.generate_etag()
            set = self.processor.add_etag_update(set, etag)
            state = {"etag": etag}
        updates = self.convert_update_ops(set)
        if where is None or exists is True:
            args: dict = {"filter": filter, "update": updates}
        elif where is not None:
            where_filter = self.convert_expr(where)
            and_filter = {"$and": [filter, where_filter]}
            args = {"filter": and_filter, "update": updates}
        if returning is None:
            func = "update_one"
        else:
            args = args | {"return_document": returning}
            func = "find_one_and_update"
        return args, state, func

    def convert_delete(
        self, key: Value, where: Expression | None, exists: bool | None
    ) -> dict:
        filter = self.processor.get_key_from_key(key)
        if where is None or exists is True:
            args = {"filter": filter}
        elif where is not None:
            where_filter = self.convert_expr(where)
            and_filter = {"$and": [filter, where_filter]}
            args = {"filter": and_filter}
        return args

    def convert_query(
        self,
        select: Select | None = None,
        where: Expression | None = None,
        order_by: OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict:
        args = {}
        if select is not None:
            args["projection"] = self.convert_select(select)
        if where is not None:
            args["filter"] = self.convert_expr(where)
        if order_by is not None:
            args["sort"] = self.convert_order_by(order_by)
        if limit is not None:
            args["limit"] = limit
        if offset is not None:
            args["skip"] = offset
        return args

    def convert_count(self, where: Expression | None = None) -> dict:
        args = {}
        if where is not None:
            args["filter"] = self.convert_expr(where)
        else:
            args["filter"] = {}
        return args

    def convert_field(self, field: Field | str) -> str:
        path: str
        if isinstance(field, str):
            path = self.processor.resolve_field(field)
        elif isinstance(field, Field):
            path = self.processor.resolve_field(field.path)
        return path.replace("[", ".").replace("]", "").rstrip(".")

    def convert_comparison(self, expr: Comparison) -> dict:
        func = False
        if isinstance(expr.lexpr, Field):
            lhs = self.convert_field(expr.lexpr)
            rhs = expr.rexpr
        elif isinstance(expr.rexpr, Field):
            lhs = self.convert_field(expr.rexpr)
            rhs = expr.lexpr
        elif isinstance(expr.lexpr, Function):
            func = True
            lhs = self.convert_func(expr.lexpr)
            rhs = expr.rexpr
        elif isinstance(expr.rexpr, Function):
            func = True
            lhs = self.convert_func(expr.rexpr)
            rhs = expr.lexpr
        else:
            raise BadRequestError("Comparison not supported")
        ops_map = {
            ComparisonOp.LT: "$lt",
            ComparisonOp.LTE: "$lte",
            ComparisonOp.GT: "$gt",
            ComparisonOp.GTE: "$gte",
            ComparisonOp.EQ: "$eq",
            ComparisonOp.NEQ: "$ne",
            ComparisonOp.IN: "$in",
            ComparisonOp.NIN: "$nin",
        }
        op = expr.op
        if op in ops_map:
            nop = ops_map[op]
            if not func:
                return {lhs: {nop: rhs}}
            else:
                return {"$expr": {nop: [lhs, rhs]}}
        else:
            if op is ComparisonOp.BETWEEN:
                if isinstance(rhs, list):
                    return {lhs: {"$gte": rhs[0], "$lte": rhs[1]}}
            elif op is ComparisonOp.LIKE:
                regex = re.escape(str(rhs))
                return {lhs: {"$regex": regex}}
        raise BadRequestError(f"Comparison {expr} not supported")

    def convert_func(self, expr: Function) -> Any:
        namespace = expr.namespace
        name = expr.name
        args = expr.args
        if namespace == FunctionNamespace.BUILTIN:
            if name == StoreFunctionName.IS_TYPE:
                field = self.convert_field(args[0])
                type = args[1]
                if isinstance(type, str):
                    type = DocumentFieldType(type.lower())
                if type == DocumentFieldType.STRING:
                    return {field: {"$type": "string"}}
                elif type == DocumentFieldType.NUMBER:
                    return {
                        "$or": [
                            {field: {"$type": "double"}},
                            {field: {"$type": "int"}},
                            {field: {"$type": "long"}},
                            {field: {"$type": "decimal"}},
                        ]
                    }
                elif type == DocumentFieldType.BOOLEAN:
                    return {field: {"$type": "bool"}}
                elif type == DocumentFieldType.OBJECT:
                    return {field: {"$type": "object"}}
                elif type == DocumentFieldType.ARRAY:
                    return {field: {"$type": "array"}}
                elif type == DocumentFieldType.NULL:
                    return {field: {"$type": "null"}}
            if name == StoreFunctionName.IS_DEFINED:
                field = self.convert_field(args[0])
                return {field: {"$exists": True}}
            if name == StoreFunctionName.IS_NOT_DEFINED:
                field = self.convert_field(args[0])
                return {field: {"$exists": False}}
            if name == StoreFunctionName.LENGTH:
                field = self.convert_field(args[0])
                splits = field.split(".")
                if splits[-1].isnumeric():
                    arr_field = str.join(".", splits[0:-1])
                    arr_index = int(splits[-1])
                    return {
                        "$strLenCP": {
                            "$arrayElemAt": [f"${arr_field}", arr_index]
                        }
                    }
                else:
                    return {"$strLenCP": f"${field}"}
            if name == StoreFunctionName.CONTAINS:
                field = self.convert_field(args[0])
                regex = re.escape(args[1])
                return {field: {"$regex": regex}}
            if name == StoreFunctionName.STARTS_WITH:
                field = self.convert_field(args[0])
                regex = re.escape(args[1])
                return {field: {"$regex": f"^{regex}"}}
            if name == StoreFunctionName.ARRAY_LENGTH:
                field = self.convert_field(args[0])
                return {"$size": f"${field}"}
            if name == StoreFunctionName.ARRAY_CONTAINS:
                field = self.convert_field(args[0])
                return {field: {"$all": [args[1]]}}
            if name == StoreFunctionName.ARRAY_CONTAINS_ANY:
                field = self.convert_field(args[0])
                return {field: {"$in": args[1]}}
        raise BadRequestError(f"Function {name} not recognized")

    def convert_expr(self, expr: Expression | None) -> Any:
        if expr is None or isinstance(
            expr, (str, int, float, bool, dict, list)
        ):
            return expr
        if isinstance(expr, Field):
            return self.convert_field(expr)
        if isinstance(expr, Function):
            return self.convert_func(expr)
        if isinstance(expr, Comparison):
            return self.convert_comparison(expr)
        if isinstance(expr, And):
            return {
                "$and": [
                    self.convert_expr(expr.lexpr),
                    self.convert_expr(expr.rexpr),
                ]
            }
        if isinstance(expr, Or):
            return {
                "$or": [
                    self.convert_expr(expr.lexpr),
                    self.convert_expr(expr.rexpr),
                ]
            }
        if isinstance(expr, Not):
            return {"$nor": [self.convert_expr(expr.expr)]}
        raise BadRequestError(f"Expression {expr!r} not supported")

    def convert_order_by(self, order_by: OrderBy) -> Any:
        sort_list = []
        for term in order_by.terms:
            field = self.convert_field(term.field)
            if (
                term.direction is None
                or term.direction == OrderByDirection.ASC
            ):
                sort_list.append((field, 1))
            elif term.direction == OrderByDirection.DESC:
                sort_list.append((field, -1))
        return sort_list

    def convert_select(self, select: Select) -> Any:
        if len(select.terms) == 0:
            return None
        field_paths = []
        for term in select.terms:
            field_path = self.convert_field(term.field)
            field_paths.append(field_path)
        return field_paths

    def convert_update_ops(self, update: Update) -> dict:
        set = {}
        unset = {}
        inc = {}
        rename = {}
        push = {}
        pop = {}
        pull = {}
        add_to_set = {}

        for operation in update.operations:
            field = self.convert_field(Field(path=operation.field))
            splits = field.split(".")
            op = operation.op
            if splits[-1].isnumeric():
                array_field = str.join(".", splits[:-1])
                array_index = int(splits[-1])
                if op == UpdateOp.PUT:
                    set[field] = operation.args[0]
                elif op == UpdateOp.INSERT:
                    if isinstance(operation.args[0], list):
                        arr = operation.args[0]
                    else:
                        arr = [operation.args[0]]
                    push[array_field] = {
                        "$each": arr,
                        "$position": array_index,
                    }
                elif op == UpdateOp.INCREMENT:
                    inc[field] = operation.args[0]
                elif op == UpdateOp.DELETE:
                    if array_index == 0:
                        pop[array_field] = -1
                    else:
                        set[array_field] = {
                            "$concatArrays": [
                                {"$slice": [f"${array_field}", array_index]},
                                {
                                    "$slice": [
                                        f"${array_field}",
                                        array_index + 1,
                                        {"$size": f"${array_field}"},
                                    ]
                                },
                            ]
                        }
            elif splits[-1] == "-":
                array_field = str.join(".", splits[:-1])
                if op == UpdateOp.INSERT:
                    if isinstance(operation.args[0], list):
                        arr = operation.args[0]
                    else:
                        arr = [operation.args[0]]
                    push[array_field] = {
                        "$each": arr,
                    }
                elif op == UpdateOp.DELETE:
                    pop[array_field] = 1
            else:
                if op == UpdateOp.PUT:
                    set[field] = operation.args[0]
                elif op == UpdateOp.INSERT:
                    set[field] = operation.args[0]
                elif op == UpdateOp.INCREMENT:
                    inc[field] = operation.args[0]
                elif op == UpdateOp.DELETE:
                    unset[field] = ""
                elif op == UpdateOp.MOVE:
                    rename[field] = operation.args[0].path
                elif op == UpdateOp.ARRAY_UNION:
                    add_to_set[field] = {"$each": operation.args[0]}
                elif op == UpdateOp.ARRAY_REMOVE:
                    pull[field] = {"$in": operation.args[0]}

        res = {}
        if len(set) > 0:
            res["$set"] = set
        if len(unset) > 0:
            res["$unset"] = unset
        if len(inc) > 0:
            res["$inc"] = inc
        if len(rename) > 0:
            res["$rename"] = rename
        if len(push) > 0:
            res["$push"] = push
        if len(pull) > 0:
            res["$pull"] = pull
        if len(pop) > 0:
            res["$pop"] = pop
        if len(add_to_set) > 0:
            res["$addToSet"] = add_to_set
        return res


class ResourceHelper:
    mongo_client: Any
    database_client: Any

    def __init__(self, mongo_client: Any, database_client: Any):
        self.mongo_client = mongo_client
        self.database_client = database_client

    def create_collection(
        self,
        collection: str,
        config: DocumentCollectionConfig | None,
        exists: bool | None,
        nargs: Any,
    ):
        try:
            NCall(
                self.database_client.create_collection,
                {"name": collection},
                nargs,
            ).invoke()
        except CollectionInvalid:
            if exists is False:
                raise ConflictError

    def drop_collection(
        self,
        collection: str,
        exists: bool | None,
        nargs: Any,
    ):
        response = NCall(
            self.database_client.drop_collection,
            {"name_or_collection": collection},
            nargs,
        ).invoke()
        if exists is True and "ns" not in response:
            raise NotFoundError

    def list_collections(self, nargs) -> Any:
        nresult = NCall(
            self.database_client.list_collection_names, None, nargs
        ).invoke()
        return nresult

    def transact(self, ops: list[dict]) -> Any:
        nresult = []
        with self.mongo_client.start_session() as session:
            with session.start_transaction():
                for op in ops:
                    func = op["func"]
                    client = op["client"]
                    args = op["args"]
                    args["session"] = session
                    if func == "insert_one":
                        res = client.insert_one(**args)
                    elif func == "replace_one":
                        res = client.replace_one(**args)
                        if "upsert" not in args and res.matched_count == 0:
                            raise ConflictError
                    elif func == "update_one":
                        res = client.update_one(**args)
                        if res.matched_count == 0:
                            raise ConflictError
                    elif func == "find_one_and_update":
                        res = client.find_one_and_update(**args)
                        if res is None:
                            raise ConflictError
                    elif func == "delete_one":
                        res = client.delete_one(**args)
                        if res.deleted_count == 0:
                            raise ConflictError
                    nresult.append(res)
                return nresult

    def close(self, nargs: Any) -> Any:
        pass


class AsyncResourceHelper:
    mongo_client: Any
    database_client: Any

    def __init__(self, mongo_client: Any, database_client: Any):
        self.mongo_client = mongo_client
        self.database_client = database_client

    async def create_collection(
        self,
        collection: str,
        config: DocumentCollectionConfig | None,
        exists: bool | None,
        nargs: Any,
    ):
        try:
            await NCall(
                self.database_client.create_collection,
                {"name": collection},
                nargs,
            ).ainvoke()
        except CollectionInvalid:
            if exists is False:
                raise ConflictError

    async def drop_collection(
        self,
        collection: str,
        exists: bool | None,
        nargs: Any,
    ):
        response = await NCall(
            self.database_client.drop_collection,
            {"name_or_collection": collection},
            nargs,
        ).ainvoke()
        if exists is True and "ns" not in response:
            raise NotFoundError

    async def list_collections(self, nargs) -> Any:
        nresult = await NCall(
            self.database_client.list_collection_names, None, nargs
        ).ainvoke()
        return nresult

    async def transact(self, ops: list[dict]) -> Any:
        nresult = []
        async with await self.mongo_client.start_session() as session:
            async with session.start_transaction():
                for op in ops:
                    func = op["func"]
                    client = op["client"]
                    args = op["args"]
                    args["session"] = session
                    if func == "insert_one":
                        res = await client.insert_one(**args)
                    elif func == "replace_one":
                        res = await client.replace_one(**args)
                        if "upsert" not in args and res.matched_count == 0:
                            raise ConflictError
                    elif func == "update_one":
                        res = await client.update_one(**args)
                        if res.matched_count == 0:
                            raise ConflictError
                    elif func == "find_one_and_update":
                        res = await client.find_one_and_update(**args)
                        if res is None:
                            raise ConflictError
                    elif func == "delete_one":
                        res = await client.delete_one(**args)
                        if res.deleted_count == 0:
                            raise ConflictError
                    nresult.append(res)
                return nresult

    async def close(self, nargs: Any) -> Any:
        pass


class ClientHelper:
    client: Any
    processor: ItemProcessor

    def __init__(self, client: Any, processor: ItemProcessor):
        self.client = client
        self.processor = processor

    def query(self, args, nargs) -> Any:
        nresult = NCall(
            self.client.find,
            args,
            nargs,
        ).invoke()
        return nresult

    def batch(self, ops: list) -> Any:
        nresult = self.client.bulk_write(ops)
        return nresult


class AsyncClientHelper:
    client: Any
    processor: ItemProcessor

    def __init__(self, client: Any, processor: ItemProcessor):
        self.client = client
        self.processor = processor

    async def query(self, args, nargs) -> Any:
        response = NCall(self.client.find, args, nargs).invoke()
        nresult = []
        async for item in response:
            nresult.append(item)
        return nresult

    async def batch(self, ops: list) -> Any:
        nresult = await self.client.bulk_write(ops)
        return nresult


class MongoDBCollection:
    client: Any
    converter: OperationConverter
    processor: ItemProcessor
    helper: Any

    def __init__(
        self,
        client: Any,
        helper_type: Any,
        id_map_field: str | None,
        pk_map_field: str | None,
        etag_embed_field: str | None,
        suppress_fields: list[str] | None,
    ) -> None:
        self.client = client
        self.processor = ItemProcessor(
            id_embed_field="_id",
            etag_embed_field=etag_embed_field,
            id_map_field=id_map_field,
            pk_map_field=pk_map_field,
            local_etag=True,
            suppress_fields=suppress_fields,
        )
        self.converter = OperationConverter(
            processor=self.processor, client=self.client
        )
        self.helper = helper_type(client, self.processor)
