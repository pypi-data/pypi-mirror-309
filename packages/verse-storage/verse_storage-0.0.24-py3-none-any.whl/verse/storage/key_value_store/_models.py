from verse.core import DataModel


class KeyValueKey(DataModel):
    """Key Value key."""

    id: str
    """Key Value id.
    """


class KeyValueItem(DataModel):
    """Config item."""

    key: KeyValueKey
    """Key Value key.
    """

    value: str | bytes | None = None
    """Config value.
    """


class KeyValueList(DataModel):
    """Key Value item list."""

    items: list[KeyValueItem]
    """List of Key Value items.
    """
