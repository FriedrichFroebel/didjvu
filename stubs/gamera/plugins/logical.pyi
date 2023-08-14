from gamera.plugin import *
from _typeshed import Incomplete

class LogicalCombine(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete

class and_image(LogicalCombine):
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class or_image(LogicalCombine):
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class xor_image(LogicalCombine):
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class LogicalModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
