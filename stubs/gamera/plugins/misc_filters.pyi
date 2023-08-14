from gamera.plugin import *
from _typeshed import Incomplete

class rank(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    doc_examples: Incomplete
    def __call__(self, rank, k: int = ..., border_treatment: int = ...): ...
    __call__: Incomplete

class mean(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, k: int = ..., border_treatment: int = ...): ...
    __call__: Incomplete

class min_max_filter(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    doc_examples: Incomplete
    def __call__(self, k: int = ..., filter: int = ..., k_vertical: int = ...): ...
    __call__: Incomplete

class create_gabor_filter(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    doc_examples: Incomplete
    def __call__(self, orientation: float = ..., frequency: float = ..., direction: int = ...): ...
    __call__: Incomplete

class kfill(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    author: str
    args: Incomplete
    def __call__(self, k: int = ..., iterations: int = ...): ...
    __call__: Incomplete

class kfill_modified(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    author: str
    args: Incomplete
    def __call__(self, k: int = ...): ...
    __call__: Incomplete

class MiscFiltersModule(PluginModule):
    category: str
    functions: Incomplete
    cpp_headers: Incomplete
    author: str
    url: str

module: Incomplete
