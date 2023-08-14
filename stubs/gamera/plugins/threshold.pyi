from gamera.plugin import *
from _typeshed import Incomplete
from gamera.args import NoneDefault as NoneDefault

class threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(image, threshold, storage_format: int = ...): ...

class otsu_find_threshold(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class otsu_threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(image, storage_format: int = ...): ...

class tsai_moment_preserving_find_threshold(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    author: str

class tsai_moment_preserving_threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    author: str
    def __call__(image, storage_format: int = ...): ...

class abutaleb_threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(image, storage_format: int = ...): ...

class bernsen_threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(image, storage_format: int = ..., region_size: int = ..., contrast_limit: int = ..., doubt_to_black: bool = ...): ...

class djvu_threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(image, smoothness: float = ..., max_block_size: int = ..., min_block_size: int = ..., block_factor: int = ...): ...
    doc_examples: Incomplete

class soft_threshold(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(image, t: Incomplete | None = ..., sigma: float = ..., dist: int = ...): ...
    doc_examples: Incomplete

class soft_threshold_find_sigma(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(image, t, dist: int = ...): ...

class ThresholdModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
