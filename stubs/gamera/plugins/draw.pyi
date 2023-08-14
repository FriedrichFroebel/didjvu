from gamera.plugin import *
from _typeshed import Incomplete
from gamera.core import RGBPixel as RGBPixel
from gamera.util import warn_deprecated as warn_deprecated

class draw_marker(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    author: str
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class draw_line(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    author: str
    def __call__(self, start, end, value, thickness: float = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class draw_hollow_rect(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    def __call__(self, *args): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class draw_filled_rect(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    def __call__(self, *args): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class draw_bezier(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    def __call__(self, start, c1, c2, end, value, accuracy: float = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class draw_circle(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    author: str
    def __call__(self, c, r, value, thickness: float = ..., accuracy: float = ...): ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class draw_text(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    author: str
    pure_python: bool
    def __call__(self, p, text, color, size: int = ..., font_family: int = ..., italic: bool = ..., bold: bool = ..., halign: int = ...) -> None: ...
    __call__: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class flood_fill(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete

class remove_border(PluginFunction):
    self_type: Incomplete

class highlight(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    def __doc_example1__(images): ...
    doc_examples: Incomplete

class DrawModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
