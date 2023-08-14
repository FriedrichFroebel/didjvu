from gamera.plugin import *
from _typeshed import Incomplete
from gamera.args import NoneDefault as NoneDefault
from gamera.core import RGBPixel as RGBPixel

class voronoi_from_labeled_image(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete
    author: str

class voronoi_from_points(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete
    author: str

class labeled_region_neighbors(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, eight_connectivity: bool = ...): ...
    __call__: Incomplete

class delaunay_from_points(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str

class graph_color_ccs(PluginFunction):
    category: str
    author: str
    args: Incomplete
    self_type: Incomplete
    return_type: Incomplete
    def __call__(image, ccs, colors: Incomplete | None = ..., method: int = ..., unique: bool = ...): ...
    __call__: Incomplete

class convex_hull_from_points(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str

class convex_hull_as_points(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str

class convex_hull_as_image(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    doc_examples: Incomplete
    def __call__(image, filled: bool = ...): ...
    __call__: Incomplete

class max_empty_rect(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class hough_lines(PluginFunction):
    author: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete

class GeometryModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    cpp_sources: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
