"""
Document Store on Amazon DynamoDB.
"""

from __future__ import annotations

__all__ = ["AmazonDynamoDB"]

import json
from decimal import Decimal
from typing import Any

import boto3
from botocore.exceptions import ClientError

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
from .._models import DocumentCollectionConfig, DocumentFieldType, DocumentItem


class AmazonDynamoDB(StoreProvider):
    collection: str | None
    table: str | None
    region_name: str | None
    profile_name: str | None
    aws_access_key_id: str | None
    aws_secret_access_key: str | None
    aws_session_token: str | None
    id_map_field: str | dict | None
    pk_map_field: str | dict | None
    etag_embed_field: str | dict | None
    suppress_fields: list[str] | None
    nparams: dict[str, Any]

    _resource: Any
    _collection_cache: dict[str, DynamoDBCollection]

    def __init__(
        self,
        table: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        id_map_field: str | dict | None = "id",
        pk_map_field: str | dict | None = "pk",
        etag_embed_field: str | dict | None = "_etag",
        suppress_fields: list[str] | None = None,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            table:
                DynamoDB table name mapped to document store collection.
            region_name:
                AWS region name.
            profile_name:
                AWS profile name.
            aws_access_key_id:
                AWS access key id.
            aws_secret_access_key:
                AWS secret access key.
            aws_session_token:
                AWS session token.
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
                Native parameters to boto3 client.
        """
        self.collection = table
        self.table = table
        self.region_name = region_name
        self.profile_name = profile_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.id_map_field = id_map_field
        self.pk_map_field = pk_map_field
        self.etag_embed_field = etag_embed_field
        self.suppress_fields = suppress_fields
        self.nparams = nparams

        self._resource = None
        self._collection_cache = dict()

    def init(self, context: Context | None = None) -> None:
        if self._resource is not None:
            return

        resource = None
        if self.profile_name is not None:
            resource = boto3.resource(
                "dynamodb",
                region_name=self.region_name,
                profile_name=self.profile_name,
                **self.nparams,
            )
        elif (
            self.aws_access_key_id is not None
            and self.aws_secret_access_key is not None
        ):
            resource = boto3.resource(
                "dynamodb",
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                **self.nparams,
            )
        else:
            resource = boto3.resource(
                "dynamodb",
                region_name=self.region_name,
                **self.nparams,
            )

        self._resource = resource
        self._conditional_check_failed_exception = (
            resource.meta.client.exceptions.ConditionalCheckFailedException
        )

    def _get_table_name(self, op_parser: StoreOperationParser) -> str | None:
        collection_name = (
            op_parser.get_operation_parsers()[0].get_collection_name()
            if op_parser.op_equals(StoreOperation.BATCH)
            else op_parser.get_collection_name()
        )
        table = (
            collection_name.split(".")[0]
            if collection_name is not None
            else self.collection
        )
        return table

    def _get_collections(
        self, op_parser: StoreOperationParser
    ) -> list[DynamoDBCollection]:
        if op_parser.is_resource_op():
            return []
        if op_parser.op_equals(StoreOperation.TRANSACT):
            collections: list[DynamoDBCollection] = []
            for single_op_parser in op_parser.get_operation_parsers():
                collections.extend(self._get_collections(single_op_parser))
            return collections
        table = self._get_table_name(op_parser)
        if table is None:
            raise BadRequestError("Collection name must be specified")
        if table in self._collection_cache:
            return [self._collection_cache[table]]
        client = self._resource.Table(table)
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field, table
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field, table
        )
        etag_embed_field = ParameterParser.get_collection_parameter(
            self.etag_embed_field, table
        )
        col = DynamoDBCollection(
            client,
            ClientHelper,
            id_map_field,
            pk_map_field,
            etag_embed_field,
            self.suppress_fields,
        )
        self._collection_cache[table] = col
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
            op_parser, collections, ResourceHelper(self._resource)
        )
        if ncall is None:
            return super().run(operation=operation, context=context)
        nresult, nerror = ncall.invoke(return_error=True)
        result = self._convert_nresult(
            nresult, nerror, state, op_parser, collections
        )
        return Response(result=result, native=dict(result=nresult, call=ncall))

    def _get_ncall(
        self,
        op_parser: StoreOperationParser,
        collections: list[DynamoDBCollection],
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
                "table": self._get_table_name(op_parser),
                "config": get_collection_config(op_parser),
                "nargs": nargs,
            }
            call = NCall(resource_helper.create_collection, args)
        # DROP COLLECTION
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            args = {
                "table": self._get_table_name(op_parser),
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
            call = NCall(client.get_item, args, nargs)
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            args, state = converter.convert_put(
                op_parser.get_key(),
                op_parser.get_value(),
                op_parser.get_where(),
                op_parser.get_where_exists(),
            )
            call = NCall(client.put_item, args, nargs)
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            args, state = converter.convert_update(
                op_parser.get_key(),
                op_parser.get_set(),
                op_parser.get_where(),
                op_parser.get_returning(),
            )
            call = NCall(client.update_item, args, nargs)
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            args = converter.convert_delete(
                op_parser.get_key(), op_parser.get_where()
            )
            call = NCall(client.delete_item, args, nargs)
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
            args["nargs"] = nargs
            call = NCall(helper.query, args, None)
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            args = converter.convert_count(
                where=op_parser.get_where(),
                collection=op_parser.get_collection_name(),
            )
            args["nargs"] = nargs
            call = NCall(helper.count, args, None)
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
        nerror: Any,
        state: dict | None,
        op_parser: StoreOperationParser,
        collections: list[DynamoDBCollection],
    ) -> Any:
        if len(collections) == 1:
            processor = collections[0].processor
        result: Any = None
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            exists = op_parser.get_where_exists()
            if nerror is not None:
                if (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "ResourceInUseException"
                ):
                    if exists is False:
                        raise ConflictError
                else:
                    raise nerror
            result = None
        # DROP COLLECTION
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            exists = op_parser.get_where_exists()
            if nerror is not None:
                if (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "ResourceNotFoundException"
                ):
                    if exists is True:
                        raise NotFoundError
                else:
                    raise nerror
            result = None
        # LIST COLLECTION
        elif op_parser.op_equals(StoreOperation.LIST_COLLECTIONS):
            if nerror is not None:
                raise nerror
            result = [t.name for t in nresult]
        # GET
        if op_parser.op_equals(StoreOperation.GET):
            if nerror is not None:
                raise nerror
            if "Item" not in nresult:
                raise NotFoundError
            document = self._convert_to_json_dict(nresult["Item"])
            result = build_item_from_value(
                processor=processor,
                value=document,
                include_value=True,
            )
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            if nerror is not None:
                if (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "ConditionalCheckFailedException"
                ):
                    if "Item" in nerror.response:
                        raise PreconditionFailedError
                    raise PreconditionFailedError
                raise nerror
            result = build_item_from_value(
                processor=processor,
                value=state["value"] if state is not None else None,
            )
        # UPDATE
        elif op_parser.op_equals(StoreOperation.UPDATE):
            where = op_parser.get_where()
            if nerror is not None:
                if (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "ConditionalCheckFailedException"
                ):
                    if "Item" in nerror.response:
                        raise PreconditionFailedError
                    if where is None:
                        raise NotFoundError
                    else:
                        raise PreconditionFailedError
                elif (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "ValidationException"
                    and "document path" in nerror.response["Error"]["Message"]
                ):
                    if where is None:
                        raise NotFoundError
                    else:
                        raise PreconditionFailedError
                raise nerror
            if "Attributes" in nresult:
                document = self._convert_to_json_dict(nresult["Attributes"])
                result = build_item_from_value(
                    processor=processor, value=document, include_value=True
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
            if nerror is not None:
                if (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "ConditionalCheckFailedException"
                ):
                    if "Item" in nerror.response:
                        raise PreconditionFailedError
                    if where is None:
                        raise NotFoundError
                    else:
                        raise PreconditionFailedError
                raise nerror
            result = None
        # QUERY
        elif op_parser.op_equals(StoreOperation.QUERY):
            if nerror is not None:
                raise nerror
            result = build_query_result(
                self._parse_query_response(
                    nresult,
                    processor,
                    op_parser.get_limit(),
                    op_parser.get_offset(),
                )
            )
        # COUNT
        elif op_parser.op_equals(StoreOperation.COUNT):
            if nerror is not None:
                raise nerror
            result = self._parse_count_response(nresult)
        # BATCH
        elif op_parser.op_equals(StoreOperation.BATCH):
            if nerror is not None:
                raise nerror
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
            if nerror is not None:
                if (
                    isinstance(nerror, ClientError)
                    and nerror.response["Error"]["Code"]
                    == "TransactionCanceledException"
                ):
                    raise ConflictError
                raise nerror
            result = []
            op_parsers = op_parser.get_operation_parsers()
            for i in range(0, len(op_parsers)):
                if state is not None:
                    st = state["values"][i]
                result.append(
                    self._convert_nresult(
                        {}, None, st, op_parsers[i], [collections[i]]
                    )
                )
        return result

    def _parse_query_response(
        self,
        responses: list,
        processor: ItemProcessor,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[DocumentItem]:
        documents = []
        for response in responses:
            if "Items" in response:
                for item in response["Items"]:
                    document = self._convert_to_json_dict(item)
                    documents.append(
                        build_item_from_value(
                            processor=processor,
                            value=document,
                            include_value=True,
                        )
                    )

        end = len(documents)
        start = 0
        if limit is not None:
            if offset is not None:
                start = offset
                end = start + limit
            else:
                end = limit
        return documents[start:end]

    def _parse_count_response(self, responses: list) -> int:
        count = 0
        for response in responses:
            if "Count" in response:
                count = response["Count"]
        return count

    def _convert_to_json_dict(self, document: dict) -> dict:
        class DecimalEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Decimal):
                    return int(obj) if obj % 1 == 0 else float(obj)
                return json.JSONEncoder.default(self, obj)

        return json.loads(json.dumps(document, cls=DecimalEncoder))


class ResourceHelper:
    resource: Any

    def __init__(self, resource: Any):
        self.resource = resource

    def create_collection(
        self,
        table: str,
        config: DocumentCollectionConfig | None,
        nargs: Any,
    ):
        def get_attribute_type(type: str) -> str:
            if type == DocumentFieldType.STRING:
                return "S"
            elif type == DocumentFieldType.NUMBER:
                return "N"
            raise BadRequestError("Field type not supported")

        attribute_definitions = []
        key_schema = []
        pk_field = (
            config.pk_field
            if config is not None and config.pk_field is not None
            else "pk"
        )
        pk_type = (
            config.pk_type
            if config is not None and config.pk_type is not None
            else DocumentFieldType.STRING
        )
        attribute_definitions.append(
            {
                "AttributeName": pk_field,
                "AttributeType": get_attribute_type(pk_type),
            }
        )
        key_schema.append({"AttributeName": pk_field, "KeyType": "HASH"})
        id_field = (
            config.id_field
            if config is not None and config.id_field is not None
            else "id"
        )
        id_type = (
            config.id_type
            if config is not None and config.id_type is not None
            else DocumentFieldType.STRING
        )
        attribute_definitions.append(
            {
                "AttributeName": id_field,
                "AttributeType": get_attribute_type(id_type),
            }
        )
        key_schema.append({"AttributeName": id_field, "KeyType": "RANGE"})
        args = {
            "TableName": table,
            "AttributeDefinitions": attribute_definitions,
            "KeySchema": key_schema,
            "BillingMode": "PAY_PER_REQUEST",
        }
        db_table = NCall(
            self.resource.create_table,
            args,
            nargs,
        ).invoke()
        NCall(db_table.wait_until_exists, None, nargs).invoke()

    def drop_collection(self, table: str, nargs: Any):
        NCall(
            self.resource.meta.client.delete_table, {"TableName": table}, nargs
        ).invoke()
        waiter = NCall(
            self.resource.meta.client.get_waiter, ["table_not_exists"], nargs
        ).invoke()
        NCall(waiter.wait, {"TableName": table}, nargs).invoke()

    def list_collections(self, nargs) -> Any:
        response = NCall(self.resource.tables.all, None, nargs).invoke()
        return response

    def transact(self, ops: list[dict]) -> Any:
        nresult = self.resource.meta.client.transact_write_items(
            TransactItems=ops
        )
        return nresult

    def close(self, nargs: Any) -> Any:
        pass


class ClientHelper:
    client: Any

    def __init__(self, client: Any) -> None:
        self.client = client

    def query(self, query: Query, nargs: Any) -> Any:
        call = self._get_query_plan(query, nargs)
        return self._execute_query(call)

    def count(self, query: Query, nargs: Any) -> Any:
        call = self._get_query_plan(query, nargs)
        return self._execute_query(call)

    def batch(self, ops: list[dict]) -> Any:
        with self.client.batch_writer() as batch:
            for op in ops:
                if op["id"] == StoreOperation.PUT:
                    batch.put_item(Item=op["args"]["Item"])
                elif op["id"] == StoreOperation.DELETE:
                    batch.delete_item(Key=op["args"]["Key"])

    def _get_query_plan(self, query: Query, nargs: Any) -> NCall:
        args: dict[str, Any] = {}
        if query.index_name is not None and "." in query.index_name:
            splits = query.index_name.split(".")
            args["IndexName"] = splits[1]
            args["TableName"] = splits[0]
        if query.select is not None:
            args["Select"] = query.select
        if query.projection_expression is not None:
            args["ProjectionExpression"] = query.projection_expression
        if query.key_condition_expression is not None:
            args["KeyConditionExpression"] = query.key_condition_expression
        if query.filter_expression is not None:
            args["FilterExpression"] = query.filter_expression
        if (
            query.expression_attribute_names is not None
            and len(query.expression_attribute_names) > 0
        ):
            args["ExpressionAttributeNames"] = query.expression_attribute_names
        if (
            query.expression_attribute_values is not None
            and len(query.expression_attribute_values) > 0
        ):
            args["ExpressionAttributeValues"] = (
                query.expression_attribute_values
            )
        if query.scan_index_forward is not None:
            args["ScanIndexForward"] = query.scan_index_forward

        limit: int | None = None
        if query.limit is not None:
            if query.offset is not None:
                limit = query.limit + query.offset
            else:
                limit = query.limit
        if limit is not None:
            args["Limit"] = limit

        if query.action == IndexManager.ACTION_QUERY:
            return NCall(self.client.query, args, nargs)
        return NCall(self.client.scan, args, nargs)

    def _execute_query(self, call: NCall) -> Any:
        responses = []
        last_evaluated_key = None
        count = 0
        limit = call.get_arg("Limit")
        while True:
            if last_evaluated_key is not None:
                call.set_arg("ExclusiveStartKey", last_evaluated_key)
            response: dict | None = None
            response = call.invoke()
            responses.append(response)
            if response is not None and "LastEvaluatedKey" in response:
                last_evaluated_key = response["LastEvaluatedKey"]
            else:
                last_evaluated_key = None
            if response is not None and "Count" in response:
                count = count + response["Count"]
            if last_evaluated_key is None:
                break
            if limit is not None and count >= limit:
                break
        return responses


class OperationConverter:
    processor: ItemProcessor
    index_manager: IndexManager

    def __init__(self, processor: ItemProcessor, index_manager: IndexManager):
        self.processor = processor
        self.index_manager = index_manager

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
                args, state = converter.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append({"Put": args})
                states.append(state)
            elif op_parser.op_equals(StoreOperation.UPDATE):
                args, state = converter.convert_update(
                    op_parser.get_key(),
                    op_parser.get_set(),
                    op_parser.get_where(),
                    op_parser.get_returning(),
                )
                if "ReturnValues" in args:
                    # ReturnValues not supported in update
                    args.pop("ReturnValues")
                ops.append({"Update": args})
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args = converter.convert_delete(
                    op_parser.get_key(), op_parser.get_where()
                )
                ops.append({"Delete": args})
                states.append(None)
        return {"ops": ops}, {"values": states}

    def convert_batch(
        self, op_parsers: list[StoreOperationParser]
    ) -> tuple[dict, dict]:
        ops: list = []
        states: list = []
        for op_parser in op_parsers:
            if op_parser.op_equals(StoreOperation.PUT):
                args, state = self.convert_put(
                    op_parser.get_key(),
                    op_parser.get_value(),
                    op_parser.get_where(),
                    op_parser.get_where_exists(),
                )
                ops.append({"id": StoreOperation.PUT, "args": args})
                states.append(state)
            elif op_parser.op_equals(StoreOperation.DELETE):
                args = self.convert_delete(
                    op_parser.get_key(), op_parser.get_where()
                )
                ops.append({"id": StoreOperation.DELETE, "args": args})
                states.append(None)
        return {"ops": ops}, {"values": states}

    def convert_get(self, key: Value) -> dict:
        dbkey = self.processor.get_key_from_key(key=key)
        return {"Key": dbkey}

    def convert_put(
        self,
        key: Value,
        value: dict,
        where: Expression | None,
        exists: bool | None,
    ) -> tuple[dict, dict | None]:
        document = self.processor.add_embed_fields(value, key)
        document = json.loads(json.dumps(document), parse_float=Decimal)
        args: dict = {
            "TableName": self.index_manager.table_name,
            "Item": document,
        }
        if where is None:
            pass
        elif exists is False:
            condition_expression = (
                f"attribute_not_exists({self.processor.id_embed_field})"
            )
            args = args | {"ConditionExpression": condition_expression}
        elif exists is True:
            condition_expression = (
                f"attribute_exists({self.processor.id_embed_field})"
            )
            args = args | {"ConditionExpression": condition_expression}
        elif where is not None:
            attribute_names: dict[str, str] = {}
            attribute_values: dict[str, Any] = {}
            condition_expression = f"""
                attribute_exists({self.processor.id_embed_field}) and {
                self.convert_expr(
                where, attribute_names, attribute_values)}"""
            args = args | {
                "ConditionExpression": condition_expression,
                "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
            }
            if len(attribute_names) > 0:
                args["ExpressionAttributeNames"] = attribute_names
            if len(attribute_values) > 0:
                args["ExpressionAttributeValues"] = attribute_values
        return args, {"value": document}

    def convert_update(
        self,
        key: Value,
        set: Update,
        where: Expression | None,
        returning: bool | None,
    ) -> tuple[dict, dict | None]:
        state = None
        dbkey = self.processor.get_key_from_key(key=key)
        if self.processor.needs_local_etag():
            etag = self.processor.generate_etag()
            set = self.processor.add_etag_update(set, etag)
            state = {"etag": etag}
        attribute_names: dict = {}
        attribute_values: dict = {}
        update_expression = self.convert_update_ops(
            set, attribute_names, attribute_values
        )
        args = {
            "TableName": self.index_manager.table_name,
            "Key": dbkey,
            "UpdateExpression": update_expression,
            "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
        }
        if returning is True:
            args = args | {"ReturnValues": "ALL_NEW"}
        elif returning is False:
            args = args | {"ReturnValues": "ALL_OLD"}
        if where is not None:
            condition_expression = self.convert_expr(
                where, attribute_names, attribute_values
            )
        else:
            condition_expression = (
                f"attribute_exists({self.processor.id_embed_field})"
            )
        args["ConditionExpression"] = condition_expression
        if len(attribute_names) > 0:
            args["ExpressionAttributeNames"] = attribute_names
        if len(attribute_values) > 0:
            args["ExpressionAttributeValues"] = attribute_values
        return args, state

    def convert_delete(self, key: Value, where: Expression | None) -> dict:
        dbkey = self.processor.get_key_from_key(key=key)
        args = {
            "TableName": self.index_manager.table_name,
            "Key": dbkey,
            "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
        }
        if where is not None:
            attribute_names: dict = {}
            attribute_values: dict = {}
            condition_expression = self.convert_expr(
                where, attribute_names, attribute_values
            )
            args["ConditionExpression"] = condition_expression
            if len(attribute_names) > 0:
                args["ExpressionAttributeNames"] = attribute_names
            if len(attribute_values) > 0:
                args["ExpressionAttributeValues"] = attribute_values
        else:
            args["ConditionExpression"] = (
                f"""attribute_exists({self.processor.id_embed_field})"""
            )
        return args

    def convert_query(
        self,
        select: Select | None = None,
        where: Expression | None = None,
        order_by: OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | None = None,
    ) -> dict:
        explicit_index = self._get_explicit_index(collection)
        order_by_field = self._get_order_by_field(order_by)
        select_fields = self._get_select_fields(select)
        where_key_fields, where_non_key_fields = self._get_where_fields(where)
        query_plan = self.index_manager.get_query_plan(
            order_by_field,
            select_fields,
            where_key_fields,
            where_non_key_fields,
            explicit_index,
        )
        query = Query()
        query.action = query_plan.action
        query.index_name = explicit_index
        query.expression_attribute_names = {}
        query.expression_attribute_values = {}
        query.limit, query.offset = self.convert_limit_offset(limit, offset)
        query.select, query.projection_expression = self.convert_select(
            select, query.expression_attribute_names
        )
        if query_plan.action == IndexManager.ACTION_QUERY:
            query.index_name = query_plan.index.name
            if query.index_name == "$main":
                query.index_name = None
            ke, fe = self._split_key_filter_expression(where, query_plan.index)
            query.key_condition_expression = self.convert_expr(
                ke,
                query.expression_attribute_names,
                query.expression_attribute_values,
            )
            query.filter_expression = self.convert_expr(
                fe,
                query.expression_attribute_names,
                query.expression_attribute_values,
            )
            query.scan_index_forward = self.convert_order_by(order_by)
        elif query_plan.action == IndexManager.ACTION_SCAN:
            if where is not None:
                query.filter_expression = self.convert_expr(
                    where,
                    query.expression_attribute_names,
                    query.expression_attribute_values,
                )
        return {"query": query}

    def convert_count(
        self, where: Expression | None, collection: str | None
    ) -> dict:
        args = self.convert_query(where=where, collection=collection)
        args["query"].select = "COUNT"
        return args

    def convert_update_ops(
        self, update: Update, attribute_names, attribute_values
    ) -> str:
        sets: list[str] = []
        removes: list[str] = []
        adds: list[str] = []
        deletes: list[str] = []

        for operation in update.operations:
            field = self.convert_expr(
                Field(path=operation.field), attribute_names, attribute_values
            )
            if operation.op == UpdateOp.PUT:
                value = self.convert_expr(
                    operation.args[0], attribute_names, attribute_values
                )
                sets.append(f"{field} = {value}")
            elif operation.op == UpdateOp.INSERT:
                if field[-1] == "]":
                    value = self.convert_expr(
                        [operation.args[0]], attribute_names, attribute_values
                    )
                    if field.endswith("[-]"):
                        sets.append(
                            f"""{field[:-3]} = list_append({
                                field[:-3]}, {value})"""
                        )
                    elif field.endswith("[0]"):
                        sets.append(
                            f"""{field[:-3]} = list_append({
                                value}, {field[:-3]})"""
                        )
                    else:
                        raise BadRequestError(
                            "List update at intermediate index not supported"
                        )
                else:
                    value = self.convert_expr(
                        operation.args[0], attribute_names, attribute_values
                    )
                    sets.append(f"{field} = {value}")
            elif operation.op == UpdateOp.DELETE:
                removes.append(field)
            elif operation.op == UpdateOp.INCREMENT:
                val = operation.args[0]
                if operation.args[0] < 0:
                    val = -val
                    op = "-"
                else:
                    op = "+"
                value = self.convert_expr(
                    val, attribute_names, attribute_values
                )
                sets.append(f"{field} = {field} {op} {value}")
            elif operation.op == UpdateOp.MOVE:
                dest = self.convert_expr(
                    Field(path=operation.args[0].path),
                    attribute_names,
                    attribute_values,
                )
                sets.append(f"{dest} = {field}")
                removes.append(f"{field}")
            else:
                raise BadRequestError("Update operation not supported")

        expr = ""
        if len(sets) > 0:
            expr = f"{expr} SET {', '.join(e for e in sets)}"
        if len(removes) > 0:
            expr = f"{expr} REMOVE {', '.join(e for e in removes)}"
        if len(adds) > 0:
            expr = f"{expr} ADD {', '.join(e for e in adds)}"
        if len(deletes) > 0:
            expr = f"{expr} DELETE {', '.join(e for e in deletes)}"
        expr = expr.strip()
        return expr

    def convert_expr(
        self,
        expr: Expression | None,
        attribute_names: dict[str, str],
        attribute_values: dict[str, Any],
    ) -> str:
        if expr is None or isinstance(
            expr, (str, int, float, bool, dict, list)
        ):
            var = f":v{len(attribute_values)}"
            if isinstance(expr, float):
                attribute_values[var] = Decimal(str(expr))
            else:
                attribute_values[var] = expr
            return var
        if isinstance(expr, Field):
            field = self.processor.resolve_field(expr.path)
            field = (
                field.replace("[", "/")
                .replace("]", "")
                .replace(".", "/")
                .rstrip("/")
            )
            splits = field.split("/")
            alias = ""
            for split in splits:
                if split == "-" or split.isdigit():
                    alias = f"{alias}[{split}]"
                else:
                    var = f"#f{len(attribute_names)}"
                    attribute_names[var] = split
                    alias = f"{alias}.{var}" if alias != "" else var
            return alias
        if isinstance(expr, Function):
            return self.convert_func(expr, attribute_names, attribute_values)
        if isinstance(expr, Comparison):
            lhs = f"""{self.convert_expr(
                    expr.lexpr, attribute_names, attribute_values)}"""
            op = expr.op.value
            rhs = None
            negate = False
            if expr.op == ComparisonOp.NEQ:
                op = "<>"
            if expr.op == ComparisonOp.BETWEEN and isinstance(
                expr.rexpr, list
            ):
                rhs = f"""{self.convert_expr(
                    expr.rexpr[0], attribute_names, attribute_values)} AND {
                        self.convert_expr(
                    expr.rexpr[1], attribute_names, attribute_values)}"""
            elif (
                expr.op == ComparisonOp.IN or expr.op == ComparisonOp.NIN
            ) and isinstance(expr.rexpr, list):
                lst = ", ".join(
                    self.convert_expr(i, attribute_names, attribute_values)
                    for i in expr.rexpr
                )
                rhs = f"({lst})"
                if expr.op == ComparisonOp.NIN:
                    op = "IN"
                    negate = True
            else:
                rhs = self.convert_expr(
                    expr.rexpr, attribute_names, attribute_values
                )
            if negate:
                return f"""NOT {lhs} {op} {rhs}"""
            return f"""{lhs} {op} {rhs}"""
        if isinstance(expr, And):
            return f"""({self.convert_expr(
                expr.lexpr, attribute_names, attribute_values)} AND {
                    self.convert_expr(
                expr.rexpr, attribute_names, attribute_values)})"""
        if isinstance(expr, Or):
            return f"""({self.convert_expr(
                expr.lexpr, attribute_names, attribute_values)} OR {
                    self.convert_expr(
                expr.rexpr, attribute_names, attribute_values)})"""
        if isinstance(expr, Not):
            return f"""NOT {self.convert_expr(
                expr.expr, attribute_names, attribute_values)}"""
        return str(expr)

    def convert_func(
        self,
        expr: Function,
        attribute_names: dict[str, str],
        attribute_values: dict[str, Any],
    ) -> str:
        namespace = expr.namespace
        name = expr.name
        args = expr.args
        if namespace == FunctionNamespace.BUILTIN:
            if name == StoreFunctionName.IS_TYPE:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                type = args[1]
                if isinstance(type, str):
                    type = DocumentFieldType(type.lower())
                type_param = None
                if type == DocumentFieldType.STRING:
                    type_param = "S"
                elif type == DocumentFieldType.NUMBER:
                    type_param = "N"
                elif type == DocumentFieldType.BOOLEAN:
                    type_param = "BOOL"
                elif type == DocumentFieldType.OBJECT:
                    type_param = "M"
                elif type == DocumentFieldType.ARRAY:
                    type_param = "L"
                elif type == DocumentFieldType.NULL:
                    type_param = "NULL"
                value = self.convert_expr(
                    type_param, attribute_names, attribute_values
                )
                return f"attribute_type({field}, {value})"
            if name == StoreFunctionName.IS_DEFINED:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                return f"attribute_exists({field})"
            if name == StoreFunctionName.IS_NOT_DEFINED:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                return f"attribute_not_exists({field})"
            if name == StoreFunctionName.LENGTH:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                return f"size({field})"
            if name == StoreFunctionName.CONTAINS:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                value = self.convert_expr(
                    args[1], attribute_names, attribute_values
                )
                return f"contains({field}, {value})"
            if name == StoreFunctionName.STARTS_WITH:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                value = self.convert_expr(
                    args[1], attribute_names, attribute_values
                )
                return f"begins_with({field}, {value})"
            if name == StoreFunctionName.ARRAY_LENGTH:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                return f"size({field})"
            if name == StoreFunctionName.ARRAY_CONTAINS:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                value = self.convert_expr(
                    args[1], attribute_names, attribute_values
                )
                return f"contains({field}, {value})"
            if name == StoreFunctionName.ARRAY_CONTAINS_ANY:
                field = self.convert_expr(
                    args[0], attribute_names, attribute_values
                )
                clauses = []
                for item in args[1]:
                    value = self.convert_expr(
                        item, attribute_names, attribute_values
                    )
                    clauses.append(f"contains({field}, {value})")
                return f"({str.join(' OR ', clauses)})"
        raise BadRequestError(f"Function {name} not recognized")

    def convert_select(
        self,
        select: Select | None,
        attribute_names: dict[str, str],
    ) -> tuple[str | None, str | None]:
        if select is None or len(select.terms) == 0:
            return "ALL_ATTRIBUTES", None
        return "SPECIFIC_ATTRIBUTES", ", ".join(
            self.convert_expr(Field(path=t.field), attribute_names, {})
            for t in select.terms
        )

    def convert_order_by(self, order_by: OrderBy | None) -> bool | None:
        if order_by is not None and len(order_by.terms) > 0:
            if order_by.terms[0].direction is not None:
                return order_by.terms[0].direction == OrderByDirection.ASC
            else:
                return True
        return None

    def convert_limit_offset(
        self, limit: int | None = None, offset: int | None = None
    ) -> tuple[int | None, int | None]:
        return limit, offset

    def _get_explicit_index(self, collection: str | None) -> str | None:
        if collection is not None and "." in collection:
            return collection.split(".")[-1]
        return None

    def _get_order_by_field(self, order_by: OrderBy | None) -> str | None:
        order_by_field = None
        if order_by is not None and len(order_by.terms) > 0:
            order_by_field = self.processor.resolve_field(
                order_by.terms[0].field
            )
        return order_by_field

    def _get_select_fields(self, select: Select | None) -> list[str]:
        select_fields = []
        if select is not None:
            for term in select.terms:
                field = self.processor.resolve_field(term.field)
                select_fields.append(field)
        return select_fields

    def _get_where_fields(self, expr: Expression | None) -> tuple:
        key_fields: dict = {}
        non_key_fields: list = []
        self._find_where_fields(expr, key_fields, non_key_fields, False)
        for f in non_key_fields:
            if f in key_fields:
                key_fields.pop(f)
        return key_fields, non_key_fields

    def _find_where_fields(
        self,
        expr: Expression | None,
        key_fields: dict[str, list],
        non_key_fields: list[str],
        non_key: bool,
    ):
        def try_add_key_field(field, index_types):
            field = self.processor.resolve_field(field)
            if field in key_fields:
                # If field already exists, add to non-key
                # DynamoDB supports only one comparison
                add_non_key_field(field)
            else:
                key_fields[field] = index_types

        def add_non_key_field(field):
            field = self.processor.resolve_field(field)
            if field not in non_key_fields:
                non_key_fields.append(field)

        if isinstance(expr, Comparison):
            field = None
            if isinstance(expr.lexpr, Field):
                field = expr.lexpr.path
            elif isinstance(expr.rexpr, Field):
                field = expr.rexpr.path
            if field is None:
                return
            if non_key:
                add_non_key_field(field)
                return
            if expr.op == ComparisonOp.EQ:
                try_add_key_field(
                    field,
                    [
                        IndexManager.INDEX_TYPE_HASH,
                        IndexManager.INDEX_TYPE_RANGE,
                    ],
                )
            elif expr.op in [
                ComparisonOp.LT,
                ComparisonOp.LTE,
                ComparisonOp.GT,
                ComparisonOp.GTE,
                ComparisonOp.BETWEEN,
            ]:
                try_add_key_field(field, [IndexManager.INDEX_TYPE_RANGE])
            else:
                if field is not None:
                    add_non_key_field(field)
        elif isinstance(expr, Function):
            if (
                expr.namespace == FunctionNamespace.BUILTIN
                and expr.name == StoreFunctionName.STARTS_WITH
                and isinstance(expr.args[0], Field)
                and not non_key
            ):
                try_add_key_field(
                    expr.args[0].path, [IndexManager.INDEX_TYPE_RANGE]
                )
            else:
                for arg in expr.args:
                    if isinstance(arg, Field):
                        add_non_key_field(arg.path)
        elif isinstance(expr, And):
            self._find_where_fields(
                expr.lexpr, key_fields, non_key_fields, non_key
            )
            self._find_where_fields(
                expr.rexpr, key_fields, non_key_fields, non_key
            )
        elif isinstance(expr, Or):
            self._find_where_fields(
                expr.lexpr, key_fields, non_key_fields, True
            )
            self._find_where_fields(
                expr.rexpr, key_fields, non_key_fields, True
            )
        elif isinstance(expr, Not):
            self._find_where_fields(
                expr.expr, key_fields, non_key_fields, True
            )

    def _split_key_filter_expression(
        self,
        expr: Expression,
        index: Index,
    ) -> tuple[Expression, Expression]:
        def is_key_field(field):
            field = self.processor.resolve_field(field)
            if field == index.hash_key or field == index.range_key:
                return True
            return False

        if isinstance(expr, Comparison):
            field = None
            if isinstance(expr.lexpr, Field):
                field = expr.lexpr.path
            elif isinstance(expr.rexpr, Field):
                field = expr.rexpr.path
            if is_key_field(field):
                return expr, Comparison(
                    lexpr=True, op=ComparisonOp.EQ, rexpr=True
                )
            return None, expr
        elif isinstance(expr, Function):
            for arg in expr.args:
                if isinstance(arg, Field):
                    if is_key_field(arg.path):
                        return expr, Comparison(
                            lexpr=True, op=ComparisonOp.EQ, rexpr=True
                        )
            return None, expr
        elif isinstance(expr, (And, Or)):
            (
                ke_lhs,
                fe_lhs,
            ) = self._split_key_filter_expression(expr.lexpr, index)

            (
                ke_rhs,
                fe_rhs,
            ) = self._split_key_filter_expression(expr.rexpr, index)

            ke: Expression = None
            if ke_lhs is not None and ke_rhs is not None:
                ke = And(lexpr=ke_lhs, rexpr=ke_rhs)
            elif ke_lhs is not None:
                ke = ke_lhs
            elif ke_rhs is not None:
                ke = ke_rhs

            fe: Expression = (
                And(lexpr=fe_lhs, rexpr=fe_rhs)
                if isinstance(expr, And)
                else Or(lexpr=fe_lhs, rexpr=fe_rhs)
            )
            return ke, fe
        elif isinstance(expr, Not):
            ke, fe = self._split_key_filter_expression(expr.expr, index)
            return ke, Not(expr=expr.expr)
        return None, expr


class IndexManager:
    INDEX_CATEGORY_MAIN = "main"
    INDEX_CATEGORY_LOCAL = "local"
    INDEX_CATEGORY_GLOBAL = "global"

    INDEX_TYPE_HASH = "hash"
    INDEX_TYPE_RANGE = "range"

    ACTION_QUERY = "query"
    ACTION_SCAN = "scan"

    table_name: str
    hash_key: str
    range_key: str | None
    indexes: list[Index]

    def __init__(self, table):
        self.indexes = []
        self.table_name = table.table_name
        self.hash_key, self.range_key = self._parse_key_schema(
            key_schema=table.key_schema
        )
        self._add_indexes(table=table)

    def __str__(self):
        return f"[{', '.join(str(i) for i in self.indexes)}]"

    def get_id_pk_field(self) -> tuple:
        if self.range_key is None:
            return self.hash_key, self.hash_key
        return self.range_key, self.hash_key

    def get_query_plan(
        self,
        order_by_field: str | None,
        select_fields: list[str],
        where_key_fields: dict[str, list[str]],
        where_non_key_fields: list[str],
        explicit_index: str | None,
    ) -> QueryPlan:
        candidate_indexes = self._get_order_by_candidate_indexes(
            order_by_field, self.indexes
        )
        if order_by_field is not None and len(candidate_indexes) == 0:
            raise BadRequestError(
                f"No index found to order by {order_by_field}"
            )

        candidate_indexes = self._get_select_candidate_indexes(
            select_fields, candidate_indexes
        )
        if order_by_field is not None and len(candidate_indexes) == 0:
            raise BadRequestError(
                f"""No index found to order by {
                order_by_field} and get the select fields"""
            )

        candidate_indexes = self._get_where_candidate_indexes(
            where_key_fields, where_non_key_fields, candidate_indexes
        )
        if order_by_field is not None and len(candidate_indexes) == 0:
            raise BadRequestError(
                f"""No index found to order by {
                order_by_field} and filter by where condition"""
            )

        action = IndexManager.ACTION_SCAN
        index = self.indexes[0]
        if explicit_index is not None:
            match = False
            for candidate_index in candidate_indexes:
                if candidate_index.name == explicit_index:
                    action = IndexManager.ACTION_QUERY
                    index = candidate_index
                    match = True
                    break
            if order_by_field is not None and not match:
                raise BadRequestError(
                    f"""Provided index does not support the order by {
                    order_by_field} query"""
                )
            if not match:
                for db_index in self.indexes:
                    if db_index.name == explicit_index:
                        action = IndexManager.ACTION_SCAN
                        index = db_index
        else:
            if len(candidate_indexes) > 0:
                action = IndexManager.ACTION_QUERY
                index = candidate_indexes[0]

        query_plan = QueryPlan()
        query_plan.action = action
        query_plan.index = index
        return query_plan

    def _get_order_by_candidate_indexes(
        self,
        order_by_field: str | None,
        current_candidate_indexes: list[Index],
    ) -> list[Index]:
        candidate_indices = []
        for index in current_candidate_indexes:
            if order_by_field is None or index.range_key == order_by_field:
                candidate_indices.append(index)
        return candidate_indices

    def _get_select_candidate_indexes(
        self, select_fields: list[str], current_candidate_indexes: list[Index]
    ) -> list[Index]:
        candidate_indices: list[Index] = []
        for index in current_candidate_indexes:
            if index.projection_type == "ALL":
                # rank higher
                candidate_indices.insert(0, index)
            else:
                if len(select_fields) > 0:
                    match = True
                    for select_field in select_fields:
                        if select_field not in index.projection_fields:
                            match = False
                    if match:
                        # rank higher
                        candidate_indices.insert(0, index)
                    elif index.category == IndexManager.INDEX_CATEGORY_LOCAL:
                        # rank lower since will require extra reads
                        candidate_indices.append(index)

        return candidate_indices

    def _get_where_candidate_indexes(
        self,
        where_key_fields: dict[str, list[str]],
        where_non_key_fields: list[str],
        current_candidate_indexes: list[Index],
    ) -> list[Index]:
        candidate_indexes: list[Index] = []
        for index in reversed(current_candidate_indexes):
            if (
                index.hash_key in where_key_fields
                and IndexManager.INDEX_TYPE_HASH
                in where_key_fields[index.hash_key]
            ):
                if index.range_key is not None:
                    if index.range_key in where_key_fields:
                        # rank higher
                        candidate_indexes.insert(0, index)
                    if index.range_key not in where_non_key_fields:
                        # rank lower
                        candidate_indexes.append(index)
                else:
                    # rank lower
                    candidate_indexes.append(index)

        return candidate_indexes

    def _add_keys_to_projection(
        self, keys: list[str | None], projection_fields: list[str]
    ):
        for key in keys:
            if key is not None and key not in projection_fields:
                projection_fields.append(key)

    def _add_indexes(self, table):
        self.indexes.append(self._get_main_index())

        for index_category in [
            IndexManager.INDEX_CATEGORY_LOCAL,
            IndexManager.INDEX_CATEGORY_GLOBAL,
        ]:
            db_indexes = None
            if index_category == IndexManager.INDEX_CATEGORY_GLOBAL:
                db_indexes = table.local_secondary_indexes
            elif index_category == IndexManager.INDEX_CATEGORY_LOCAL:
                db_indexes = table.global_secondary_indexes
            if db_indexes is not None:
                for db_index in db_indexes:
                    index = self._parse_index(db_index)
                    index.category = index_category
                    if index.projection_type != "ALL":
                        self._add_keys_to_projection(
                            [
                                self.hash_key,
                                self.range_key,
                                index.hash_key,
                                index.range_key,
                            ],
                            index.projection_fields,
                        )
                    self.indexes.append(index)

    def _get_main_index(self) -> Index:
        index = Index()
        index.name = "$main"
        index.category = IndexManager.INDEX_CATEGORY_MAIN
        index.hash_key = self.hash_key
        index.range_key = self.range_key
        index.projection_type = "ALL"
        index.projection_fields = []
        return index

    def _parse_index(self, db_index: dict) -> Index:
        index = Index()
        index.name = f"{self.table_name}.{db_index['IndexName']}"
        index.hash_key, index.range_key = self._parse_key_schema(
            db_index["KeySchema"]
        )
        (
            index.projection_type,
            index.projection_fields,
        ) = self._parse_projection(db_index["Projection"])
        return index

    def _parse_key_schema(self, key_schema: list[dict]) -> tuple:
        hash_key = None
        range_key = None
        if len(key_schema) == 2:
            if key_schema[0]["KeyType"] == "HASH":
                hash_key = key_schema[0]["AttributeName"]
                range_key = key_schema[1]["AttributeName"]
            elif key_schema[0]["KeyType"] == "RANGE":
                hash_key = key_schema[1]["AttributeName"]
                range_key = key_schema[0]["AttributeName"]
        else:
            hash_key = key_schema[0]["AttributeName"]
        return hash_key, range_key

    def _parse_projection(self, projection: dict) -> tuple:
        projection_type = projection["ProjectionType"]
        projection_fields = []
        if projection_type == "INCLUDE":
            projection_fields = projection["NonKeyAttributes"]
        return projection_type, projection_fields


class Index:
    name: str | None
    hash_key: str
    range_key: str | None
    projection_type: str
    projection_fields: list[str]
    category: str

    def __repr__(self):
        return str(self.__dict__)


class QueryPlan:
    action: str
    index: Index


class Query:
    action: str = IndexManager.ACTION_SCAN
    index_name: str | None = None
    select: str | None = None
    projection_expression: str | None = None
    key_condition_expression: str | None = None
    filter_expression: str | None = None
    scan_index_forward: bool | None = None
    limit: int | None = None
    offset: int | None = None
    expression_attribute_values: dict[str, Any] = {}
    expression_attribute_names: dict[str, str] = {}

    def __repr__(self) -> str:
        return str(self.__dict__)


class DynamoDBCollection:
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
    ):
        self.client = client
        index_manager = IndexManager(table=client)
        id_embed_field, pk_embed_field = index_manager.get_id_pk_field()
        self.processor = ItemProcessor(
            id_embed_field=id_embed_field,
            pk_embed_field=pk_embed_field,
            etag_embed_field=etag_embed_field,
            id_map_field=id_map_field,
            pk_map_field=pk_map_field,
            local_etag=True,
            suppress_fields=suppress_fields,
        )
        self.converter = OperationConverter(self.processor, index_manager)
        self.helper = helper_type(client)
