from .command.router import command_router
from .command.service import get_command_service, CommandService

from.callback.service import get_callback_service, CallbackService



__routers__ = [
     command_router,
]


__depends__ = {
     CommandService: get_command_service,
     CallbackService: get_callback_service
}