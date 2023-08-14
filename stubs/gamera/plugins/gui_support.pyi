from gamera.plugin import *
from _typeshed import Incomplete

class to_string(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete

class to_buffer(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete

class draw_cc(PluginFunction):
    self_type: Incomplete
    args: Incomplete

class to_buffer_colorize(PluginFunction):
    self_type: Incomplete
    args: Incomplete

class color_ccs(PluginFunction):
    author: str
    args: Incomplete
    category: str
    self_type: Incomplete
    return_type: Incomplete
    def __call__(image, ignore_unlabeled: bool = ...): ...
    __call__: Incomplete

class GuiSupportModule(PluginModule):
    category: Incomplete
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
