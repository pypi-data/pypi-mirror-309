from __future__ import annotations

from typing import Any

from verse.core import Operation, Response
from verse.internal.storage_core import (
    StoreComponent,
    StoreOperation,
    UpdateAttribute,
)
from verse.ql import Expression, OrderBy, Select, Update

from ._models import (
    VectorCollectionConfig,
    VectorItem,
    VectorKey,
    VectorList,
    VectorValue,
)


class VectorStore(StoreComponent):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

    def create_collection(
        self,
        collection: str | None = None,
        config: dict | VectorCollectionConfig | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Create collection.

        Args:
            collection:
                Collection name.
            config:
                Collection config.

        Returns:
            None.
        """
        operation = StoreOperation.create_collection(
            collection=collection,
            config=config,
            **kwargs,
        )
        return self.run(operation)

    def drop_collection(
        self,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Drop collection.

        Args:
            collection:
                Collection name.

        Returns:
            None.
        """
        operation = StoreOperation.drop_collection(
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def list_collections(
        self,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """List collections.

        Returns:
            List of collection names.
        """
        operation = StoreOperation.list_collections(
            **kwargs,
        )
        return self.run(operation)

    def get(
        self,
        key: str | dict | VectorKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Get vector.

        Args:
            key:
                Vector key.
            collection:
                Collection name.

        Returns:
            Vector item.

        Raises:
            NotFoundError:
                Vector not found.
        """
        operation = StoreOperation.get(
            key=key,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def put(
        self,
        key: str | dict | VectorKey,
        value: list[float] | dict | VectorValue,
        metadata: dict | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Put vector.

        Args:
            key:
                Vector key.
            value:
                Vector value.
            metadata:
                Custom metadata.
            collection:
                Collection name.

        Returns:
            Vector item.
        """
        operation = StoreOperation.put(
            key=key,
            value=value,
            metadata=metadata,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def update(
        self,
        key: str | dict | VectorKey,
        value: list[float] | dict | VectorValue,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Update vector value.

        Args:
            key:
                Vector key.
            value:
                Vector value.
            collection:
                Collection name.

        Returns:
            Vector item.
        """
        update = Update()
        update.put(UpdateAttribute.VALUE, value)
        operation = StoreOperation.update(
            key=key,
            set=update,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def update_metadata(
        self,
        key: str | dict | VectorKey,
        metadata: dict | None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Update vector metadata.

        Args:
            key:
                Vector key.
            metadata:
                Vector metadata.
            collection:
                Collection name.

        Returns:
            Vector item.
        """
        update = Update()
        update.put(UpdateAttribute.METADATA, metadata)
        operation = StoreOperation.update(
            key=key,
            set=update,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def delete(
        self,
        key: str | dict | VectorKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete vector.

        Args:
            key:
                Vector key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Vector not found.
            PreconditionFailedError:
                Condition failed.
        """
        operation = StoreOperation.delete(
            key=key,
            where=where,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def query(
        self,
        search: str | Expression | None = None,
        select: str | Select | None = None,
        where: str | Expression | None = None,
        order_by: str | OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[VectorList]:
        """Query vectors.

        Args:
            search:
                Search expression.
            select:
                Select expression.
            where:
                Condition expression.
            order_by:
                Order by expression.
            limit:
                Query limit.
            offset:
                Query offset.
            collection:
                Collection name.

        Returns:
            List of vectors.
        """
        operation = StoreOperation.query(
            select=select,
            search=search,
            where=where,
            order_by=order_by,
            limit=limit,
            offset=offset,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def count(
        self,
        search: str | Expression | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count vectors.

        Args:
            search:
                Search expression.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Vector count.
        """
        operation = StoreOperation.count(
            search=search,
            where=where,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def batch(
        self,
        operations: list[Operation],
        **kwargs,
    ) -> Response[list[Any]]:
        """Batch operation.

        Args:
            operations:
                List of operations.

        Returns:
            Batch operation results.
        """
        operation = StoreOperation.batch(
            operations=operations,
            **kwargs,
        )
        return self.run(operation)

    def transact(
        self,
        operations: list[Operation],
        **kwargs,
    ) -> Response[list[Any]]:
        """Execute transaction.

        Args:
            operations:
                List of operations.

        Returns:
            Transaction results.

        Raises:
            ConflictError:
                Transaction failed.
        """
        operation = StoreOperation.transact(
            operations=operations,
            **kwargs,
        )
        return self.run(operation)

    def close(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close the sync client.

        Returns:
            None.
        """
        operation = StoreOperation.close(
            **kwargs,
        )
        return self.run(operation)

    async def acreate_collection(
        self,
        collection: str | None = None,
        config: dict | VectorCollectionConfig | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Create collection.

        Args:
            collection:
                Collection name.
            config:
                Collection config.

        Returns:
            None.
        """
        operation = StoreOperation.create_collection(
            collection=collection,
            config=config,
            **kwargs,
        )
        return await self.arun(operation)

    async def adrop_collection(
        self,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Drop collection.

        Args:
            collection:
                Collection name.

        Returns:
            None.
        """
        operation = StoreOperation.drop_collection(
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def alist_collections(
        self,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """List collections.

        Returns:
            List of collection names.
        """
        operation = StoreOperation.list_collections(
            **kwargs,
        )
        return await self.arun(operation)

    async def aget(
        self,
        key: str | dict | VectorKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Get vector.

        Args:
            key:
                Vector key.
            collection:
                Collection name.

        Returns:
            Vector item.

        Raises:
            NotFoundError:
                Vector not found.
        """
        operation = StoreOperation.get(
            key=key,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aput(
        self,
        key: str | dict | VectorKey,
        value: list[float] | dict | VectorValue,
        metadata: dict | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Put vector.

        Args:
            key:
                Vector key.
            value:
                Vector value.
            metadata:
                Custom metadata.
            collection:
                Collection name.

        Returns:
            Vector item.
        """
        operation = StoreOperation.put(
            key=key,
            value=value,
            metadata=metadata,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aupdate(
        self,
        key: str | dict | VectorKey,
        value: list[float] | dict | VectorValue,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Update vector value.

        Args:
            key:
                Vector key.
            value:
                Vector value.
            collection:
                Collection name.

        Returns:
            Vector item.
        """
        update = Update()
        update.put(UpdateAttribute.VALUE, value)
        operation = StoreOperation.update(
            key=key,
            set=update,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aupdate_metadata(
        self,
        key: str | dict | VectorKey,
        metadata: dict | None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[VectorItem]:
        """Update vector metadata.

        Args:
            key:
                Vector key.
            metadata:
                Vector metadata.
            collection:
                Collection name.

        Returns:
            Vector item.
        """
        update = Update()
        update.put(UpdateAttribute.METADATA, metadata)
        operation = StoreOperation.update(
            key=key,
            set=update,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def adelete(
        self,
        key: str | dict | VectorKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete vector.

        Args:
            key:
                Vector key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Vector not found.
            PreconditionFailedError:
                Condition failed.
        """
        operation = StoreOperation.delete(
            key=key,
            where=where,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aquery(
        self,
        search: str | Expression | None = None,
        select: str | Select | None = None,
        where: str | Expression | None = None,
        order_by: str | OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[VectorList]:
        """Query vectors.

        Args:
            search:
                Search expression.
            select:
                Select expression.
            where:
                Condition expression.
            order_by:
                Order by expression.
            limit:
                Query limit.
            offset:
                Query offset.
            collection:
                Collection name.

        Returns:
            List of vectors.
        """
        operation = StoreOperation.query(
            select=select,
            search=search,
            where=where,
            order_by=order_by,
            limit=limit,
            offset=offset,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def acount(
        self,
        search: str | Expression | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count vectors.

        Args:
            search:
                Search expression.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Vector count.
        """
        operation = StoreOperation.count(
            search=search,
            where=where,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def abatch(
        self,
        operations: list[Operation],
        **kwargs: Any,
    ) -> Response[list[Any]]:
        """Batch operation.

        Args:
            operations:
                List of operations.

        Returns:
            Batch operation results.
        """
        operation = StoreOperation.batch(
            operations=operations,
            **kwargs,
        )
        return await self.arun(operation)

    async def atransact(
        self,
        operations: list[Operation],
        **kwargs: Any,
    ) -> Response[list[Any]]:
        """Execute transaction.

        Args:
            operations:
                List of operations.

        Returns:
            Transaction results.

        Raises:
            ConflictError:
                Transaction failed.
        """
        operation = StoreOperation.transact(
            operations=operations,
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


class VectorOperation:
    @staticmethod
    def get(
        key: str | dict | VectorKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Get vector operation.

        Args:
            key:
                Vector key.
            collection:
                Collection name.

        Returns:
            Get vector operation.
        """
        return StoreOperation.get(
            key=key,
            collection=collection,
            **kwargs,
        )

    @staticmethod
    def put(
        key: str | dict | VectorKey,
        value: list[float] | dict | VectorValue,
        metadata: dict | None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Put vector operation.

        Args:
            key:
                Vector key.
            value:
                Vector value.
            metadata:
                Custom metadata.
            collection:
                Collection name.

        Returns:
            Put vector operation.
        """
        return StoreOperation.put(
            key=key,
            value=value,
            metadata=metadata,
            collection=collection,
            **kwargs,
        )

    @staticmethod
    def delete(
        key: str | dict | VectorKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Delete vector operation.

        Args:
            key:
                Vector key.
            collection:
                Collection name.

        Returns:
            Delete vector operation.
        """
        return StoreOperation.delete(
            key=key,
            collection=collection,
            **kwargs,
        )
