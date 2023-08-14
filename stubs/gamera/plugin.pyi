from types import *
from gamera.args import *
from gamera.enums import *
from _typeshed import Incomplete
from gamera import util as util

plugin_methods: Incomplete

class PluginModule:
    category: Incomplete
    cpp_namespaces: Incomplete
    cpp_sources: Incomplete
    cpp_headers: Incomplete
    cpp_defines: Incomplete
    cpp_include_dirs: Incomplete
    extra_libraries: Incomplete
    library_dirs: Incomplete
    define_macros: Incomplete
    extra_compile_args: Incomplete
    extra_link_args: Incomplete
    extra_objects: Incomplete
    functions: Incomplete
    pure_python: bool
    version: str
    author: Incomplete
    url: Incomplete
    stable: bool
    def __init__(self) -> None: ...

class Builtin(PluginModule):
    author: str
    url: str

class PluginFunction:
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete
    image_types_must_match: int
    testable: int
    feature_function: bool
    doc_examples: Incomplete
    category: Incomplete
    pure_python: bool
    progress_bar: str
    author: Incomplete
    add_to_image: bool
    def get_formatted_argument_list(cls): ...
    get_formatted_argument_list: Incomplete
    def escape_docstring(cls): ...
    escape_docstring: Incomplete
    def register(cls) -> None: ...
    register: Incomplete

def PluginFactory(name, category: Incomplete | None = ..., return_type: Incomplete | None = ..., self_type=..., args: Incomplete | None = ...): ...
def get_config_options(command): ...
def methods_flat_category(category, pixel_type: Incomplete | None = ...): ...
