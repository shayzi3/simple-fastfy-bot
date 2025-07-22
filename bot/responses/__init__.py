from .abstract import AnyResponse
from .error import (
    InvalidSteamID,
    InventoryLock,
    SkinNotExists,
    SkinNotFound,
    SteamUserNotFound,
    TryLater,
)
from .success import DataUpdate, SkinCreate, SkinDelete


def isresponse(obj: type) -> bool:
    return isinstance(obj, type) and AnyResponse in obj.mro()