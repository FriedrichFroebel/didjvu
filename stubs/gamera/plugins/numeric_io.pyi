from gamera.plugin import *
from _typeshed import Incomplete
from gamera import config as config
from gamera.util import warn_deprecated as warn_deprecated

verbose: Incomplete

class from_numeric(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(array, offset=...): ...
    __call__: Incomplete

class to_numeric(PluginFunction):
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

class NumericModule(PluginModule):
    category: Incomplete
    author: str
    functions: Incomplete
    pure_python: bool
    url: str

module: Incomplete
