from gamera.plugin import *
from _typeshed import Incomplete

class Feature(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    feature_function: bool
    doc_examples: Incomplete

class black_area(Feature): ...

class moments(Feature):
    return_type: Incomplete

class nholes(Feature):
    return_type: Incomplete

class nholes_extended(Feature):
    return_type: Incomplete

class volume(Feature): ...
class area(Feature): ...
class aspect_ratio(Feature): ...
class nrows_feature(Feature): ...
class ncols_feature(Feature): ...
class compactness(Feature): ...

class volume16regions(Feature):
    return_type: Incomplete

class volume64regions(Feature):
    return_type: Incomplete

class zernike_moments(Feature):
    author: str
    return_type: Incomplete

class zernike_moments_plugin(PluginFunction):
    category: str
    author: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(image, order: int = ...): ...
    __call__: Incomplete

class skeleton_features(Feature):
    return_type: Incomplete

class top_bottom(Feature):
    return_type: Incomplete

class diagonal_projection(Feature):
    return_type: Incomplete
    author: str

class generate_features(PluginFunction):
    category: str
    pure_python: bool
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    cache: Incomplete
    feature_functions: Incomplete
    features: Incomplete
    def __call__(self, features: Incomplete | None = ..., force: bool = ...) -> None: ...
    __call__: Incomplete

class FeaturesModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete

def get_features_length(features): ...
def generate_features_list(list, features: str = ...) -> None: ...
