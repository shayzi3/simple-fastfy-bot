from .abstract import AnyResponse
from .error import (
    InvalidSteamID,
    InvenotoryEmpty,
    InventoryLock,
    SkinNotExists,
    SkinNotFound,
    SteamSkinsExistsInInventory,
    SteamUserNotFound,
    TryLater,
)
from .success import DataUpdate, SkinCreate, SkinDelete


def isresponse(obj: type) -> bool:
    return isinstance(obj, type) and AnyResponse in obj.mro()