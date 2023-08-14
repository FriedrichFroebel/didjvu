from gamera.plugin import *
from _typeshed import Incomplete

ARITHMETIC_TYPES: Incomplete

class ArithmeticCombine(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    image_types_must_match: bool

class add_images(ArithmeticCombine):
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class subtract_images(ArithmeticCombine):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class divide_images(ArithmeticCombine):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete

class multiply_images(ArithmeticCombine):
    def __call__(self, other, in_place: bool = ...): ...
    __call__: Incomplete

class ArithmeticModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
