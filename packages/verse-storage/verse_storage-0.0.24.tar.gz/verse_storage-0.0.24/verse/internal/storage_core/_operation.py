from __future__ import annotations

from typing import Any

from verse.core import Operation
from verse.ql import Collection, Expression, OrderBy, Select, Update, Value


class StoreOperation:
    EXECUTE = "execute"
    GET = "get"
    PUT = "put"
    UPDATE = "update"
    DELETE = "delete"
    QUERY = "query"
    COUNT = "count"
    BATCH = "batch"
    TRANSACT = "transact"
    COPY = "copy"
    GENERATE = "generate"
    WATCH = "watch"
    CLOSE = "close"

    CREATE_COLLECTION = "create_collection"
    DROP_COLLECTION = "drop_collection"
    LIST_COLLECTIONS = "list_collections"

    CREATE_INDEX = "create_index"
    DROP_INDEX = "drop_index"
    LIST_INDEXES = "list_indexes"

    @staticmethod
    def execute(
        statement: str,
        params: dict[str, Any] | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.EXECUTE, locals())

    @staticmethod
    def create_collection(
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.CREATE_COLLECTION, locals())

    @staticmethod
    def drop_collection(
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.DROP_COLLECTION, locals())

    @staticmethod
    def list_collections(
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.LIST_COLLECTIONS, locals())

    @staticmethod
    def get(
        key: Any = None,
        where: str | Expression | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.GET, locals())

    @staticmethod
    def put(
        key: Any = None,
        value: Value | None = None,
        where: str | Expression | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.PUT, locals())

    @staticmethod
    def update(
        key: Any = None,
        set: str | Update | None = None,
        where: str | Expression | None = None,
        returning: bool | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.UPDATE, locals())

    @staticmethod
    def delete(
        key: Any = None,
        where: str | Expression | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.DELETE, locals())

    @staticmethod
    def query(
        select: str | Select | None = None,
        search: str | Expression | None = None,
        where: str | Expression | None = None,
        order_by: str | OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.QUERY, locals())

    @staticmethod
    def count(
        search: str | Expression | None = None,
        where: str | Expression | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.COUNT, locals())

    @staticmethod
    def batch(
        operations: list[Operation],
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.BATCH, locals())

    @staticmethod
    def transact(
        operations: list[Operation],
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.TRANSACT, locals())

    @staticmethod
    def copy(
        key: Any = None,
        source: Value = None,
        where: str | Expression | None = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.COPY, locals())

    @staticmethod
    def generate(
        key: Any = None,
        collection: str | Collection | None = None,
        **kwargs,
    ):
        return Operation.normalize(StoreOperation.GENERATE, locals())

    @staticmethod
    def close(**kwargs):
        return Operation.normalize(StoreOperation.CLOSE, locals())
