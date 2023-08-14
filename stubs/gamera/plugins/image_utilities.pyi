from gamera.plugin import *
from _typeshed import Incomplete
from gamera.args import NoneDefault as NoneDefault
from gamera.gui import has_gui as has_gui

class image_copy(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    def __call__(image, storage_format: int = ...): ...
    __call__: Incomplete

class image_save(PluginFunction):
    pure_python: int
    category: str
    self_type: Incomplete
    args: Incomplete
    def __call__(image, name, format) -> None: ...
    __call__: Incomplete

class histogram(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete
    def __call__(image): ...
    __call__: Incomplete

class union_images(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class fill_white(PluginFunction):
    category: str
    self_type: Incomplete

class fill(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete

class pad_image_default(PluginFunction):
    category: Incomplete
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class pad_image(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, top, right, bottom, left, value: Incomplete | None = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class trim_image(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(self, PixelValue: Incomplete | None = ...): ...
    __call__: Incomplete

class invert(PluginFunction):
    category: str
    self_type: Incomplete
    doc_examples: Incomplete

class clip_image(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete

class mask(PluginFunction):
    category: str
    return_type: Incomplete
    self_type: Incomplete
    args: Incomplete

class to_nested_list(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete

class nested_list_to_image(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(l, t: int = ...): ...
    __call__: Incomplete

class diff_images(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(self, other): ...
    __call__: Incomplete

class mse(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class reset_onebit_image(PluginFunction):
    category: str
    self_type: Incomplete
    author: str

class ccs_from_labeled_image(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete
    author: str

class min_max_location(PluginFunction):
    category: str
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    author: str
    doc_examples: Incomplete
    def __call__(self, mask: Incomplete | None = ...): ...
    __call__: Incomplete

class min_max_location_nomask(PluginFunction):
    category: Incomplete
    self_type: Incomplete
    return_type: Incomplete
    author: str

class UtilModule(PluginModule):
    cpp_headers: Incomplete
    category: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
