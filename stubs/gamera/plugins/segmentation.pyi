from gamera.plugin import *
from _typeshed import Incomplete
from gamera import util as util

class Segmenter(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class cc_analysis(Segmenter): ...

class cc_and_cluster(Segmenter):
    pure_python: bool
    args: Incomplete
    return_type: Incomplete
    def __call__(image, ratio: float = ..., distance: int = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class splitx(Segmenter):
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, center: float = ...): ...
    __call__: Incomplete
    author: str

class splitx_max(Segmenter):
    args: Incomplete
    def __call__(self, center: float = ...): ...
    __call__: Incomplete
    author: str

class splity(Segmenter):
    args: Incomplete
    def __call__(self, center=...): ...
    __call__: Incomplete
    author: str

class splitx_base(Segmenter):
    pure_python: bool
    return_type: Incomplete

class splitx_left(splitx_base):
    def __call__(self): ...
    __call__: Incomplete

class splitx_right(splitx_base):
    def __call__(self): ...
    __call__: Incomplete

class splity_base(Segmenter):
    pure_python: bool
    return_type: Incomplete

class splity_top(splity_base):
    def __call__(self): ...
    __call__: Incomplete

class splity_bottom(splity_base):
    def __call__(self): ...
    __call__: Incomplete

def filter_wide(ccs, max_width): ...
def filter_narrow(ccs, min_width): ...
def filter_tall(ccs, max_height): ...
def filter_short(ccs, min_height): ...
def filter_small(ccs, min_size): ...
def filter_large(ccs, max_size): ...
def filter_black_area_small(ccs, min_size): ...
def filter_black_area_large(ccs, max_size): ...

class SegmentationModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
