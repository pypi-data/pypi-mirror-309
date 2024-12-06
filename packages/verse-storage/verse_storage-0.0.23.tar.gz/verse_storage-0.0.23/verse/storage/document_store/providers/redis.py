"""
Document Store on Redis.
"""

from __future__ import annotations

__all__ = ["Redis"]

import json
from typing import Any

from verse.core import Context, NCall, Operation, Response
from verse.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    PreconditionFailedError,
)
from verse.internal.storage_core import (
    ItemProcessor,
    JSONHelper,
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
    Not,
    Or,
    OrderBy,
    OrderByDirection,
    Select,
    Update,
    UpdateOp,
    UpdateOperation,
    Value,
)

from .._helper import (
    build_item_from_parts,
    build_item_from_value,
    build_query_result,
    get_collection_config,
)
from .._models import DocumentCollectionConfig


class Redis(StoreProvider):
    collection: str | None
    url: str | None
    host: str | None
    port: int | None
    username: str | None
    password: str | None
    options: dict | None
    id_map_field: str | dict | None
    pk_map_field: str | dict | None
    etag_embed_field: str | dict | None
    suppress_fields: list[str] | None
    field_types: dict | dict[str, dict] | None
    index: list[str] | dict[str, list[str]] | None
    find_index: bool | None
    nparams: dict[str, Any]

    _lib: Any
    _alib: Any

    _client: Any
    _aclient: Any
    _collection_cache: dict[str, RedisCollection]
    _acollection_cache: dict[str, RedisCollection]

    def __init__(
        self,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        options: dict | None = None,
        collection: str | None = None,
        id_map_field: str | dict | None = "id",
        pk_map_field: str | dict | None = "pk",
        etag_embed_field: str | dict | None = "_etag",
        suppress_fields: list[str] | None = None,
        field_types: dict | dict[str, dict] | None = None,
        index: list[str] | dict[str, list[str]] | None = None,
        find_index: bool | None = True,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            url:
                Redis endpoint url.
            host:
                Redis endpoint host name.
            port:
                Redis endpoint port.
            username:
                Username for auth.
            password:
                Password for auth.
            options:
                Redis client options.
            collection:
                Collection name.
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
            field_types:
                Field types as a dictionary where key is the field name
                and value is the JSON type.
                Some operations in Redis simply returns a string.
                The types provided here are used to convert them to
                the correct types.
                To specify for multiple collections,
                use a dictionary of dictionary
                where the key is the collection name and the value
                dictionary of field types.
            index:
                Redis search index to use for collection.
                To provide a single index, use string.
                To provide multiple indexes, use list.
                To specify for multiple collections,
                use a dictionary of list of strings,
                where the key is the collection name and the value is the
                list of index names.
            find_index:
                A value indicating whether the index should be found
                automatically for the collection.
            nparams:
                Native parameters to the redis client.
        """
        self.collection = collection
        self.url = url
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.options = options
        self.id_map_field = id_map_field
        self.pk_map_field = pk_map_field
        self.etag_embed_field = etag_embed_field
        self.suppress_fields = suppress_fields
        self.field_types = field_types
        self.index = index
        self.find_index = find_index
        self.nparams = nparams

        self._client = None
        self._aclient = None
        self._collection_cache = dict()
        self._acollection_cache = dict()

    def init(self, context: Context | None = None) -> None:
        if self._client is not None:
            return

        import redis

        self._lib = redis
        options: dict = self.options if self.options is not None else {}
        if self.url is not None:
            self._client = redis.from_url(
                self.url, decode_responses=True, **options
            )
        elif self.host is not None and self.port is not None:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                decode_responses=True,
                **options,
            )
        else:
            raise BadRequestError(
                "Redis initialization needs url or host and port"
            )

    async def ainit(self, context: Context | None = None) -> None:
        if self._aclient is not None:
            return

        import redis.asyncio as redis

        self._alib = redis
        options: dict = self.options if self.options is not None else {}
        if self.url is not None:
            self._aclient = redis.from_url(
                self.url, decode_responses=True, **options
            )
        elif self.host is not None and self.port is not None:
            self._aclient = redis.Redis(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                decode_responses=True,
                **options,
            )
        else:
            raise BadRequestError(
                "Redis initialization needs url or host and port"
            )

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
    ) -> list[RedisCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[RedisCollection] = []
            for single_op_parser in op_parser.get_operation_parsers():
                collections.extend(self._get_collections(single_op_parser))
            return collections
        db_collection = self._get_collection_name(op_parser)
        if db_collection is None:
            raise BadRequestError("Collection name must be specified")
        if db_collection in self._collection_cache:
            return [self._collection_cache[db_collection]]
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, db_collection
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, db_collection
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, db_collection
        )
        field_types = ParameterParser.get_collection_parameter(
            self.field_types, db_collection, is_parameter_dict=True
        )
        index_names = []
        if self.find_index:
            index_names = self._client.execute_command("FT._LIST")
        else:
            index_names = self._get_index_names_from_config(db_collection)
        indexes = [
            self._client.ft(index_name).info() for index_name in index_names
        ]
        col = RedisCollection(
            db_collection,
            self._client,
            ClientHelper,
            self._lib,
            id_map_field,
            pk_map_field,
            etag_embed_field,
            self.suppress_fields,
            field_types,
            indexes,
        )
        self._collection_cache[db_collection] = col
        return [col]

    async def _aget_collections(
        self, op_parser: StoreOperationParser
    ) -> list[RedisCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[RedisCollection] = []
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
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, db_collection
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, db_collection
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, db_collection
        )
        field_types = ParameterParser.get_collection_parameter(
            self.field_types, db_collection, is_parameter_dict=True
        )
        index_names = []
        if self.find_index:
            index_names = await self._aclient.execute_command("FT._LIST")
        else:
            index_names = self._get_index_names_from_config(db_collection)
        indexes = [
            await self._aclient.ft(index_name).info()
            for index_name in index_names
        ]
        col = RedisCollection(
            db_collection,
            self._aclient,
            AsyncClientHelper,
            self._alib,
            id_map_field,
            pk_map_field,
            etag_embed_field,
            self.suppress_fields,
            field_types,
            indexes,
        )
        self._acollection_cache[db_collection] = col
        return [col]

    def _get_index_names_from_config(self, collection) -> list[str]:
        indexes = []
        collection_indexes: Any = None
        if isinstance(self.index, dict):
            if collection in self.index:
                collection_indexes = self.index[collection]
        elif isinstance(self.index, (list, str)):
            collection_indexes = self.index
        if isinstance(collection_indexes, str):
            indexes.append(collection_indexes)
        elif isinstance(collection_indexes, list):
            indexes.extend(collection_indexes)
        return indexes

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
            ResourceHelper(self._client, self._lib),
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
            op_parser,
            collections,
            AsyncResourceHelper(self._aclient, self._alib),
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
        collections: list[RedisCollection],
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
            args: dict | list = {
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
            call = NCall(client.json().get, args, nargs, {None: NotFoundError})
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            args, state, func = converter.convert_put(
                op_parser.get_key(),
                op_parser.get_value(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            if func == "set":
                call = NCall(
                    client.json().set,
                    args,
                    nargs,
                )
            elif func == "helper":
                call = NCall(helper.put, args)
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            (args, state, func) = converter.convert_update(
                op_parser.get_key(),
                op_parser.get_set(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
                op_parser.get_returning(),
            )
            call = NCall(helper.update, args)
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            args, func = converter.convert_delete(
                op_parser.get_key(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            if func == "delete":
                call = NCall(client.json().delete, args, nargs)
            elif func == "helper":
                call = NCall(helper.delete, args)
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            args = converter.convert_query(
                select=op_parser.get_select(),
                where=op_parser.get_where(),
                order_by=op_parser.get_order_by(),
                limit=op_parser.get_limit(),
                offset=op_parser.get_offset(),
                collection=op_parser.get_collection_name(),
            )
            call = NCall(client.execute_command, args, nargs)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            args = converter.convert_count(
                where=op_parser.get_where(),
                collection=op_parser.get_collection_name(),
            )
            call = NCall(client.execute_command, args, nargs)
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
        collections: list[RedisCollection],
    ) -> Any:
        if len(collections) == 1:
            processor = collections[0].processor
        result: Any = None
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            result = None
        # DROP
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            result = None
        # LIST
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
            if nresult is None:
                raise PreconditionFailedError
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
            where = op_parser.get_where()
            if nresult == 0:
                if where is None:
                    raise NotFoundError
                else:
                    raise PreconditionFailedError
            result = None
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            select = op_parser.get_select()
            items: list = []
            parse_json = True
            local_project = False
            for i in range(0, int((len(nresult) - 1) / 2)):
                item = nresult[2 * (i + 1)]
                if select is not None and len(select.terms) > 0:
                    if processor.field_types is not None:
                        parse_json = False
                    else:
                        local_project = True
                if parse_json:
                    value = json.loads(item[-1])
                else:
                    value = {}
                    for j in range(0, int(len(item) / 2)):
                        field = item[j * 2].replace("$.", "")
                        field_value = item[(j * 2) + 1]
                        value[field] = [
                            processor.convert_type(field, field_value)
                        ]
                    value = QueryHelper.normalize_select_get(value)
                items.append(
                    build_item_from_value(
                        processor=processor,
                        value=value,
                        include_value=True,
                    )
                )
            if local_project:
                items = QueryProcessor.project_item(
                    result, select, processor.resolve_field
                )
            result = build_query_result(items)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            result = int(nresult[1][1])
        # BATCH
        elif op_parser.op_equals(StoreOperation.BATCH):
            result = []
            if state is not None:
                for c in state["values"]:
                    if c is not None:
                        result.append(
                            build_item_from_value(
                                processor=processor,
                                value=c["value"],
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
                    c = state["values"][i]
                result.append(
                    self._convert_nresult(
                        nresult[i], c, op_parsers[i], [collections[i]]
                    )
                )
        return result


class OperationConverter:
    processor: ItemProcessor
    index_manager: IndexManager
    collection_name: str

    def __init__(
        self,
        processor: ItemProcessor,
        index_manager: IndexManager,
        collection_name: str,
    ):
        self.processor = processor
        self.index_manager = index_manager
        self.collection_name = collection_name

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
                    {
                        "op": StoreOperation.PUT,
                        "func": func,
                        "args": args,
                        "converter": converter,
                        "processor": converter.processor,
                    }
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
                    {
                        "op": StoreOperation.UPDATE,
                        "func": func,
                        "args": args,
                        "converter": converter,
                        "processor": converter.processor,
                    }
                )
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args, func = converter.convert_delete(
                    op_parser.get_key(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append(
                    {
                        "op": StoreOperation.DELETE,
                        "func": func,
                        "args": args,
                        "converter": converter,
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
                args, state, func = self.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append({"op": StoreOperation.PUT, "args": args})
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args, func = self.convert_delete(
                    op_parser.get_key(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append({"op": StoreOperation.DELETE, "args": args})
                states.append(None)
        return {"ops": ops}, {"values": states}

    def convert_get(self, key: Value) -> dict:
        id = self.processor.get_id_from_key(key)
        db_key = self.get_key(id)
        args = {"name": db_key}
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
            id = self.processor.get_id_from_key(key)
        else:
            id = self.processor.get_id_from_value(document)
        db_key = self.get_key(id)
        if where is None:
            args: dict = {"name": db_key, "path": "$", "obj": document}
            func = "set"
        elif exists is False:
            args = {
                "name": db_key,
                "path": "$",
                "obj": document,
                "nx": True,
            }
            func = "set"
        elif exists is True:
            args = {
                "name": db_key,
                "path": "$",
                "obj": document,
                "xx": True,
            }
            func = "set"
        elif where is not None:
            args = {"key": db_key, "document": document, "where": where}
            func = "helper"
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
        id = self.processor.get_id_from_key(key=key)
        if self.processor.needs_local_etag():
            etag = self.processor.generate_etag()
            set = self.processor.add_etag_update(set, etag)
            state = {"etag": etag}
        db_key = self.get_key(id)
        args = {
            "key": db_key,
            "update": set,
            "where": where,
            "returning": returning,
        }
        func = "helper"
        if (
            (where is None or exists is True)
            and returning is None
            and len(set.operations) == 1
            and set.operations[0].op != UpdateOp.DELETE
        ):
            args["single_op"] = True
        else:
            args["single_op"] = False
        return args, state, func

    def convert_delete(
        self, key: Value, where: Expression | None, exists: bool | None
    ) -> tuple[dict, str]:
        id = self.processor.get_id_from_key(key=key)
        db_key = self.get_key(id)
        if where is None or exists is True:
            args: dict = {"key": db_key}
            func = "delete"
        else:
            args = {"key": db_key, "where": where}
            func = "helper"
        return args, func

    def convert_query(
        self,
        select: Select | None = None,
        where: Expression | None = None,
        order_by: OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | None = None,
    ) -> list[Any]:
        args: list = ["FT.SEARCH"]
        explicit_index = self._get_explicit_index(collection)
        order_by_field = self._get_order_by_field(order_by)
        where_fields = self._get_where_fields(where)
        index = self.index_manager.get_best_index(
            order_by_field, where_fields, explicit_index
        )
        if index is None:
            raise BadRequestError(
                f"Index for query not found {where_fields} {order_by_field}"
            )
        where_clause = self.convert_where(where, index)
        args.append(index.name)
        args.append(where_clause)
        if order_by is not None:
            order_by_clause = self.convert_order_by(order_by, index)
            args.extend(order_by_clause)
        limit_clause = 10000
        offset_clause = 0
        if limit is not None:
            limit_clause = limit
        if offset is not None:
            offset_clause = offset
        args.append("LIMIT")
        args.append(offset_clause)
        args.append(limit_clause)
        if (
            select is not None
            and len(select.terms) > 0
            and self.processor.field_types is not None
        ):
            select_fields = self._get_select_fields(select)
            args.append("RETURN")
            args.append(len(select_fields))
            args.extend(select_fields)
        return args

    def convert_count(
        self,
        where: Expression | None = None,
        collection: str | None = None,
    ) -> list[Any]:
        args: list = ["FT.AGGREGATE"]
        explicit_index = self._get_explicit_index(collection)
        where_fields = self._get_where_fields(where)
        index = self.index_manager.get_best_index(
            None, where_fields, explicit_index
        )
        if index is None:
            raise BadRequestError("Index not found")
        where_clause = self.convert_where(where, index)
        args.append(index.name)
        args.append(where_clause)
        args.extend(["GROUPBY", 0, "REDUCE", "COUNT", 0])
        return args

    def get_key(self, id) -> str:
        return f"{self.collection_name}:{id}"

    def convert_field(self, field: Field | str) -> str:
        if isinstance(field, Field):
            return self.processor.resolve_field(field.path)
        return self.processor.resolve_field(field)

    def convert_update_ops(
        self, client: Any, key: str, update: Update
    ) -> list[NCall]:
        calls = []
        for operation in update.operations:
            calls.append(self.convert_update_op(client, key, operation))
        return calls

    def convert_update_op(
        self, client: Any, key: str, operation: UpdateOperation
    ) -> NCall:
        field = self.convert_field(operation.field)
        path = field.replace("[", ".").replace("]", "").rstrip(".")
        splits = path.split(".")
        op = operation.op
        if splits[-1].isnumeric():
            array_field = str.join(".", splits[:-1])
            array_index = int(splits[-1])
            if op == UpdateOp.PUT:
                return NCall(
                    client.json().set,
                    {
                        "name": key,
                        "path": f"$.{field}",
                        "obj": operation.args[0],
                    },
                )
            elif op == UpdateOp.INSERT:
                args = [key, f"$.{array_field}", array_index]
                if isinstance(operation.args[0], list):
                    args.extend(operation.args[0])
                else:
                    args.append(operation.args[0])
                return NCall(client.json().arrinsert, args)
            elif op == UpdateOp.INCREMENT:
                return NCall(
                    client.json().numincrby,
                    {
                        "name": key,
                        "path": f"$.{field}",
                        "number": operation.args[0],
                    },
                )
            elif op == UpdateOp.DELETE:
                return NCall(
                    client.json().arrpop,
                    {
                        "name": key,
                        "path": f"$.{array_field}",
                        "index": array_index,
                    },
                )
        elif splits[-1] == "-":
            array_field = str.join(".", splits[:-1])
            if op == UpdateOp.INSERT:
                args = [key, f"$.{array_field}"]
                if isinstance(operation.args[0], list):
                    args.extend(operation.args[0])
                else:
                    args.append(operation.args[0])
                return NCall(client.json().arrappend, args)
            elif op == UpdateOp.DELETE:
                return NCall(
                    client.json().arrpop,
                    {"name": key, "path": f"$.{array_field}", "index": -1},
                )
        else:
            if op == UpdateOp.PUT or op == UpdateOp.INSERT:
                return NCall(
                    client.json().set,
                    {
                        "name": key,
                        "path": f"$.{field}",
                        "obj": operation.args[0],
                    },
                )
            elif op == UpdateOp.INCREMENT:
                return NCall(
                    client.json().numincrby,
                    {
                        "name": key,
                        "path": f"$.{field}",
                        "number": operation.args[0],
                    },
                )
            elif op == UpdateOp.DELETE:
                return NCall(
                    client.json().delete, {"key": key, "path": f"$.{field}"}
                )
        raise BadRequestError(f"Update operation {operation} not supported")

    def convert_where(self, expr: Expression | None, index: Index) -> str:
        if expr is None:
            return "*"
        if isinstance(expr, Function):
            return self.convert_func(expr, index)
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
                raise BadRequestError(f"Comparison {expr!r} not supported")
            if expr.op in [ComparisonOp.EQ, ComparisonOp.NEQ]:
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_HASH
                )
                if type == IndexManager.REDIS_INDEX_TYPE_TAG:
                    query = f"@{attribute}:{{{self.escape(field_value)}}}"
                elif type == IndexManager.REDIS_INDEX_TYPE_TEXT:
                    query = f'@{attribute}:"{self.escape(field_value)}"'
                elif type == IndexManager.REDIS_INDEX_TYPE_NUMERIC:
                    query = f"@{attribute}:[{field_value!r} {field_value!r}]"
                if expr.op == ComparisonOp.NEQ:
                    query = f"-({query})"
                return query
            elif expr.op in [
                ComparisonOp.IN,
                ComparisonOp.NIN,
            ]:
                if not isinstance(field_value, list):
                    raise BadRequestError("IN needs a list operand")
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_HASH
                )
                if type == IndexManager.REDIS_INDEX_TYPE_TAG:
                    field_value = "|".join(
                        [f"{value}" for value in field_value]
                    )
                    query = f"@{attribute}:{{{self.escape(field_value)}}}"
                elif type == IndexManager.REDIS_INDEX_TYPE_TEXT:
                    field_value = "|".join(
                        [f'"{value}"' for value in field_value]
                    )
                    query = f"@{attribute}:{self.escape(field_value)}"
                elif type == IndexManager.REDIS_INDEX_TYPE_NUMERIC:
                    queries = []
                    for value in field_value:
                        queries.append(f"(@{attribute}:[{value} {value}])")
                    query = "|".join(queries)
                if expr.op == ComparisonOp.NIN:
                    query = f"-({query})"
                return query
            elif expr.op in [
                ComparisonOp.LT,
                ComparisonOp.LTE,
                ComparisonOp.GT,
                ComparisonOp.GTE,
                ComparisonOp.BETWEEN,
            ]:
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_RANGE
                )
                rhs = None
                if expr.op == ComparisonOp.LT:
                    rhs = f"[-inf {field_value!r})]"
                elif expr.op == ComparisonOp.LTE:
                    rhs = f"[-inf {field_value!r}]"
                elif expr.op == ComparisonOp.GT:
                    rhs = f"[{field_value!r} +inf]"
                elif expr.op == ComparisonOp.GTE:
                    rhs = f"[{field_value!r} +inf]"
                elif expr.op == ComparisonOp.BETWEEN:
                    if isinstance(field_value, list):
                        rhs = f"[{field_value[0]} {field_value[1]}]"
                    else:
                        raise BadRequestError(
                            "BETWEEN op needs list of 2 elements"
                        )
                return f"@{attribute}:{rhs}"
            elif expr.op in [ComparisonOp.LIKE]:
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_TEXT
                )
                query = f"@{attribute}:{self.escape(field_value)}"
            else:
                raise BadRequestError(
                    f"Comparison op {expr.op} is not supported"
                )
        if isinstance(expr, And):
            lhs = self.convert_where(expr.lexpr, index)
            rhs = self.convert_where(expr.rexpr, index)
            return f"({lhs}) ({rhs})"
        if isinstance(expr, Or):
            lhs = self.convert_where(expr.lexpr, index)
            rhs = self.convert_where(expr.rexpr, index)
            return f"({lhs})|({rhs})"
        if isinstance(expr, Not):
            query = self.convert_where(expr.expr, index)
            return f"-({query})"
        raise BadRequestError(f"Expression {expr!r} not supported")

    def convert_func(self, expr: Function, index: Index) -> str:
        namespace = expr.namespace
        name = expr.name
        args = expr.args
        if namespace == FunctionNamespace.BUILTIN:
            if name == StoreFunctionName.STARTS_WITH:
                field = self.convert_field(args[0])
                field_value = args[1]
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_HASH
                )
                if type == IndexManager.REDIS_INDEX_TYPE_TAG:
                    query = f"@{attribute}:{{{self.escape(field_value)}*}}"
                elif type == IndexManager.REDIS_INDEX_TYPE_TEXT:
                    query = f"@{attribute}:{self.escape(field_value)}*"
                return query
            if name == StoreFunctionName.CONTAINS:
                field = self.convert_field(args[0])
                field_value = args[1]
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_HASH
                )
                if type == IndexManager.REDIS_INDEX_TYPE_TAG:
                    query = f"@{attribute}:{{*{self.escape(field_value)}*}}"
                elif type == IndexManager.REDIS_INDEX_TYPE_TEXT:
                    query = f"@{attribute}:*{self.escape(field_value)}*"
                return query
            if name == StoreFunctionName.ARRAY_CONTAINS:
                field = self.convert_field(args[0])
                field_value = args[1]
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_HASH
                )
                if type == IndexManager.REDIS_INDEX_TYPE_TAG:
                    query = f"@{attribute}:{{{field_value}}}"
                elif type == IndexManager.REDIS_INDEX_TYPE_TEXT:
                    query = f'@{attribute}:"{field_value}"'
                elif type == IndexManager.REDIS_INDEX_TYPE_NUMERIC:
                    query = f"@{attribute}:[{field_value} {field_value}]"
                return query
            if name == StoreFunctionName.ARRAY_CONTAINS_ANY:
                field = self.convert_field(args[0])
                field_value = args[1]
                attribute, type = self.convert_index_field(
                    field, index, IndexManager.INDEX_TYPE_HASH
                )
                queries = []
                for value in field_value:
                    if type == IndexManager.REDIS_INDEX_TYPE_TAG:
                        queries.append(f"@{attribute}:{{{value}}}")
                    elif type == IndexManager.REDIS_INDEX_TYPE_TEXT:
                        queries.append(f'@{attribute}:"{value}"')
                    elif type == IndexManager.REDIS_INDEX_TYPE_NUMERIC:
                        queries.append(f"@{attribute}:[{value} {value}]")
                query = "|".join(queries)
                return query
        raise BadRequestError(f"Function {name} not supported")

    def convert_order_by(self, order_by: OrderBy, index: Index) -> list[str]:
        args = []
        for term in order_by.terms:
            field = self.convert_field(term.field)
            field, type = self.convert_index_field(
                field, index, IndexManager.INDEX_TYPE_HASH, sortable=True
            )
            if (
                term.direction is None
                or term.direction == OrderByDirection.ASC
            ):
                args = ["SORTBY", field, "ASC"]
            elif term.direction == OrderByDirection.DESC:
                args = ["SORTBY", field, "DESC"]
        return args

    def convert_select(self, query, select: Select):
        if len(select.terms) == 0:
            return query
        field_paths = []
        for term in select.terms:
            field_path = self.convert_field(term.field)
            field_paths.append(field_path)
        return query.select(field_paths)

    def convert_index_field(
        self,
        field: str,
        index: Index,
        index_type: str,
        sortable: bool | None = None,
    ) -> tuple[str, str]:
        if field in index.fields:
            index_attributes = index.fields[field]
            for index_attribute in index_attributes:
                if (
                    index_type == IndexManager.INDEX_TYPE_HASH
                    or (
                        index_type == IndexManager.INDEX_TYPE_RANGE
                        and index_attribute.type
                        == IndexManager.REDIS_INDEX_TYPE_NUMERIC
                    )
                    or (
                        index_type == IndexManager.INDEX_TYPE_TEXT
                        and index_attribute.type
                        == IndexManager.REDIS_INDEX_TYPE_TEXT
                    )
                ):
                    if sortable:
                        if not index_attribute.sortable:
                            continue
                    return index_attribute.attribute, index_attribute.type
        raise BadRequestError(f"Index not found for {field}")

    def _get_explicit_index(self, collection: str | None) -> str | None:
        if collection is not None and "." in collection:
            return collection.split(".")[-1]
        return None

    def _get_select_fields(self, select: Select | None) -> list[str]:
        select_fields = []
        if select is not None:
            for term in select.terms:
                field = self.processor.resolve_field(term.field)
                select_fields.append(f"$.{field}")
        return select_fields

    def _get_order_by_field(self, order_by: OrderBy | None) -> str | None:
        order_by_field = None
        if order_by is not None and len(order_by.terms) > 0:
            order_by_field = self.processor.resolve_field(
                order_by.terms[0].field
            )
        return order_by_field

    def _get_where_fields(self, expr: Expression | None) -> dict[str, list]:
        fields: dict = {}
        self._find_where_fields(expr, fields)
        return fields

    def _find_where_fields(
        self, expr: Expression | None, fields: dict[str, list]
    ):
        def add_field(field, index_type):
            field = self.processor.resolve_field(field)
            if field not in fields:
                fields[field] = []
            if index_type not in fields[field]:
                fields[field].append(index_type)

        if isinstance(expr, Comparison):
            field = None
            if isinstance(expr.lexpr, Field):
                field = expr.lexpr.path
            elif isinstance(expr.rexpr, Field):
                field = expr.rexpr.path
            if field is None:
                return
            if expr.op in [
                ComparisonOp.EQ,
                ComparisonOp.NEQ,
                ComparisonOp.IN,
                ComparisonOp.NIN,
            ]:
                add_field(field, IndexManager.INDEX_TYPE_HASH)
            elif expr.op in [
                ComparisonOp.LT,
                ComparisonOp.LTE,
                ComparisonOp.GT,
                ComparisonOp.GTE,
                ComparisonOp.BETWEEN,
            ]:
                add_field(field, IndexManager.INDEX_TYPE_RANGE)
            elif expr.op in [ComparisonOp.LIKE]:
                add_field(field, IndexManager.INDEX_TYPE_TEXT)
            else:
                raise BadRequestError(
                    f"Comparison op {expr.op} is not supported"
                )
        elif isinstance(expr, Function):
            if (
                expr.namespace == FunctionNamespace.BUILTIN
                and expr.name
                in [
                    StoreFunctionName.STARTS_WITH,
                    StoreFunctionName.CONTAINS,
                ]
                and isinstance(expr.args[0], Field)
            ):
                add_field(expr.args[0].path, IndexManager.INDEX_TYPE_HASH)
            elif (
                expr.namespace == FunctionNamespace.BUILTIN
                and expr.name
                in [
                    StoreFunctionName.ARRAY_CONTAINS,
                    StoreFunctionName.ARRAY_CONTAINS_ANY,
                ]
                and isinstance(expr.args[0], Field)
            ):
                add_field(expr.args[0].path, IndexManager.INDEX_TYPE_HASH)
            else:
                raise BadRequestError(f"Function {expr.name} is not supported")
        elif isinstance(expr, And):
            self._find_where_fields(expr.lexpr, fields)
            self._find_where_fields(expr.rexpr, fields)
        elif isinstance(expr, Or):
            self._find_where_fields(expr.lexpr, fields)
            self._find_where_fields(expr.rexpr, fields)
        elif isinstance(expr, Not):
            self._find_where_fields(expr.expr, fields)

    def escape(self, value: Any) -> str:
        # TODO: Handle $, {, }, \  |
        if isinstance(value, str):
            return value.replace("/", "\\/").replace("-", "\\-")
        return value


class IndexManager:
    INDEX_TYPE_HASH = "hash"
    INDEX_TYPE_RANGE = "range"
    INDEX_TYPE_TEXT = "text"

    REDIS_INDEX_TYPE_TAG = "TAG"
    REDIS_INDEX_TYPE_TEXT = "TEXT"
    REDIS_INDEX_TYPE_NUMERIC = "NUMERIC"
    REDIS_INDEX_SORTABLE = "SORTABLE"

    indexes: list[Index]

    def __init__(self, collection: str, db_indexes: list[Any]):
        self.indexes = []
        for db_index in db_indexes:
            prefixes = db_index["index_definition"][3]
            for prefix in prefixes:
                if prefix.startswith(collection):
                    self.indexes.append(self.parse_index(db_index))

    def __repr__(self):
        return str(self.__dict__)

    def get_best_index(
        self,
        order_by_field: str | None,
        where_fields: dict[str, list],
        explicit_index: str | None,
    ) -> Index | None:
        best_index = None
        for index in self.indexes:
            if explicit_index is not None:
                if index.name != explicit_index:
                    continue
            if order_by_field is not None:
                found = False
                if order_by_field in index.fields:
                    for index_attribute in index.fields[order_by_field]:
                        if index_attribute.sortable:
                            found = True
                if not found:
                    continue
            best_index = index
            for where_field in where_fields:
                found = False
                if where_field in index.fields:
                    index_types = where_fields[where_field]
                    for index_type in index_types:
                        index_attributes = index.fields[where_field]
                        for index_attribute in index_attributes:
                            if (
                                index_type == IndexManager.INDEX_TYPE_HASH
                                or (
                                    index_type == IndexManager.INDEX_TYPE_RANGE
                                    and index_attribute.type
                                    == IndexManager.REDIS_INDEX_TYPE_NUMERIC
                                )
                                or (
                                    index_type == IndexManager.INDEX_TYPE_TEXT
                                    and index_attribute.type
                                    == IndexManager.REDIS_INDEX_TYPE_TEXT
                                )
                            ):
                                found = True
                                break
                        if found:
                            break
                if not found:
                    best_index = None
                    break
            if best_index is None:
                continue
        return best_index

    def parse_index(self, db_index: Any) -> Index:
        index = Index()
        index.name = db_index["index_name"]

        for attribute in db_index["attributes"]:
            index_field = IndexField(
                attribute[1],
                attribute[3],
                attribute[5],
                IndexManager.REDIS_INDEX_SORTABLE in attribute,
            )
            field = attribute[1]
            if field.startswith("$."):
                field = field.replace("$.", "")
            if field.endswith(".*"):
                field = field.replace(".*", "")
            if field not in index.fields:
                index.fields[field] = []
            index.fields[field].append(index_field)
        return index


class Index:
    name: str | None
    fields: dict[str, list[IndexField]]

    def __init__(self):
        self.fields = {}

    def __repr__(self):
        return str(self.__dict__)


class IndexField:
    identifier: str
    attribute: str
    type: str
    sortable: bool

    def __init__(
        self, identifier: str, attribute: str, type: str, sortable: bool
    ):
        self.identifier = identifier
        self.attribute = attribute
        self.type = type
        self.sortable = sortable

    def __repr__(self):
        return str(self.__dict__)


class QueryHelper:
    @staticmethod
    def extract_where_fields(where, processor: ItemProcessor) -> list:
        fields = QueryProcessor.extract_filter_fields(
            where, processor.resolve_field
        )
        fields = [f"$.{field}" for field in fields]
        return fields

    @staticmethod
    def normalize_select_get(get_result):
        result = {}
        for k, v in get_result.items():
            if v is not None and len(v) > 0:
                JSONHelper.update_field(
                    result, k.replace("$.", ""), UpdateOp.PUT, v[0]
                )
        return result


class ResourceHelper:
    client: Any
    lib: Any

    def __init__(self, client: Any, lib: Any):
        self.client = client
        self.lib = lib

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
        lua = self.client.register_script(
            """return redis.call('del',
                '#', unpack(redis.call('keys', ARGV[1])))"""
        )
        lua(args=[f"{collection}:"])

    def list_collections(self, nargs) -> Any:
        return []

    def transact(self, ops: list[dict]) -> Any:
        nresult: list = []
        docs: list = []
        with self.client.pipeline() as pipe:
            try:
                # watch keys
                for op in ops:
                    args = op["args"]
                    if "name" in args:
                        key = args["name"]
                    elif "key" in args:
                        key = args["key"]
                    pipe.watch(key)
                # check conditions
                for op in ops:
                    func = op["func"]
                    args = op["args"]
                    converter = op["converter"]
                    processor = op["processor"]
                    doc = None
                    if op["op"] == StoreOperation.PUT:
                        if func == "helper":
                            ClientHelper.eval_condition(
                                pipe,
                                args["key"],
                                args["where"],
                                True,
                                processor,
                            )
                        else:
                            if "nx" in args:
                                if pipe.exists(args["name"]) == 1:
                                    raise ConflictError
                            if "xx" in args:
                                if pipe.exists(args["name"]) == 0:
                                    raise ConflictError
                    elif op["op"] == StoreOperation.UPDATE:
                        if not args["single_op"]:
                            if args["where"] is not None:
                                doc = ClientHelper.eval_condition(
                                    pipe,
                                    args["key"],
                                    args["where"],
                                    args["returning"] is None,
                                    processor,
                                )
                            elif args["returning"] is not None:
                                doc = pipe.json().get(args["key"])
                            else:
                                if pipe.exists(args["key"]) == 0:
                                    raise ConflictError
                    elif op["op"] == StoreOperation.DELETE:
                        if func == "helper":
                            ClientHelper.eval_condition(
                                pipe,
                                args["key"],
                                args["where"],
                                True,
                                processor,
                            )
                        else:
                            if pipe.exists(args["key"]) == 0:
                                raise ConflictError
                    docs.append(doc)
                # execute operations
                pipe.multi()
                for i in range(0, len(ops)):
                    op = ops[i]
                    doc = docs[i]
                    func = op["func"]
                    args = op["args"]
                    converter = op["converter"]
                    processor = op["processor"]
                    if op["op"] == StoreOperation.PUT:
                        if func == "set":
                            NCall(pipe.json().set, args).invoke()
                        elif func == "helper":
                            pipe.json().set(args["key"], "$", args["document"])
                        nresult.append(True)
                    elif op["op"] == StoreOperation.UPDATE:
                        if args["single_op"]:
                            call = converter.convert_update_op(
                                pipe, args["key"], args["update"].operations[0]
                            )
                            return call.invoke()
                        else:
                            calls = converter.convert_update_ops(
                                pipe, args["key"], args["update"]
                            )
                            for call in calls:
                                call.invoke()
                            if args["returning"] is None:
                                nresult.append(None)
                            elif args["returning"] is False:
                                nresult.append(doc)
                            else:
                                nresult.append(
                                    QueryProcessor.update_item(
                                        doc,
                                        args["update"],
                                        processor.resolve_field,
                                    )
                                )
                    elif op["op"] == StoreOperation.DELETE:
                        if func == "delete":
                            NCall(pipe.json().delete, args).invoke()
                        elif func == "helper":
                            pipe.json().delete(args["key"])
                        nresult.append(True)
                pipe.execute()
            except self.lib.WatchError:
                raise ConflictError
            except PreconditionFailedError:
                raise ConflictError
        return nresult

    def close(self, nargs: Any) -> Any:
        pass


class AsyncResourceHelper:
    client: Any
    lib: Any

    def __init__(self, client: Any, lib: Any):
        self.client = client
        self.lib = lib

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
        lua = self.client.register_script(
            """return redis.call('del',
                '#', unpack(redis.call('keys', ARGV[1])))"""
        )
        await lua(args=[f"{collection}:"])

    async def list_collections(self, nargs) -> Any:
        return []

    async def transact(self, ops: list[dict]) -> Any:
        nresult: list = []
        docs: list = []
        async with self.client.pipeline() as pipe:
            try:
                # watch keys
                for op in ops:
                    args = op["args"]
                    if "name" in args:
                        key = args["name"]
                    elif "key" in args:
                        key = args["key"]
                    await pipe.watch(key)
                # check conditions
                for op in ops:
                    func = op["func"]
                    args = op["args"]
                    converter = op["converter"]
                    processor = op["processor"]
                    doc = None
                    if op["op"] == StoreOperation.PUT:
                        if func == "helper":
                            await AsyncClientHelper.eval_condition(
                                pipe,
                                args["key"],
                                args["where"],
                                True,
                                processor,
                            )
                        else:
                            if "nx" in args:
                                if await pipe.exists(args["name"]) == 1:
                                    raise ConflictError
                            if "xx" in args:
                                if await pipe.exists(args["name"]) == 0:
                                    raise ConflictError
                    elif op["op"] == StoreOperation.UPDATE:
                        if not args["single_op"]:
                            if args["where"] is not None:
                                doc = await AsyncClientHelper.eval_condition(
                                    pipe,
                                    args["key"],
                                    args["where"],
                                    args["returning"] is None,
                                    processor,
                                )
                            elif args["returning"] is not None:
                                doc = await pipe.json().get(args["key"])
                            else:
                                if await pipe.exists(args["key"]) == 0:
                                    raise ConflictError
                    elif op["op"] == StoreOperation.DELETE:
                        if func == "helper":
                            await AsyncClientHelper.eval_condition(
                                pipe,
                                args["key"],
                                args["where"],
                                True,
                                processor,
                            )
                        else:
                            if await pipe.exists(args["key"]) == 0:
                                raise ConflictError
                    docs.append(doc)
                # execute operations
                pipe.multi()
                for i in range(0, len(ops)):
                    op = ops[i]
                    doc = docs[i]
                    func = op["func"]
                    args = op["args"]
                    converter = op["converter"]
                    processor = op["processor"]
                    if op["op"] == StoreOperation.PUT:
                        if func == "set":
                            NCall(pipe.json().set, args).invoke()
                        elif func == "helper":
                            pipe.json().set(args["key"], "$", args["document"])
                        nresult.append(True)
                    elif op["op"] == StoreOperation.UPDATE:
                        if args["single_op"]:
                            call = converter.convert_update_op(
                                pipe, args["key"], args["update"].operations[0]
                            )
                            return call.invoke()
                        else:
                            calls = converter.convert_update_ops(
                                pipe, args["key"], args["update"]
                            )
                            for call in calls:
                                call.invoke()
                            if args["returning"] is None:
                                nresult.append(None)
                            elif args["returning"] is False:
                                nresult.append(doc)
                            else:
                                nresult.append(
                                    QueryProcessor.update_item(
                                        doc,
                                        args["update"],
                                        processor.resolve_field,
                                    )
                                )
                    elif op["op"] == StoreOperation.DELETE:
                        if func == "delete":
                            NCall(pipe.json().delete, args).invoke()
                        elif func == "helper":
                            pipe.json().delete(args["key"])
                        nresult.append(True)
                await pipe.execute()
            except self.lib.WatchError:
                raise ConflictError
            except PreconditionFailedError:
                raise ConflictError
        return nresult

    async def close(self, nargs: Any) -> Any:
        await self.client.aclose()


class ClientHelper:
    client: Any
    processor: ItemProcessor
    converter: OperationConverter
    lib: Any

    def __init__(
        self,
        client: Any,
        processor: ItemProcessor,
        converter: OperationConverter,
        lib: Any,
    ):
        self.client = client
        self.processor = processor
        self.converter = converter
        self.lib = lib

    def put(self, key, document, where) -> Any:
        with self.client.pipeline() as pipe:
            try:
                pipe.watch(key)
                ClientHelper.eval_condition(
                    pipe, key, where, True, self.processor
                )
                pipe.multi()
                pipe.json().set(key, "$", document)
                pipe.execute()
            except self.lib.WatchError:
                raise PreconditionFailedError
        return True

    def update(
        self,
        key,
        update: Update,
        where,
        returning: bool | None,
        single_op: bool,
    ) -> Any:
        if single_op:
            call = self.converter.convert_update_op(
                self.client, key, update.operations[0]
            )
            call.error_map = {self.lib.exceptions.ResponseError: NotFoundError}
            return call.invoke()
        with self.client.pipeline() as pipe:
            try:
                pipe.watch(key)
                if where is not None:
                    doc = ClientHelper.eval_condition(
                        pipe, key, where, returning is None, self.processor
                    )
                elif returning is not None:
                    doc = pipe.json().get(key)
                else:
                    if pipe.exists(key) == 0:
                        raise NotFoundError
                calls = self.converter.convert_update_ops(pipe, key, update)
                pipe.multi()
                for call in calls:
                    call.invoke()
                pipe.execute()
                if returning is None:
                    return None
                if returning is False:
                    return doc
                return QueryProcessor.update_item(
                    doc, update, self.processor.resolve_field
                )
            except self.lib.WatchError:
                raise PreconditionFailedError

    def delete(self, key, where) -> Any:
        with self.client.pipeline() as pipe:
            try:
                pipe.watch(key)
                ClientHelper.eval_condition(
                    pipe, key, where, True, self.processor
                )
                pipe.multi()
                pipe.json().delete(key)
                pipe.execute()
            except self.lib.WatchError:
                raise PreconditionFailedError
        return True

    def batch(self, ops: list) -> Any:
        with self.client.pipeline() as pipe:
            for op in ops:
                if op["op"] == StoreOperation.PUT:
                    pipe.json().set(**op["args"])
                else:
                    pipe.json().delete(**op["args"])
            pipe.execute()

    def close(self, nargs: Any) -> Any:
        pass

    @staticmethod
    def eval_condition(pipe, key, where, project_get: bool, processor) -> Any:
        if project_get:
            fields = QueryHelper.extract_where_fields(where, processor)
            get_result = pipe.json().get(key, *fields)
            if get_result is None:
                raise PreconditionFailedError
            if len(fields) == 1:
                get_result = {fields[0]: get_result}
            current_document = QueryHelper.normalize_select_get(get_result)
        else:
            current_document = pipe.json().get(key)
        if not QueryProcessor.eval_expr(
            current_document, where, processor.resolve_field
        ):
            raise PreconditionFailedError
        return current_document


class AsyncClientHelper:
    client: Any
    processor: ItemProcessor
    converter: OperationConverter
    lib: Any

    def __init__(
        self,
        client: Any,
        processor: ItemProcessor,
        converter: OperationConverter,
        lib: Any,
    ):
        self.client = client
        self.processor = processor
        self.converter = converter
        self.lib = lib

    async def put(self, key, document, where) -> Any:
        async with self.client.pipeline() as pipe:
            try:
                await pipe.watch(key)
                await AsyncClientHelper.eval_condition(
                    pipe, key, where, True, self.processor
                )
                pipe.multi()
                pipe.json().set(key, "$", document)
                await pipe.execute()
            except self.lib.WatchError:
                raise PreconditionFailedError
        return True

    async def update(
        self,
        key,
        update: Update,
        where,
        returning: bool | None,
        single_op: bool,
    ) -> Any:
        if single_op:
            call = self.converter.convert_update_op(
                self.client, key, update.operations[0]
            )
            call.error_map = {self.lib.exceptions.ResponseError: NotFoundError}
            return await call.ainvoke()
        async with self.client.pipeline() as pipe:
            try:
                await pipe.watch(key)
                if where is not None:
                    doc = await AsyncClientHelper.eval_condition(
                        pipe, key, where, returning is None, self.processor
                    )
                elif returning is not None:
                    doc = await pipe.json().get(key)
                else:
                    if await pipe.exists(key) == 0:
                        raise NotFoundError
                calls = self.converter.convert_update_ops(pipe, key, update)
                pipe.multi()
                for call in calls:
                    call.invoke()
                await pipe.execute()
                if returning is None:
                    return None
                if returning is False:
                    return doc
                return QueryProcessor.update_item(
                    doc, update, self.processor.resolve_field
                )
            except self.lib.WatchError:
                raise PreconditionFailedError

    async def delete(self, key, where) -> Any:
        async with self.client.pipeline() as pipe:
            try:
                await pipe.watch(key)
                await AsyncClientHelper.eval_condition(
                    pipe, key, where, True, self.processor
                )
                pipe.multi()
                pipe.json().delete(key)
                await pipe.execute()
            except self.lib.WatchError:
                raise PreconditionFailedError
        return True

    async def batch(self, ops: list) -> Any:
        async with self.client.pipeline() as pipe:
            for op in ops:
                if op["op"] == StoreOperation.PUT:
                    pipe.json().set(**op["args"])
                else:
                    pipe.json().delete(**op["args"])
            await pipe.execute()

    async def close(self, nargs: Any) -> Any:
        await self.client.close()

    @staticmethod
    async def eval_condition(
        pipe, key, where, project_get: bool, processor
    ) -> Any:
        if project_get:
            fields = QueryHelper.extract_where_fields(where, processor)
            get_result = await pipe.json().get(key, *fields)
            if get_result is None:
                raise PreconditionFailedError
            if len(fields) == 1:
                get_result = {fields[0]: get_result}
            current_document = QueryHelper.normalize_select_get(get_result)
        else:
            current_document = await pipe.json().get(key)
        if not QueryProcessor.eval_expr(
            current_document, where, processor.resolve_field
        ):
            raise PreconditionFailedError
        return current_document


class RedisCollection:
    name: str
    client: Any
    helper: Any
    lib: Any
    converter: OperationConverter
    processor: ItemProcessor
    field_types: dict | None

    def __init__(
        self,
        name: str,
        client: Any,
        helper_type: Any,
        lib: Any,
        id_map_field: str | None,
        pk_map_field: str | None,
        etag_embed_field: str | None,
        suppress_fields: list[str] | None,
        field_types: dict | None,
        indexes: list,
    ) -> None:
        self.name = name
        self.client = client
        self.lib = lib
        self.processor = ItemProcessor(
            etag_embed_field=etag_embed_field,
            id_map_field=id_map_field,
            pk_map_field=pk_map_field,
            local_etag=True,
            suppress_fields=suppress_fields,
            field_types=field_types,
        )
        index_manager = IndexManager(name, indexes)
        self.converter = OperationConverter(
            self.processor, index_manager, name
        )
        self.helper = helper_type(
            client, self.processor, self.converter, self.lib
        )
