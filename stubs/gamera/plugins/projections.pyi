from gamera.plugin import *
from _typeshed import Incomplete

class projection_rows(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class projection_cols(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class projections(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    pure_python: int
    def __call__(image): ...
    __call__: Incomplete

class projection_skewed_cols(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, angles): ...
    __call__: Incomplete
    doc_examples: Incomplete

class projection_skewed_rows(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, angles): ...
    __call__: Incomplete
    doc_examples: Incomplete

class rotation_angle_projections(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    pure_python: int
    def __call__(self, minangle: float = ..., maxangle: float = ..., accuracy: int = ...): ...
    __call__: Incomplete

class diagonal_projections(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    pure_python: int
    def __call__(image): ...
    __call__: Incomplete

class ProjectionsModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
