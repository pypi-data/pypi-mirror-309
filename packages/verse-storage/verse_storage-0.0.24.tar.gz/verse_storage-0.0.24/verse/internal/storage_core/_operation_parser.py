from __future__ import annotations

import json
from datetime import datetime
from typing import IO, Any

from verse.core import Operation, OperationParser
from verse.core.exceptions import BadRequestError
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
    Parameter,
    QLParser,
    Select,
    Update,
    UpdateOp,
    UpdateOperation,
    Value,
)

from ._attributes import (
    Attribute,
    KeyAttribute,
    SpecialAttribute,
    UpdateAttribute,
)
from ._functions import StoreFunctionName
from ._models import (
    ArrayIndex,
    AscIndex,
    BaseIndex,
    CompositeIndex,
    DescIndex,
    FieldIndex,
    GeospatialIndex,
    HashIndex,
    Index,
    MatchCondition,
    RangeIndex,
    SparseVectorIndex,
    TextIndex,
    TTLIndex,
    VectorIndex,
    WildcardIndex,
)
from ._operation import StoreOperation


class StoreOperationParser(OperationParser):
    ARG_STATEMENT = "statement"
    ARG_SELECT = "select"
    ARG_COLLECTION = "collection"
    ARG_SET = "set"
    ARG_WHERE = "where"
    ARG_ORDER_BY = "order_by"
    ARG_SEARCH = "search"

    _ql_cache: dict[Any, Any]
    operation_parsers: list[StoreOperationParser] | None

    def __init__(self, operation: Operation | None):
        super().__init__(operation)
        self._ql_cache = dict()
        self.operation_parsers = None
        if self.op_equals(StoreOperation.EXECUTE):
            super().__init__(self.parse_statement())

    def is_single_op(self) -> bool:
        operations = self.get_arg("operations")
        return operations is None

    def is_resource_op(self) -> bool:
        if self.get_name() in [
            StoreOperation.CREATE_COLLECTION,
            StoreOperation.DROP_COLLECTION,
            StoreOperation.LIST_COLLECTIONS,
            StoreOperation.CLOSE,
        ]:
            return True
        return False

    def is_collection_op(self) -> bool:
        if self.get_name() in [
            StoreOperation.GET,
            StoreOperation.PUT,
            StoreOperation.UPDATE,
            StoreOperation.DELETE,
            StoreOperation.QUERY,
            StoreOperation.COUNT,
            StoreOperation.BATCH,
            StoreOperation.TRANSACT,
            StoreOperation.WATCH,
            StoreOperation.CREATE_INDEX,
            StoreOperation.DROP_INDEX,
            StoreOperation.LIST_INDEXES,
        ]:
            return True
        return False

    def parse_statement(self) -> Operation:
        operation = self.get_parsed_arg(StoreOperationParser.ARG_STATEMENT)
        if operation is None:
            raise BadRequestError("No operation found")
        params = self.get_params()
        operation = self.replace_operation_params(operation, params)
        if params is not None:
            operation.args["params"] = params
        return operation

    def get_params(self) -> dict[str, Any] | None:
        return self.get_arg("params")

    def get_operations(self) -> list[Operation]:
        return self.get_arg("operations")

    def get_operation_parsers(self) -> list[StoreOperationParser]:
        if self.operation_parsers is None:
            self.operation_parsers = []
            for operation in self.get_operations():
                params = self.get_params()
                if params is not None:
                    args: dict | None = {"params": params}
                    if operation.args is not None and args is not None:
                        args = operation.args | args
                else:
                    args = operation.args
                self.operation_parsers.append(
                    StoreOperationParser(
                        self.replace_operation_params(
                            Operation(name=operation.name, args=args), params
                        )
                    )
                )
        return self.operation_parsers

    def get_index(self) -> Index:
        index = self.get_arg("index")
        if index is None:
            raise BadRequestError("Index parameter missing")
        if isinstance(index, BaseIndex):
            return index
        type_map: dict = {
            "field": FieldIndex,
            "range": RangeIndex,
            "hash": HashIndex,
            "composite": CompositeIndex,
            "asc": AscIndex,
            "desc": DescIndex,
            "array": ArrayIndex,
            "ttl": TTLIndex,
            "text": TextIndex,
            "geospatial": GeospatialIndex,
            "vector": VectorIndex,
            "sparse_vector": SparseVectorIndex,
            "wildcard": WildcardIndex,
        }
        if isinstance(index, dict):
            if "type" in index and index["type"] in type_map:
                type = type_map[index["type"]]
                return type.from_dict(index)
        raise BadRequestError("Index format error")

    def get_key(self) -> Value:
        return self.get_arg("key", True)

    def get_id_from_key(self, key: Value) -> Value:
        if key is not None:
            if isinstance(key, (str, int, float, bool)):
                return key
            if isinstance(key, dict) and KeyAttribute.ID in key:
                return key[KeyAttribute.ID]
        return None

    def get_id(self) -> Value:
        return self.get_id_from_key(self.get_key())

    def get_id_as_str(self) -> str:
        id = self.get_id()
        if not isinstance(id, str):
            raise BadRequestError("id is not string")
        return id

    def get_expiry(self) -> int | None:
        return self.get_arg("expiry")

    def get_method(self) -> str | None:
        return self.get_arg("method")

    def get_id_as_str_or_none(self) -> str | None:
        id = self.get_id()
        if id is None:
            return None
        if not isinstance(id, str):
            raise BadRequestError("id is not string")
        return id

    def get_version_from_key(self, key: Value) -> str | None:
        if key is not None:
            if isinstance(key, dict) and KeyAttribute.VERSION in key:
                return key[KeyAttribute.VERSION]
        return None

    def get_version(self) -> str | None:
        return self.get_version_from_key(self.get_key())

    def get_label(self) -> str | None:
        key = self.get_key()
        if key is not None:
            if isinstance(key, dict) and KeyAttribute.LABEL in key:
                return key[KeyAttribute.LABEL]
        return None

    def get_source(self) -> Value:
        return self.get_arg("source", True)

    def get_source_collection(self) -> str | None:
        source = self.get_source()
        if isinstance(source, dict):
            if "collection" in source:
                return source["collection"]
        return None

    def get_source_key(self) -> Value:
        source = self.get_source()
        if isinstance(source, dict):
            if Attribute.KEY in source:
                return source[Attribute.KEY]
        return source

    def get_source_id_as_str(self) -> str:
        source = self.get_source()
        if isinstance(source, str):
            return source
        elif isinstance(source, dict) and Attribute.KEY in source:
            id = self.get_id_from_key(source[Attribute.KEY])
            if isinstance(id, str):
                return id
        raise BadRequestError("id is not string")

    def get_source_version(self) -> str | None:
        return self.get_version_from_key(self.get_source_key())

    def get_attribute(self) -> str:
        attr = self.get_arg("attr")
        if attr is not None:
            return attr
        return Attribute.VALUE

    def is_attribute(self, attribute: str) -> bool:
        return attribute.lower() == self.get_attribute().lower()

    def is_value_attribute(self) -> bool:
        return self.is_attribute(Attribute.VALUE)

    def is_metadata_attribute(self) -> bool:
        return self.is_attribute(Attribute.METADATA)

    def is_properties_attribute(self) -> bool:
        return self.is_attribute(Attribute.PROPERTIES)

    def is_versions_attribute(self) -> bool:
        return self.is_attribute(Attribute.VERSIONS)

    def get_filter(self) -> dict | None:
        return self.get_arg("filter")

    def get_select(self) -> Select | None:
        return self.get_parsed_arg(StoreOperationParser.ARG_SELECT)

    def get_collection_name(self) -> str | None:
        collection = self.get_arg("collection")
        if isinstance(collection, str):
            return collection
        collection = self.get_parsed_arg(StoreOperationParser.ARG_COLLECTION)
        if collection is None:
            return None
        return collection.name

    def get_value(self) -> Any:
        return self.get_arg("value", True)

    def get_value_as_bytes(self) -> bytes | None:
        value = self.get_value()
        if value is None:
            return None
        if isinstance(value, bytes):
            return value
        return json.dumps(value).encode()

    def get_file(self) -> str | None:
        return self.get_arg("file")

    def get_url(self) -> str | None:
        return self.get_arg("url")

    def get_stream(self) -> IO | None:
        return self.get_arg("stream")

    def get_start(self) -> int | None:
        return self.get_arg("start")

    def get_end(self) -> int | None:
        return self.get_arg("end")

    def get_vector_value(self) -> dict:
        value = self.get_value()
        if isinstance(value, list):
            return {"vector": value}
        if isinstance(value, dict):
            return value
        raise BadRequestError("Vector value must be list or dict")

    def get_metadata(self) -> dict | None:
        return self.get_arg("metadata")

    def get_properties(self) -> dict | None:
        return self.get_arg("properties")

    def get_set(self) -> Update:
        set = self.get_parsed_arg(StoreOperationParser.ARG_SET)
        return set

    def get_update_attribute(self) -> str:
        set = self.get_parsed_arg(StoreOperationParser.ARG_SET)
        if len(set.operations) == 1:
            return set.operations[0].field
        raise BadRequestError("Invalid number of update attributes")

    def is_value_update(self) -> bool:
        attribute = self.get_update_attribute()
        return attribute.lower() == UpdateAttribute.VALUE

    def is_metadata_update(self) -> bool:
        attribute = self.get_update_attribute()
        return attribute.lower() == UpdateAttribute.METADATA

    def is_properties_update(self) -> bool:
        attribute = self.get_update_attribute()
        return attribute.lower() == UpdateAttribute.PROPERTIES

    def get_updated_value(self) -> Any:
        set = self.get_parsed_arg(StoreOperationParser.ARG_SET)
        for operation in set.operations:
            if operation.field == UpdateAttribute.VALUE and (
                operation.op == UpdateOp.INSERT or operation.op == UpdateOp.PUT
            ):
                return operation.args[0]
        raise BadRequestError("Update value not found")

    def get_updated_metadata(self) -> dict | None:
        set = self.get_parsed_arg(StoreOperationParser.ARG_SET)
        for operation in set.operations:
            if operation.field == UpdateAttribute.METADATA and (
                operation.op == UpdateOp.INSERT or operation.op == UpdateOp.PUT
            ):
                return operation.args[0]
        raise BadRequestError("Update metadata not found")

    def get_updated_properities(self) -> dict | None:
        set = self.get_parsed_arg(StoreOperationParser.ARG_SET)
        for operation in set.operations:
            if operation.field == UpdateAttribute.PROPERTIES and (
                operation.op == UpdateOp.INSERT or operation.op == UpdateOp.PUT
            ):
                return operation.args[0]
        raise BadRequestError("Update properties not found")

    def get_search_as_function(self) -> Function | None:
        funcs = self.get_search_as_functions()
        if funcs is None:
            return None
        if funcs is not None and len(funcs) > 1:
            raise BadRequestError("Multiple search functions found.")
        return funcs[0]

    def get_search_as_functions(self) -> list[Function] | None:
        def _get_functions(expr):
            if expr is None:
                return None
            funcs = []
            if isinstance(expr, Function):
                return [expr]
            elif isinstance(expr, And):
                funcs.extend(_get_functions(expr.lexpr))
                funcs.extend(_get_functions(expr.rexpr))
            else:
                raise BadRequestError(
                    f"Expression not support in search {expr}"
                )
            return funcs

        expr = self.get_search()
        return _get_functions(expr)

    def get_search(self) -> Expression | None:
        expr = self.get_parsed_arg(StoreOperationParser.ARG_SEARCH)
        return expr

    def get_where(self) -> Expression | None:
        expr = self.get_parsed_arg(StoreOperationParser.ARG_WHERE)
        return expr

    def get_where_expr_list(self) -> list[Expression]:
        conditions = []

        def parse_expr(expr):
            if expr is None:
                return
            if isinstance(expr, And):
                parse_expr(expr.lexpr)
                parse_expr(expr.rexpr)
            elif isinstance(expr, Or):
                raise BadRequestError("OR is not supported in WHERE")
            elif isinstance(expr, Not):
                raise BadRequestError("NOT is not supported in WHERE")
            else:
                conditions.append(expr)

        expr = self.get_parsed_arg(StoreOperationParser.ARG_WHERE)
        parse_expr(expr)
        return conditions

    def get_match_condition(self) -> MatchCondition:
        match_condition = MatchCondition()
        expr_list = self.get_where_expr_list()
        for expr in expr_list:
            field = None
            if isinstance(expr, Function):
                if (
                    expr.namespace == FunctionNamespace.BUILTIN
                    and expr.name == StoreFunctionName.EXISTS
                ):
                    match_condition.exists = True
                if (
                    expr.namespace == FunctionNamespace.BUILTIN
                    and expr.name == StoreFunctionName.NOT_EXISTS
                ):
                    match_condition.exists = False
            if isinstance(expr, Comparison):
                if isinstance(expr.lexpr, Field):
                    field = expr.lexpr.path
                    value = expr.rexpr
                elif isinstance(expr.rexpr, Field):
                    field = expr.rexpr.path
                    value = expr.lexpr
                if field == SpecialAttribute.ETAG and isinstance(value, str):
                    if expr.op == ComparisonOp.EQ:
                        match_condition.if_match = value
                    elif expr.op == ComparisonOp.NEQ:
                        match_condition.if_none_match = value
                if field == SpecialAttribute.VERSION and isinstance(
                    value, str
                ):
                    if expr.op == ComparisonOp.EQ:
                        match_condition.if_version_match = value
                    elif expr.op == ComparisonOp.NEQ:
                        match_condition.if_version_not_match = value
                if field == SpecialAttribute.MODIFIED and isinstance(
                    value, datetime
                ):
                    if expr.op in [ComparisonOp.GT, ComparisonOp.GTE]:
                        match_condition.if_modified_since = value
                    elif expr.op in [ComparisonOp.LT, ComparisonOp.LTE]:
                        match_condition.if_unmodified_since = value
        return match_condition

    def get_where_exists(self) -> bool | None:
        expr = self.get_parsed_arg(StoreOperationParser.ARG_WHERE)
        if expr is not None:
            exists = True
            if isinstance(expr, Not):
                expr = expr.expr
                exists = False
            if isinstance(expr, Function):
                if (
                    expr.namespace == FunctionNamespace.BUILTIN
                    and expr.name == StoreFunctionName.EXISTS
                ):
                    return exists
                if (
                    expr.namespace == FunctionNamespace.BUILTIN
                    and expr.name == StoreFunctionName.NOT_EXISTS
                ):
                    return not exists
        return None

    def get_where_etag(self) -> Any:
        expr = self.get_parsed_arg(StoreOperationParser.ARG_WHERE)
        if (
            expr is not None
            and isinstance(expr, Comparison)
            and expr.op == ComparisonOp.EQ
        ):
            if (
                isinstance(expr.lexpr, Field)
                and expr.lexpr.path == SpecialAttribute.ETAG
            ):
                return expr.rexpr
            elif (
                isinstance(expr.rexpr, Field)
                and expr.rexpr.path == SpecialAttribute.ETAG
            ):
                return expr.lexpr
        return None

    def get_order_by(self) -> OrderBy | None:
        return self.get_parsed_arg(StoreOperationParser.ARG_ORDER_BY)

    def get_limit(self) -> int | None:
        return self.get_arg("limit")

    def get_offset(self) -> int | None:
        return self.get_arg("offset")

    def get_returning(self) -> bool | None:
        return self.get_arg("returning")

    def get_continuation(self) -> str | None:
        return self.get_arg("continuation")

    def get_config(self) -> Any:
        return self.get_arg("config")

    def get_nflags(self) -> dict | None:
        return self.get_arg("nflags")

    def get_parsed_arg(self, arg: Any) -> Any:
        if arg in self._ql_cache:
            return self._ql_cache[arg]
        if arg == StoreOperationParser.ARG_STATEMENT:
            statement = self.get_arg("statement")
            parsed_arg: Any = QLParser.parse_statement(statement)
        if arg == StoreOperationParser.ARG_SELECT:
            select = self.get_arg("select")
            if not isinstance(select, str):
                return select
            parsed_arg = QLParser.parse_select(select)
        elif arg == StoreOperationParser.ARG_COLLECTION:
            collection = self.get_arg("collection")
            if not isinstance(collection, str):
                return collection
            parsed_arg = QLParser.parse_collection(collection)
        elif arg == StoreOperationParser.ARG_SET:
            set = self.get_arg("set")
            if not isinstance(set, str):
                parsed_arg = set
            else:
                parsed_arg = QLParser.parse_update(set)
            parsed_arg = self.replace_set_params(parsed_arg, self.get_params())
        elif arg == StoreOperationParser.ARG_SEARCH:
            search = self.get_arg("search")
            if not isinstance(search, str):
                parsed_arg = search
            else:
                parsed_arg = QLParser.parse_search(search)
            parsed_arg = self.replace_expr_params(
                parsed_arg, self.get_params()
            )
        elif arg == StoreOperationParser.ARG_WHERE:
            where = self.get_arg("where")
            if not isinstance(where, str):
                parsed_arg = where
            else:
                parsed_arg = QLParser.parse_where(where)
            parsed_arg = self.replace_expr_params(
                parsed_arg, self.get_params()
            )
        elif arg == StoreOperationParser.ARG_ORDER_BY:
            order_by = self.get_arg("order_by")
            if not isinstance(order_by, str):
                return order_by
            parsed_arg = QLParser.parse_order_by(order_by)
        self._ql_cache[arg] = parsed_arg
        return parsed_arg

    def replace_operation_params(
        self, operation: Operation, params: dict[str, Any] | None
    ) -> Operation:
        if params is None or len(params) == 0:
            return operation
        if operation.args is not None:
            args: dict = {}
            for key, value in operation.args.items():
                args[key] = self.replace_expr_params(value, params)
            return Operation(name=operation.name, args=args)
        return Operation(name=operation.name)

    def replace_set_params(
        self, set: Update, params: dict[str, Any] | None
    ) -> Update:
        if params is None or len(params) == 0:
            return set
        copy = Update()
        for operation in set.operations:
            copy.operations.append(
                UpdateOperation(
                    field=operation.field,
                    op=operation.op,
                    args=tuple(
                        [
                            self.replace_expr_params(arg, params)
                            for arg in operation.args
                        ]
                    ),
                )
            )
        return copy

    def replace_expr_params(self, expr, params: dict[str, Any] | None) -> Any:
        if params is None or len(params) == 0:
            return expr
        if isinstance(expr, list):
            return [self.replace_expr_params(i, params) for i in expr]
        if isinstance(expr, Parameter):
            if expr.name in params:
                return params[expr.name]
            else:
                raise BadRequestError(f"Parameter {expr.name} not found")
        if isinstance(expr, Comparison):
            return Comparison(
                lexpr=self.replace_expr_params(expr.lexpr, params),
                op=expr.op,
                rexpr=self.replace_expr_params(expr.rexpr, params),
            )

        if isinstance(expr, Function):
            args = None
            named_args = None
            if expr.args is not None:
                args = tuple(
                    self.replace_expr_params(arg, params) for arg in expr.args
                )
            if expr.named_args is not None:
                named_args = dict()
                for k, v in expr.named_args.items():
                    named_args[k] = self.replace_expr_params(v, params)

            return Function(
                namespace=expr.namespace,
                name=expr.name,
                args=args,
                named_args=named_args,
            )
        if isinstance(expr, And):
            return And(
                lexpr=self.replace_expr_params(expr.lexpr, params),
                rexpr=self.replace_expr_params(expr.rexpr, params),
            )
        if isinstance(expr, Or):
            return Or(
                lexpr=self.replace_expr_params(expr.lexpr, params),
                rexpr=self.replace_expr_params(expr.rexpr, params),
            )
        if isinstance(expr, Not):
            return Not(expr=self.replace_expr_params(expr.expr, params))
        return expr
