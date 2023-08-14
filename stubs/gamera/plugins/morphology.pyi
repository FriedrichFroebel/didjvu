from gamera.plugin import *
from _typeshed import Incomplete

class erode(PluginFunction):
    self_type: Incomplete
    doc_examples: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(image): ...
    __call__: Incomplete

class dilate(PluginFunction):
    self_type: Incomplete
    doc_examples: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(image): ...
    __call__: Incomplete

class erode_dilate(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class despeckle(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete

class distance_transform(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    author: str

class dilate_with_structure(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, structuring_element, origin, only_border: bool = ...): ...
    __call__: Incomplete

class erode_with_structure(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str

class MorphologyModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
