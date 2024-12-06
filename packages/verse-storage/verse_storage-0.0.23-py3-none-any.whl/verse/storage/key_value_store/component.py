from typing import Any

from verse.core import Response
from verse.internal.storage_core import StoreComponent, StoreOperation
from verse.ql import Expression

from ._models import KeyValueItem, KeyValueKey, KeyValueList


class KeyValueStore(StoreComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(
        self,
        key: str | dict | KeyValueKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[KeyValueItem]:
        """Get value.

        Args:
            key: Key.

        Returns:
            KV item with value.

        Raises:
            NotFoundError: Key not found.
        """
        return self._run_internal(StoreOperation.GET, locals())

    def put(
        self,
        key: str | dict | KeyValueKey,
        value: str | bytes,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[KeyValueItem]:
        """Put value.

        Args:
            key: Key.
            value: Value.
            where: Condition expression.

        Returns:
            KV item.
        """
        return self._run_internal(StoreOperation.PUT, locals())

    def delete(
        self,
        key: str | dict | KeyValueKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete key.

        Args:
            key: Key.

        Returns:
           None

        Raises:
            NotFoundError: Key not found.
        """
        return self._run_internal(StoreOperation.DELETE, locals())

    def query(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[KeyValueList]:
        """Query items.

        Args:
            where: Condition expression.

        Returns:
            List of KV items.
        """
        return self._run_internal(StoreOperation.QUERY, locals())

    def count(
        self,
        where: str | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count items.

        Args:
            where: Condition expression.

        Returns:
            Count of KV items.
        """
        return self._run_internal(StoreOperation.COUNT, locals())

    async def aget(
        self,
        key: str | dict | KeyValueKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[KeyValueItem]:
        """Get value.

        Args:
            key: Key.

        Returns:
            KV item with value.

        Raises:
            NotFoundError: Key not found.
        """
        return await self._arun_internal(StoreOperation.GET, locals())

    async def aput(
        self,
        key: str | dict | KeyValueKey,
        value: str | bytes,
        where: str | Expression | None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[KeyValueItem]:
        """Put value.

        Args:
            key: Key.
            value: Value.
            where: Condition expression.

        Returns:
            KV item.
        """
        return await self._arun_internal(StoreOperation.PUT, locals())

    async def adelete(
        self,
        key: str | dict | KeyValueKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete key.

        Args:
            key: Key.

        Returns:
           None

        Raises:
            NotFoundError: Key not found.
        """
        return await self._arun_internal(StoreOperation.DELETE, locals())

    async def aquery(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[KeyValueList]:
        """Query items.

        Args:
            where: Condition expression.

        Returns:
            List of KV items.
        """
        return await self._arun_internal(StoreOperation.QUERY, locals())

    async def acount(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count items.

        Args:
            where: Condition expression.

        Returns:
            Count of KV items.
        """
        return await self._arun_internal(StoreOperation.COUNT, locals())

    async def aclose(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close the async client.

        Returns:
            None.
        """
        return await self._arun_internal(StoreOperation.CLOSE, locals())
