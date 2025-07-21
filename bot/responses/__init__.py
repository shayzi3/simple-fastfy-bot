from .abstract import AnyResponse
from .error import (
    InvalidSteamID,
    InventoryEmpty,
    InventoryLock,
    SkinNotFound,
    SteamUserNotFound,
    TryLater,
)
from .success import DataUpdate, SkinCreate


def isresponse(obj: type) -> bool:
    return isinstance(obj, type) and AnyResponse in obj.mro()