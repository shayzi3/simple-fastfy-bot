from .command.router import command_router
from .command.service import get_command_service

from.callback.service import get_callback_service



__routers__ = [
     command_router,
]


__depends__ = {
     "CommandService": get_command_service,
     "CallbackService": get_callback_service,
     "UserDataclass": ...
}