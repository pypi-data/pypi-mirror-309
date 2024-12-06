from __future__ import annotations

from typing import Any

from verse.core import DataModel, Operation, Response
from verse.internal.storage_core import Index, StoreComponent, StoreOperation
from verse.ql import Expression, OrderBy, Select, Update

from ._models import (
    DocumentCollectionConfig,
    DocumentItem,
    DocumentKey,
    DocumentKeyType,
    DocumentList,
)


class DocumentStore(StoreComponent):
    collection: str | None
    id_map_field: str | dict | None
    pk_map_field: str | dict | None

    def __init__(
        self,
        collection: str | None = None,
        id_map_field: str | dict | None = "id",
        pk_map_field: str | dict | None = "pk",
        **kwargs,
    ):
        """Initialize.

        Args:
            collection:
                Default collection name.
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
        """
        self.collection = collection
        self.id_map_field = id_map_field
        self.pk_map_field = pk_map_field

        super().__init__(**kwargs)

    def get_component_parameters(self):
        return ["collection", "id_map_field", "pk_map_field"]

    def create_collection(
        self,
        collection: str | None = None,
        config: dict | DocumentCollectionConfig | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Create collection.

        Args:
            collection:
                Collection name.
            config:
                Collection config.
            where:
                Condition expression.
        """
        return self._run_internal(StoreOperation.CREATE_COLLECTION, locals())

    def drop_collection(
        self,
        collection: str | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Drop collection.

        Args:
            collection:
                Collection name.
            where:
                Condition expression.
        """
        return self._run_internal(StoreOperation.DROP_COLLECTION, locals())

    def list_collections(
        self,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """List collections.

        Returns:
            List of collection names.
        """
        return self._run_internal(StoreOperation.LIST_COLLECTIONS, locals())

    def create_index(
        self,
        index: dict | Index,
        collection: str | None = None,
    ) -> Response[None]:
        """Create index.

        Args:
            index:
                Index to create.
            collection:
                Collection name.
        """
        return self._run_internal(StoreOperation.CREATE_INDEX, locals())

    def drop_index(
        self,
        index: dict | Index | None = None,
        collection: str | None = None,
    ) -> Response[None]:
        """Drop index.

        Args:
            index:
                Index to drop.
            collection:
                Collection name.
        """
        return self._run_internal(StoreOperation.DROP_INDEX, locals())

    def list_indexes(
        self,
        collection: str | None = None,
    ) -> Response[list[Index]]:
        """List indexes.

        Args:
            collection:
                Collection name.
        """
        return self._run_internal(StoreOperation.LIST_INDEXES, locals())

    def get(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[DocumentItem]:
        """Get document.

        Args:
            key:
                Document key.
            collection:
                Collection name.

        Returns:
            Document item.

        Raises:
            NotFoundError:
                Document not found.
        """
        return self._run_internal(StoreOperation.GET, locals())

    def put(
        self,
        value: dict[str, Any] | DataModel,
        key: DocumentKeyType | dict | DocumentKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[DocumentItem]:
        """Put document.

        Args:
            value:
                Document.
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Document item.

        Raises:
            PreconditionFailedError:
                Condition failed.
        """
        return self._run_internal(StoreOperation.PUT, locals())

    def update(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        set: str | Update,
        where: str | Expression | None = None,
        returning: bool | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[DocumentItem]:
        """Update document.

        Args:
            key:
                Document key.
            set:
                Update expression.
            where:
                Condition expression.
            returning:
                A value indicating whether updated document is returned.
            collection:
                Collection name.

        Returns:
            Document item.

        Raises:
            NotFoundError:
                Document not found.
            PreconditionFailedError:
                Condition failed.
        """
        return self._run_internal(StoreOperation.UPDATE, locals())

    def delete(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete document.

        Args:
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Document not found.
            PreconditionFailedError:
                Condition failed.
        """
        return self._run_internal(StoreOperation.DELETE, locals())

    def query(
        self,
        select: str | Select | None = None,
        where: str | Expression | None = None,
        order_by: str | OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[DocumentList]:
        """Query documents.

        Args:
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
            Document list with items.
        """
        return self._run_internal(StoreOperation.QUERY, locals())

    def count(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count documents.

        Args:
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Count of documents.
        """
        return self._run_internal(StoreOperation.COUNT, locals())

    def batch(
        self,
        operations: list[Operation],
        **kwargs,
    ) -> Response[list[Any]]:
        """Execute batch.

        Args:
            operations:
                List of document operations.

        Returns:
            Batch operation results.
        """
        return self._run_internal(StoreOperation.BATCH, locals())

    def transact(
        self,
        operations: list[Operation],
        **kwargs,
    ) -> Response[list[Any]]:
        """Execute transaction.

        Args:
            operations:
                List of document operations.

        Returns:
            Transaction results.

        Raises:
            ConflictError:
                Transaction failed.
        """
        return self._run_internal(StoreOperation.TRANSACT, locals())

    def close(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close client.

        Returns:
            None.
        """
        return self._run_internal(StoreOperation.CLOSE, locals())

    async def acreate_collection(
        self,
        collection: str | None = None,
        config: dict | DocumentCollectionConfig | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Create collection.

        Args:
            collection:
                Collection name.
            config:
                Collection config.
            where:
                Condition expression.

        Returns:
            None.
        """
        return await self._arun_internal(
            StoreOperation.CREATE_COLLECTION, locals()
        )

    async def adrop_collection(
        self,
        collection: str | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Drop collection.

        Args:
            collection:
                Collection name.
            where:
                Condition expression.

        Returns:
            None.
        """
        return await self._arun_internal(
            StoreOperation.DROP_COLLECTION, locals()
        )

    async def alist_collections(
        self,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """List collections.

        Returns:
            List of collection names.
        """
        return await self._arun_internal(
            StoreOperation.LIST_COLLECTIONS, locals()
        )

    async def acreate_index(
        self,
        index: dict | Index,
        collection: str | None = None,
    ) -> Response[None]:
        """Create index.

        Args:
            index:
                Index to create.
            collection:
                Collection name.
        """
        return await self._arun_internal(StoreOperation.CREATE_INDEX, locals())

    async def adrop_index(
        self,
        index: dict | Index | None = None,
        collection: str | None = None,
    ) -> Response[None]:
        """Drop index.

        Args:
            index:
                Index to drop.
            collection:
                Collection name.
        """
        return await self._arun_internal(StoreOperation.DROP_INDEX, locals())

    async def alist_indexes(
        self,
        collection: str | None = None,
    ) -> Response[list[Index]]:
        """List indexes.

        Args:
            collection:
                Collection name.
        """
        return await self._arun_internal(StoreOperation.LIST_INDEXES, locals())

    async def aget(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[DocumentItem]:
        """Get document.

        Args:
            key:
                Document key.
            collection:
                Collection name.

        Returns:
            Document item.

        Raises:
            NotFoundError:
                Document not found.
        """
        return await self._arun_internal(StoreOperation.GET, locals())

    async def aput(
        self,
        value: dict[str, Any] | DataModel,
        key: DocumentKeyType | dict | DocumentKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[DocumentItem]:
        """Put document.

        Args:
            value:
                Document.
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Document item.

        Raises:
            PreconditionFailedError:
                Condition failed.
        """
        return await self._arun_internal(StoreOperation.PUT, locals())

    async def aupdate(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        set: str | Update,
        where: str | Expression | None = None,
        returning: bool | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[DocumentItem]:
        """Update document.

        Args:
            key:
                Document key.
            set:
                Update expression.
            where:
                Condition expression.
            returning:
                A value indicating whether updated document is returned.
            collection:
                Collection name.

        Returns:
            Document item.

        Raises:
            NotFoundError:
                Document not found.
            PreconditionFailedError:
                Condition failed.
        """
        return await self._arun_internal(StoreOperation.UPDATE, locals())

    async def adelete(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete document.

        Args:
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Document not found.
            PreconditionFailedError:
                Condition failed.
        """
        return await self._arun_internal(StoreOperation.DELETE, locals())

    async def aquery(
        self,
        select: str | Select | None = None,
        where: str | Expression | None = None,
        order_by: str | OrderBy | None = None,
        limit: int | None = None,
        offset: int | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[DocumentList]:
        """Query documents.

        Args:
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
            Document list with items.
        """
        return await self._arun_internal(StoreOperation.QUERY, locals())

    async def acount(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count documents.

        Args:
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Count of documents.
        """
        return await self._arun_internal(StoreOperation.COUNT, locals())

    async def abatch(
        self,
        operations: list[Operation],
        **kwargs: Any,
    ) -> Response[list[Any]]:
        """Execute batch.

        Args:
            operations:
                List of document operations.

        Returns:
            Batch operation results.
        """
        return await self._arun_internal(StoreOperation.BATCH, locals())

    async def atransact(
        self,
        operations: list[Operation],
        **kwargs: Any,
    ) -> Response[list[Any]]:
        """Execute transaction.

        Args:
            operations:
                List of document operations.

        Returns:
            Transaction results.

        Raises:
            ConflictError:
                Transaction failed.
        """
        return await self._arun_internal(StoreOperation.TRANSACT, locals())

    async def aclose(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close async client.

        Returns:
            None.
        """
        return await self._arun_internal(StoreOperation.CLOSE, locals())


class DocumentOperation:
    @staticmethod
    def get(
        key: DocumentKeyType | dict | DocumentKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Operation:
        """Get operation.

        Args:
            key:
                Document key.
            collection:
                Collection name.

        Returns:
            Get operation.
        """
        return StoreOperation.get(
            key=key,
            collection=collection,
            **kwargs,
        )

    @staticmethod
    def put(
        value: dict[str, Any] | DataModel,
        key: DocumentKeyType | dict | DocumentKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Operation:
        """Put operation.

        Args:
            value:
                Document value.
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            _description_
        """
        return StoreOperation.put(
            key=key,
            value=value,
            where=where,
            collection=collection,
            **kwargs,
        )

    @staticmethod
    def update(
        key: DocumentKeyType | dict | DocumentKey,
        set: str | Update,
        where: str | Expression | None = None,
        returning: bool | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Operation:
        """Update operation.

        Args:
            key:
                Document key.
            set:
                Update expression.
            where:
                Condition expression.
            returning:
                A value indicating whether the updated document is returned.
            collection:
                Collection name.

        Returns:
            Update operation.
        """
        return StoreOperation.update(
            key=key,
            set=set,
            where=where,
            returning=returning,
            collection=collection,
            **kwargs,
        )

    @staticmethod
    def delete(
        key: DocumentKeyType | dict | DocumentKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Operation:
        """Delete operation.

        Args:
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Delete operation.
        """
        return StoreOperation.delete(
            key=key,
            where=where,
            collection=collection,
            **kwargs,
        )


class DocumentBatch(DataModel):
    operations: list[Operation] = []

    def get(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Get operation.

        Args:
            key:
                Document key.
            collection:
                Collection name.

        Returns:
            Get operation.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.GET, args=locals())
        )

    def put(
        self,
        value: dict[str, Any] | DataModel,
        key: DocumentKeyType | dict | DocumentKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Put operation.

        Args:
            value:
                Document value.
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.PUT, args=locals())
        )

    def update(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        set: str | Update,
        where: str | Expression | None = None,
        returning: bool | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Update operation.

        Args:
            key:
                Document key.
            set:
                Update expression.
            where:
                Condition expression.
            returning:
                A value indicating whether the updated document is returned.
            collection:
                Collection name.

        Returns:
            Update operation.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.UPDATE, args=locals())
        )

    def delete(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Delete operation.

        Args:
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Delete operation.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.PUT, args=locals())
        )


class DocumentTransaction(DataModel):
    operations: list[Operation] = []

    def get(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Get operation.

        Args:
            key:
                Document key.
            collection:
                Collection name.

        Returns:
            Get operation.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.GET, args=locals())
        )

    def put(
        self,
        value: dict[str, Any] | DataModel,
        key: DocumentKeyType | dict | DocumentKey | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Put operation.

        Args:
            value:
                Document value.
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.PUT, args=locals())
        )

    def update(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        set: str | Update,
        where: str | Expression | None = None,
        returning: bool | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Update operation.

        Args:
            key:
                Document key.
            set:
                Update expression.
            where:
                Condition expression.
            returning:
                A value indicating whether the updated document is returned.
            collection:
                Collection name.

        Returns:
            Update operation.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.UPDATE, args=locals())
        )

    def delete(
        self,
        key: DocumentKeyType | dict | DocumentKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Delete operation.

        Args:
            key:
                Document key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Delete operation.
        """
        self.operations.append(
            Operation.normalize(name=StoreOperation.PUT, args=locals())
        )
