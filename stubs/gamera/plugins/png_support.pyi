from gamera.plugin import *
from _typeshed import Incomplete

class PNG_info(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class load_PNG(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(filename, compression: int = ...): ...
    __call__: Incomplete
    exts: Incomplete

class save_PNG(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    exts: Incomplete

class PngSupportModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    internal_png_dir: str
    internal_zlib_dir: str
    cpp_sources: Incomplete
    cpp_include_dirs: Incomplete
    extra_libraries: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
