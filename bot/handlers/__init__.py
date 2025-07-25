from .callback.router import callback_router
from .command.router import command_router
from .state.router import state_router

__routers__ = [
     command_router,
     callback_router,
     state_router
]

