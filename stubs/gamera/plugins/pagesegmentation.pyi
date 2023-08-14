from gamera.plugin import *
from _typeshed import Incomplete
from gamera.plugins.listutilities import argmax as argmax, kernel_density as kernel_density

class projection_cutting(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(image, Tx: int = ..., Ty: int = ..., noise: int = ..., gap_treatment: int = ...): ...
    __call__: Incomplete

class runlength_smearing(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    def __call__(image, Cx: int = ..., Cy: int = ..., Csm: int = ...): ...
    __call__: Incomplete

class bbox_merging(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    pure_python: bool
    author: str
    ccs: Incomplete
    indices: Incomplete
    rect: Incomplete
    def __call__(self, Ex: int = ..., Ey: int = ..., iterations: int = ...): ...
    __call__: Incomplete

class kise_block_extraction(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    pure_python: bool
    author: str
    cc1: Incomplete
    cc2: Incomplete
    d: Incomplete
    ar: Incomplete
    def __call__(self, Ta: float = ..., fr: float = ...): ...
    __call__: Incomplete

class sub_cc_analysis(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str

class textline_reading_order(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    pure_python: bool
    author: str
    segment: Incomplete
    label: int
    def __call__(lineccs): ...
    __call__: Incomplete

class segmentation_error(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str

class PageSegmentationModule(PluginModule):
    cpp_headers: Incomplete
    cpp_namespace: Incomplete
    category: str
    functions: Incomplete

module: Incomplete
