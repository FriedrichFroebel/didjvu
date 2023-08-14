from gamera.plugin import *
from _typeshed import Incomplete
from gamera import config as config

verbose: Incomplete

class from_numpy(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(array, offset=...): ...
    __call__: Incomplete

class to_numpy(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(image): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    def __doc_example2__(images): ...
    def __doc_example4__(images): ...
    def __doc_example5__(images): ...
    def __doc_example6__(images): ...
    doc_examples: Incomplete

class NumpyModule(PluginModule):
    category: str
    author: str
    functions: Incomplete
    pure_python: bool

module: Incomplete
