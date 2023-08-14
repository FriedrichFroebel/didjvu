from gamera.plugin import *
from _typeshed import Incomplete

class permute_list(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class all_subsets(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class median(PluginFunction):
    category: str
    pure_python: int
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    def __call__(list, inlist: bool = ...): ...
    __call__: Incomplete

class median_py(PluginFunction):
    category: Incomplete
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str

class kernel_density(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    def __call__(values, x, bw: float = ..., kernel: int = ...): ...
    __call__: Incomplete

class argmax(PluginFunction):
    category: str
    pure_python: int
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    def __call__(x): ...
    __call__: Incomplete

class argmin(PluginFunction):
    category: str
    pure_python: int
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    def __call__(x): ...
    __call__: Incomplete

class ListUtilitiesModule(PluginModule):
    category: Incomplete
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
