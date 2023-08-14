from gamera.plugin import *
from _typeshed import Incomplete

class Thinning(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class thin_zs(Thinning): ...
class thin_hs(Thinning): ...

class medial_axis_transform_hs(Thinning):
    pure_python: bool
    def __call__(self): ...

class thin_hs_large_image(Thinning):
    pure_python: bool
    def __call__(self): ...
    __call__: Incomplete

class medial_axis_transform_large_image_hs(Thinning):
    pure_python: bool
    def __call__(self): ...

class thin_lc(Thinning): ...

class ThinningModule(PluginModule):
    category: str
    functions: Incomplete
    cpp_headers: Incomplete
    author: str
    url: str

module: Incomplete
