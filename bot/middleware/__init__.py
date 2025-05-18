from .depends import DependMiddleware
from .log import LogMiddleware
from .timeout import TimeoutMiddleware


__middlewares__ = [
     LogMiddleware,
     TimeoutMiddleware,
     DependMiddleware,
]