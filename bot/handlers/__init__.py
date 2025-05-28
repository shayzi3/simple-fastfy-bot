from .callback.router import callback_router
from .callback.service import CallbackService, get_callback_service
from .command.router import command_router
from .command.service import CommandService, get_command_service
from .state.router import state_router
from .state.service import StateService, get_state_service

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