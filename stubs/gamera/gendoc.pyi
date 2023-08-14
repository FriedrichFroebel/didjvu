from gamera.enums import *
from _typeshed import Incomplete
from collections.abc import Generator
from gamera import args as args, core as core, paths as paths, plugin as plugin, util as util
from gamera.plugins import png_support as png_support, tiff_support as tiff_support

html_formatter: Incomplete

def code_block(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine): ...
def cmp(a, b): ...
def sort_lowercase(a, b): ...
def sort_firstitem_lowercase(a, b): ...
def underline(level, s, extra: int = ...): ...

class DocumentationGenerator:
    test_mode: Incomplete
    classes: Incomplete
    plugins: Incomplete
    sourceforge_logo: Incomplete
    contact_url: Incomplete
    def __init__(self, root_path: str = ..., test_mode: bool = ..., classes=..., plugins: Incomplete | None = ..., sourceforge_logo: bool = ..., contact_url: str = ...) -> None: ...
    root_path: Incomplete
    src_path: Incomplete
    src_images_path: Incomplete
    icons_path: Incomplete
    output_path: Incomplete
    output_images_path: Incomplete
    def set_paths(self, root) -> None: ...
    def generate(self) -> None: ...
    def generate_generic_pngs(self) -> None: ...
    def copy_css(self, input_path, output_path) -> None: ...
    def copy_images(self, src_paths, output_path) -> None: ...
    def get_rest_docs(self) -> Generator[Incomplete, None, None]: ...
    def convert_to_html(self) -> None: ...

class PluginDocumentationGenerator:
    docgen: Incomplete
    def __init__(self, docgen, plugins: Incomplete | None = ...) -> None: ...
    def get_generic_images(): ...
    get_generic_images: Incomplete
    def get_methods(plugins): ...
    get_methods: Incomplete
    def recurse(self, methods, level, images, s: Incomplete | None = ...) -> None: ...
    def table_of_contents(self, methods): ...
    def method_doc(self, func, level, images, s) -> None: ...
    def run_example(self, func, images): ...
    def method_example(self, func, level, images, s) -> None: ...
    def save_image(self, image, filename) -> None: ...
    def write_image(self, s, filename, tag: str = ...) -> None: ...

class ClassDocumentationGenerator:
    docgen: Incomplete
    class_names: Incomplete
    def __init__(self, docgen, classes) -> None: ...
    def document_class(self, cls_desc) -> None: ...
    def table_of_contents(self, classes): ...

def docstring(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine): ...
def copy_images(path_obj) -> None: ...

class Paths:
    root_path: Incomplete
    src_path: Incomplete
    src_images_path: Incomplete
    icons_path: Incomplete
    output_path: Incomplete
    output_images_path: Incomplete
    def __init__(self, root: str = ...) -> None: ...

def print_usage() -> None: ...
def gendoc(classes=..., plugins: Incomplete | None = ..., sourceforge_logo: bool = ..., contact_url: str = ...) -> None: ...
