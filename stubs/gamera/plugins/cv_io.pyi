from gamera.plugin import *
from _typeshed import Incomplete
from gamera import config as config

verbose: Incomplete

class from_cv(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    pure_python: bool
    def __call__(image, offset: Incomplete | None = ...): ...
    __call__: Incomplete

class to_cv(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    def __call__(image): ...
    __call__: Incomplete

class CVioModule(PluginModule):
    category: str
    author: str
    functions: Incomplete
    pure_python: bool
    url: str

module: Incomplete
