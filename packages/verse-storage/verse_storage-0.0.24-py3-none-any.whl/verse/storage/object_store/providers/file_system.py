"""
Object Store on File System.
"""

from __future__ import annotations

__all__ = ["FileSystem"]

import os
from typing import Any

from verse.core import Context, NCall, Operation, Response
from verse.core.exceptions import BadRequestError
from verse.internal.storage_core import (
    ItemProcessor,
    StoreOperation,
    StoreOperationParser,
    StoreProvider,
)

from .._helper import get_collection_config
from .._models import ObjectCollectionConfig


class FileSystem(StoreProvider):
    store_path: str
    folder: str | None
    nparams: dict[str, Any]

    _init: bool
    _collection_cache: dict[str, FileSystemCollection]

    def __init__(
        self,
        store_path: str = ".",
        folder: str | None = None,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            store_path:
                Base store path. Defaults to ".".
            folder:
                Folder name mapped to object store collection name.
            nparams:
                Native parameters to file system operations.
        """
        self.store_path = store_path
        self.folder = folder
        self.nparams = nparams

        self._init = False
        self._collection_cache = dict()

    def init(self, context: Context | None = None) -> None:
        if not self._init:
            return

        self._init = True

    def _get_folder_name(self, op_parser: StoreOperationParser) -> str | None:
        collection_name = (
            op_parser.get_operation_parsers()[0].get_collection_name()
            if op_parser.op_equals(StoreOperation.BATCH)
            else op_parser.get_collection_name()
        )
        folder = (
            collection_name if collection_name is not None else self.folder
        )
        return folder

    def _get_collection(
        self, op_parser: StoreOperationParser
    ) -> FileSystemCollection | None:
        if op_parser.is_resource_op():
            return None
        folder_name = self._get_folder_name(op_parser)
        if folder_name is None:
            raise BadRequestError("Collection name must be specified")
        if folder_name in self._collection_cache:
            return self._collection_cache[folder_name]
        col = FileSystemCollection(self.store_path, folder_name)
        self._collection_cache[folder_name] = col
        return col

    def _validate(self, op_parser: StoreOperationParser):
        pass

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        self.init(context=context)
        op_parser = self.get_op_parser(operation)
        self._validate(op_parser)
        collection = self._get_collection(op_parser)
        ncall, state = self._get_ncall(
            op_parser,
            collection,
            ResourceHelper(self.store_path),
        )
        if ncall is None:
            return super().run(operation=operation, context=context)
        nresult, nerror = ncall.invoke(return_error=True)
        result = self._convert_nresult(
            nresult, nerror, state, op_parser, collection
        )
        return Response(result=result, native=dict(result=nresult, call=ncall))

    def _get_ncall(
        self,
        op_parser: StoreOperationParser,
        collection: FileSystemCollection | None,
        resource_helper: Any,
    ) -> tuple[NCall | None, dict | None]:
        call = None
        state = None
        nargs = op_parser.get_nargs()
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            args = {
                "folder": self._get_folder_name(op_parser),
                "config": get_collection_config(op_parser),
                "nargs": nargs,
            }
            call = NCall(resource_helper.create_collection, args)
        # DROP COLLECTION
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            args = {
                "folder": self._get_folder_name(op_parser),
                "nargs": nargs,
            }
            call = NCall(resource_helper.drop_collection, args)
        # LIST COLLECTIONS
        elif op_parser.op_equals(StoreOperation.LIST_COLLECTIONS):
            args = {"nargs": nargs}
            call = NCall(resource_helper.list_collections, args)
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
        collection: FileSystemCollection | None,
    ) -> Any:
        result: Any = None
        # CREATE COLLECTION
        if op_parser.op_equals(StoreOperation.CREATE_COLLECTION):
            result = None
        # DROP COLLECTION
        elif op_parser.op_equals(StoreOperation.DROP_COLLECTION):
            result = None
        # LIST COLLECTIONS
        elif op_parser.op_equals(StoreOperation.LIST_COLLECTIONS):
            result = nresult
        return result


class ResourceHelper:
    store_path: str

    def __init__(self, store_path: str):
        self.store_path = store_path

    def create_collection(
        self, folder: str, config: ObjectCollectionConfig | None, nargs: Any
    ):
        folder_path = os.path.join(self.store_path, folder)
        os.makedirs(folder_path, exist_ok=True)

    def drop_collection(self, folder: str, nargs: Any):
        folder_path = os.path.join(self.store_path, folder)
        import shutil

        shutil.rmtree(folder_path)

    def list_collections(self, nargs) -> Any:
        nresult = []
        items = os.listdir(self.store_path)
        for item in items:
            if not os.path.isfile(item):
                nresult.append(item)
        return nresult

    def close(self, nargs: Any) -> Any:
        pass


class OperationConverter:
    processor: ItemProcessor

    def __init__(self, processor: ItemProcessor):
        self.processor = processor


class FileSystemCollection:
    converter: OperationConverter
    processor: ItemProcessor

    def __init__(self, store_path: str, collection_name: str):
        self.processor = ItemProcessor()
        self.converter = OperationConverter(self.processor)
