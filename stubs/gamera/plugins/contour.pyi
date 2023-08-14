from gamera.plugin import *
from _typeshed import Incomplete

class Contour(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class contour_top(Contour): ...
class contour_bottom(Contour): ...
class contour_left(Contour): ...
class contour_right(Contour): ...

class contour_samplepoints(PluginFunction):
    self_type: Incomplete
    author: str
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(self, percentage: int = ..., contourtype: int = ...): ...
    __call__: Incomplete

class contour_pavlidis(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    author: str

class ContourModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
