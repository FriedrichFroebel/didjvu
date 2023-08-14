from gamera.plugin import *
from _typeshed import Incomplete

class difference_of_exponential_edge_image(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, scale: float = ..., gradient_threshold: float = ..., min_edge_length: int = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class difference_of_exponential_crack_edge_image(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, scale: float = ..., gradient_threshold: float = ..., min_edge_length: int = ..., close_gaps: bool = ..., beautify: bool = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class canny_edge_image(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, scale: float = ..., gradient_threshold: float = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class labeled_region_edges(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, mark_both: bool = ...): ...
    __call__: Incomplete

class outline(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(self, which: int = ...): ...
    __call__: Incomplete

class EdgeDetect(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
