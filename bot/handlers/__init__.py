from .command.router import command_router
from .callback.router import callback_router
from .state.router import state_router

from .state.service import get_state_service, StateService
from .command.service import get_command_service, CommandService
from .callback.service import get_callback_service, CallbackService



__routers__ = [
     command_router,
     callback_router,
     state_router
]


__depends__ = {
     CommandService: get_command_service,
     CallbackService: get_callback_service,
     StateService: get_state_service
}