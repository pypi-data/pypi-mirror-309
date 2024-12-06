"""
Secret Store on Environment variables.
"""

__all__ = ["Environment"]

import os
from typing import Any

from verse.core import Context, Operation, Response
from verse.core.exceptions import NotFoundError, PreconditionFailedError
from verse.internal.storage_core import StoreOperation, StoreProvider

from .._constants import LATEST_VERSION
from .._models import SecretItem, SecretKey, SecretVersion


class Environment(StoreProvider):
    def __init__(self, **kwargs):
        """Initalize."""
        pass

    def init(self, context: Context | None = None) -> None:
        pass

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
            val = os.environ.get(id)
            if val is None:
                raise NotFoundError
            result = SecretItem(
                key=SecretKey(id=id, version=LATEST_VERSION), value=val
            )
        # GET versions
        elif (
            op_parser.op_equals(StoreOperation.GET)
            and op_parser.is_versions_attribute()
        ):
            id = op_parser.get_id_as_str()
            val = os.environ.get(id)
            if val is None:
                raise NotFoundError
            versions: list = []
            versions.append(SecretVersion(version=LATEST_VERSION))
            result = SecretItem(key=SecretKey(id=id), versions=versions)
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            id = op_parser.get_id_as_str()
            value = str(op_parser.get_value())
            exists = op_parser.get_where_exists()
            if exists is False:
                current_value = os.environ.get(id)
                if current_value is not None:
                    raise PreconditionFailedError
            elif exists is True:
                current_value = os.environ.get(id)
                if current_value is None:
                    raise PreconditionFailedError
            os.environ[id] = value
            result = SecretItem(key=SecretKey(id=id, version=LATEST_VERSION))
        # UPDATE value
        elif (
            op_parser.op_equals(StoreOperation.UPDATE)
            and op_parser.is_value_update()
        ):
            id = op_parser.get_id_as_str()
            value = str(op_parser.get_updated_value())
            current_value = os.environ.get(id)
            if current_value is None:
                raise NotFoundError
            os.environ[id] = value
            result = SecretItem(key=SecretKey(id=id, version=LATEST_VERSION))
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            id = op_parser.get_id_as_str()
            try:
                os.environ.pop(id)
            except KeyError:
                raise NotFoundError
            result = None
        # CLOSE
        elif op_parser.op_equals(StoreOperation.CLOSE):
            result = None
        else:
            return super().run(operation)
        return Response(result=result)
