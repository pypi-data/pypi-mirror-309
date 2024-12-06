from __future__ import annotations

from typing import IO, Any

from verse.core import Operation, Response
from verse.internal.storage_core import (
    Attribute,
    StoreComponent,
    StoreOperation,
    UpdateAttribute,
)
from verse.ql import Expression, Update, Value

from ._models import (
    ObjectCollectionConfig,
    ObjectItem,
    ObjectKey,
    ObjectList,
    ObjectProperties,
    ObjectQueryConfig,
    ObjectSource,
    ObjectTransferConfig,
)


class ObjectStore(StoreComponent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_collection(
        self,
        collection: str | None = None,
        config: dict | ObjectCollectionConfig | None = None,
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

    def put(
        self,
        key: str | dict | ObjectKey,
        value: Value = None,
        file: str | None = None,
        stream: IO | None = None,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Put object.

        Args:
            key:
                Object key.
            value:
                Object value. If the type is not bytes, it
                will be converted to bytes.
            file:
                File path to upload.
            stream:
                Stream to upload.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            PreconditionFailedError:
                Condition failed.
        """
        operation = StoreOperation.put(
            key=key,
            value=value,
            file=file,
            stream=stream,
            metadata=metadata,
            properties=properties,
            where=where,
            config=config,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def get(
        self,
        key: str | dict | ObjectKey,
        file: str | None = None,
        stream: IO | None = None,
        where: str | Expression | None = None,
        start: int | None = None,
        end: int | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object.

        Args:
            key:
                Object key.
            file:
                File path to download.
            stream:
                Stream to download to.
            where:
                Condition expression.
            start:
                Start bytes for range request.
            end:
                End bytes for range request.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        operation = StoreOperation.get(
            key=key,
            file=file,
            stream=stream,
            where=where,
            start=start,
            end=end,
            config=config,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def get_metadata(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object metadata.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with metadata.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        operation = StoreOperation.get(
            key=key,
            attr=Attribute.METADATA,
            where=where,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def get_properties(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object properties.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with properties.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        operation = StoreOperation.get(
            key=key,
            attr=Attribute.PROPERTIES,
            where=where,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def get_versions(
        self,
        key: str | dict | ObjectKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object versions.

        Args:
            key:
                Object key.
            collection:
                Collection name.

        Returns:
            Object item with object versions.

        Raises:
            NotFoundError:
                Object not found.
        """
        operation = StoreOperation.get(
            key=key,
            attr=Attribute.VERSIONS,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def update(
        self,
        key: str | dict | ObjectKey,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Update object metadata and properties.

        Args:
            key:
                Objecy key.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            PreconditionFailedError:
                Condition failed.
        """
        update = Update()
        update.put(UpdateAttribute.METADATA, metadata)
        update.put(UpdateAttribute.PROPERTIES, properties)
        operation = StoreOperation.update(
            key=key, set=update, where=where, collection=collection, **kwargs
        )
        return self.run(operation)

    def delete(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete object.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Object not found.
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

    def copy(
        self,
        key: str | dict | ObjectKey,
        source: str | dict | ObjectSource,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Copy object.

        Args:
            key:
                Destination object key.
            source:
                Object source.
            collection:
                Collection name.

        Returns:
            Copied object item.

        Raises:
            NotFoundError:
                Source object not found.
        """
        operation = StoreOperation.copy(
            key=key,
            source=source,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def generate(
        self,
        key: str | dict | ObjectKey,
        method: str,
        expiry: int,
        collection: str | None = None,
    ) -> Response[ObjectItem]:
        """Generate signed URL.

        Args:
            key:
                Object key.
            method:
                Operation method. One of "GET", "PUT" or "DELETE".
            expiry:
                Expiry in seconds
            collection:
                Collection name.

        Returns:
            Object item with signed URL.
        """
        operation = StoreOperation.generate(
            key=key,
            method=method,
            expiry=expiry,
            collection=collection,
        )
        return self.run(operation)

    def query(
        self,
        where: str | Expression | None = None,
        limit: int | None = None,
        continuation: str | None = None,
        config: dict | ObjectQueryConfig | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[ObjectList]:
        """Query objects.

        Args:
            where:
                Condition expression.
            limit:
                Query limit.
            continuation:
                Continuation token.
            config:
                Query config.
            collection:
                Collection name.

        Returns:
            List of objects.
        """
        operation = StoreOperation.query(
            where=where,
            limit=limit,
            continuation=continuation,
            config=config,
            collection=collection,
            **kwargs,
        )
        return self.run(operation)

    def count(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count objects.

        Args:
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Count of objects.
        """
        operation = StoreOperation.count(
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
        config: dict | ObjectCollectionConfig | None = None,
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

    async def aput(
        self,
        key: str | dict | ObjectKey,
        value: Value = None,
        file: str | None = None,
        stream: IO | None = None,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Put object.

        Args:
            key:
                Object key.
            value:
                Object value. If the type is not bytes, it
                will be converted to bytes.
            file:
                File path to upload.
            stream:
                Stream to upload.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            PreconditionFailedError:
                Condition failed.
        """
        operation = StoreOperation.put(
            key=key,
            value=value,
            file=file,
            stream=stream,
            metadata=metadata,
            properties=properties,
            where=where,
            config=config,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aget(
        self,
        key: str | dict | ObjectKey,
        file: str | None = None,
        stream: IO | None = None,
        where: str | Expression | None = None,
        start: int | None = None,
        end: int | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object.

        Args:
            key:
                Object key.
            file:
                File path to download.
            stream:
                Stream to download to.
            where:
                Condition expression.
            start:
                Start bytes for range request.
            end:
                End bytes for range request.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        operation = StoreOperation.get(
            collection=collection,
            key=key,
            file=file,
            stream=stream,
            where=where,
            start=start,
            end=end,
            config=config,
            **kwargs,
        )
        return await self.arun(operation)

    async def aget_metadata(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object metadata.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with metadata.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        operation = StoreOperation.get(
            key=key,
            attr=Attribute.METADATA,
            where=where,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aget_properties(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object properties.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with properties.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        operation = StoreOperation.get(
            key=key,
            attr=Attribute.PROPERTIES,
            where=where,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aget_versions(
        self,
        key: str | dict | ObjectKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object versions.

        Args:
            key:
                Object key.
            collection:
                Collection name.

        Returns:
            Object item with object versions.

        Raises:
            NotFoundError:
                Object not found.
        """
        operation = StoreOperation.get(
            key=key,
            attr=Attribute.VERSIONS,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def aupdate(
        self,
        key: str | dict | ObjectKey,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Update object metadata and properties.

        Args:
            key:
                Objecy key.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            PreconditionFailedError:
                Condition failed.
        """
        update = Update()
        update.put(UpdateAttribute.METADATA, metadata)
        update.put(UpdateAttribute.PROPERTIES, properties)
        operation = StoreOperation.update(
            key=key,
            set=update,
            where=where,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def adelete(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete object.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Object not found.
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

    async def acopy(
        self,
        key: str | dict | ObjectKey,
        source: str | dict | ObjectSource,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Copy object.

        Args:
            key:
                Destination object key.
            source:
                Object source.
            collection:
                Collection name.

        Returns:
            Copied object item.

        Raises:
            NotFoundError:
                Source object not found.
        """
        operation = StoreOperation.copy(
            key=key,
            source=source,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def agenerate(
        self,
        key: str | dict | ObjectKey,
        method: str,
        expiry: int,
        collection: str | None = None,
    ) -> Response[ObjectItem]:
        """Generate signed URL.

        Args:
            key:
                Object key.
            method:
                Operation method. One of "GET", "PUT" or "DELETE".
            expiry:
                Expiry in seconds
            collection:
                Collection name.

        Returns:
            Object item with signed URL.
        """
        operation = StoreOperation.generate(
            key=key, method=method, expiry=expiry, collection=collection
        )
        return await self.arun(operation)

    async def aquery(
        self,
        where: str | Expression | None = None,
        limit: int | None = None,
        continuation: str | None = None,
        config: dict | ObjectQueryConfig | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[ObjectList]:
        """Query objects.

        Args:
            where:
                Condition expression.
            limit:
                Query limit.
            continuation:
                Continuation token.
            config:
                Query config.
            collection:
                Collection name.

        Returns:
            List of objects.
        """
        operation = StoreOperation.query(
            where=where,
            limit=limit,
            continuation=continuation,
            config=config,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def acount(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count objects.

        Args:
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Count of objects.
        """
        operation = StoreOperation.count(
            where=where,
            collection=collection,
            **kwargs,
        )
        return await self.arun(operation)

    async def abatch(
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


class ObjectOperation:
    @staticmethod
    def delete(
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Operation:
        """Delete object operation.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Delete object operation.
        """
        return StoreOperation.delete(
            key=key,
            where=where,
            collection=collection,
            **kwargs,
        )
