from typing import Any

from verse.core import Response
from verse.internal.storage_core import StoreComponent, StoreOperation
from verse.ql import Expression

from ._models import ConfigItem, ConfigKey, ConfigList


class ConfigStore(StoreComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(
        self,
        key: str | dict | ConfigKey,
        **kwargs: Any,
    ) -> Response[ConfigItem]:
        """Get config value.

        Args:
            key: Config key.

        Returns:
            Config item with value.

        Raises:
            NotFoundError: Key not found.
        """
        operation = StoreOperation.get(
            key=key,
            **kwargs,
        )
        return self.run(operation)

    def put(
        self,
        key: str | dict | ConfigKey,
        value: str,
        **kwargs: Any,
    ) -> Response[ConfigItem]:
        """Put config value.

        Args:
            key: Config key.
            value: Config value.

        Returns:
            Config item.
        """
        operation = StoreOperation.put(
            key=key,
            value=value,
            **kwargs,
        )
        return self.run(operation)

    def delete(
        self,
        key: str | dict | ConfigKey,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete config.

        Args:
            key: Config key.

        Returns:
           None

        Raises:
            NotFoundError: Key not found.
        """
        operation = StoreOperation.delete(
            key=key,
            **kwargs,
        )
        return self.run(operation)

    def query(
        self,
        where: str | Expression | None = None,
        **kwargs,
    ) -> Response[ConfigList]:
        """Query config.

        Args:
            where: Condition expression, defaults to None.

        Returns:
            List of config items.
        """
        operation = StoreOperation.query(
            where=where,
            **kwargs,
        )
        return self.run(operation)

    def count(
        self,
        where: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count config.

        Args:
            where: Condition expression, defaults to None.

        Returns:
            Count of config items.
        """
        operation = StoreOperation.count(
            where=where,
            **kwargs,
        )
        return self.run(operation)

    async def aget(
        self,
        key: str | dict | ConfigKey,
        **kwargs: Any,
    ) -> Response[ConfigItem]:
        """Get config value.

        Args:
            key: Config key.

        Returns:
            Config item with value.

        Raises:
            NotFoundError: Key not found.
        """
        operation = StoreOperation.get(
            key=key,
            **kwargs,
        )
        return await self.arun(operation)

    async def aput(
        self,
        key: str | dict | ConfigKey,
        value: str,
        **kwargs: Any,
    ) -> Response[ConfigItem]:
        """Put config value.

        Args:
            key: Config key.
            value: Config value.

        Returns:
            Config item.
        """
        operation = StoreOperation.put(
            key=key,
            value=value,
            **kwargs,
        )
        return await self.arun(operation)

    async def adelete(
        self,
        key: str | dict | ConfigKey,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete config.

        Args:
            key: Config key.

        Returns:
           None

        Raises:
            NotFoundError: Key not found.
        """
        operation = StoreOperation.delete(
            key=key,
            **kwargs,
        )
        return await self.arun(operation)

    async def aquery(
        self,
        where: str | Expression | None = None,
        **kwargs,
    ) -> Response[ConfigList]:
        """Query config.

        Args:
            where: Condition expression, defaults to None.

        Returns:
            List of config items.
        """
        operation = StoreOperation.query(
            where=where,
            **kwargs,
        )
        return await self.arun(operation)

    async def acount(
        self,
        where: str | Expression | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count config.

        Args:
            where: Condition expression, defaults to None.

        Returns:
            Count of config items.
        """
        operation = StoreOperation.count(
            where=where,
            **kwargs,
        )
        return await self.arun(operation)

    async def aclose(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close the async client.

        Returns:
            None.
        """
        operation = StoreOperation.close(
            **kwargs,
        )
        return await self.arun(operation)
