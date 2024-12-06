"""
Secret Store on YAML file.
"""

__all__ = ["YamlFile"]

from typing import Any

import yaml

from verse.core import Context, Operation, Response
from verse.core.exceptions import NotFoundError
from verse.internal.storage_core import StoreOperation, StoreProvider

from .._constants import LATEST_VERSION
from .._models import SecretItem, SecretKey


class YamlFile(StoreProvider):
    path: str

    _items: dict | None

    def __init__(self, path: str = "secret.yaml", **kwargs):
        """Initialize.

        Args:
            path:
                File path. Defaults to "secret.yaml".
        """
        self.path = path
        self._items = None

    def init(self, context: Context | None = None) -> None:
        if self._items is not None:
            return
        self._items = yaml.safe_load(self.path)
        if self._items is None:
            self._items = dict()

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        self.init(context=context)
        op_parser = self.get_op_parser(operation)
        result = None
        # GET value
        if (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_value_attribute()
        ):
            id = op_parser.get_id_as_str()
            if self._items is None:
                raise NotFoundError
            if id not in self._items:
                raise NotFoundError
            val = self._items[id]
            result = SecretItem(
                key=SecretKey(id=id, version=LATEST_VERSION), value=val
            )
        # CLOSE
        elif op_parser.op_equals(StoreOperation.CLOSE):
            pass
        else:
            return super().run(operation)
        return Response(result=result)
