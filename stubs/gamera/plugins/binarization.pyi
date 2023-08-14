from gamera.plugin import *
from _typeshed import Incomplete
from gamera.args import NoneDefault as NoneDefault

class image_mean(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    def __call__(self): ...
    __call__: Incomplete

class image_variance(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    def __call__(self): ...
    __call__: Incomplete

class mean_filter(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, region_size: int = ...): ...
    __call__: Incomplete

class variance_filter(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    def __call__(self, means, region_size: int = ...): ...
    __call__: Incomplete

class wiener_filter(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, region_size: int = ..., noise_variance: int = ...): ...
    __call__: Incomplete

class niblack_threshold(PluginFunction):
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, region_size: int = ..., sensitivity: float = ..., lower_bound: int = ..., upper_bound: int = ...): ...
    __call__: Incomplete

class sauvola_threshold(PluginFunction):
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, region_size: int = ..., sensitivity: float = ..., dynamic_range: int = ..., lower_bound: int = ..., upper_bound: int = ...): ...
    __call__: Incomplete

class gatos_background(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    def __call__(self, binarization, region_size: int = ...): ...
    __call__: Incomplete

class gatos_threshold(PluginFunction):
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    def __call__(self, background, binarization, q: float = ..., p1: float = ..., p2: float = ...): ...
    __call__: Incomplete

class white_rohrer_threshold(PluginFunction):
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    author: str
    doc_examples: Incomplete
    def __call__(self, x_lookahead: int = ..., y_lookahead: int = ..., bias_mode: int = ..., bias_factor: int = ..., f_factor: int = ..., g_factor: int = ...): ...
    __call__: Incomplete

class shading_subtraction(PluginFunction):
    author: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, k: int = ..., threshold: Incomplete | None = ...): ...
    __call__: Incomplete

class brink_threshold(PluginFunction):
    author: str
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(self): ...
    __call__: Incomplete

class BinarizationGenerator(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
