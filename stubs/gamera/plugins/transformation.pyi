from gamera.plugin import *
from _typeshed import Incomplete
from gamera.args import NoneDefault as NoneDefault
from gamera.core import RGBPixel as RGBPixel
from gamera.gui import has_gui as has_gui
from gamera.util import warn_deprecated as warn_deprecated

class rotate(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    author: str
    def __call__(self, angle, bgcolor: Incomplete | None = ..., order: int = ...): ...
    __call__: Incomplete

class resize(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class scale(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class shear_row(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete

class shear_column(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete

class mirror_horizontal(PluginFunction):
    category: str
    self_type: Incomplete
    doc_examples: Incomplete

class mirror_vertical(PluginFunction):
    category: str
    self_type: Incomplete
    doc_examples: Incomplete

class grey_convert(PluginFunction):
    category: str
    author: str
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete

class TransformationModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
