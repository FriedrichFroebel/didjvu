from gamera.plugin import *
from _typeshed import Incomplete
from gamera import config as config

verbose: Incomplete

class from_pil(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    pure_python: bool
    def __call__(image, offset: Incomplete | None = ...): ...
    __call__: Incomplete

class to_pil(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    def __call__(image): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    def __doc_example2__(images): ...
    doc_examples: Incomplete

class PilIOModule(PluginModule):
    category: str
    author: str
    functions: Incomplete
    pure_python: bool
    url: str

module: Incomplete
