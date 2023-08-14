from gamera.plugin import *
from _typeshed import Incomplete

class tiff_info(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class load_tiff(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(filename, compression: int = ...): ...
    __call__: Incomplete
    exts: Incomplete

class save_tiff(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    exts: Incomplete

class TiffSupportModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    cpp_include_dirs: Incomplete
    extra_libraries: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
