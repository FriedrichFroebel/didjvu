from gamera.plugin import *
from _typeshed import Incomplete
from gamera import util as util
from gamera.plugins import image_utilities as image_utilities

CONVOLUTION_TYPES: Incomplete

class convolve(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, kernel, border_treatment: int = ...): ...
    __call__: Incomplete

class convolve_xy(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    def __call__(self, kernel_x, kernel_y: Incomplete | None = ..., border_treatment: int = ...): ...
    __call__: Incomplete

class convolve_x(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, kernel, border_treatment: int = ...): ...
    __call__: Incomplete

class convolve_y(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    def __call__(self, kernel, border_treatment: int = ...): ...
    __call__: Incomplete

class ConvolutionKernel(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    category: str

class GaussianKernel(ConvolutionKernel):
    args: Incomplete

class GaussianDerivativeKernel(ConvolutionKernel):
    args: Incomplete

class BinomialKernel(ConvolutionKernel):
    args: Incomplete

class AveragingKernel(ConvolutionKernel):
    args: Incomplete

class SymmetricGradientKernel(ConvolutionKernel):
    args: Incomplete

class SimpleSharpeningKernel(ConvolutionKernel):
    args: Incomplete

class gaussian_smoothing(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, std_dev: float = ...): ...
    __call__: Incomplete

class simple_sharpen(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, sharpening_factor: float = ...): ...
    __call__: Incomplete

class gaussian_gradient(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, scale: float = ...): ...
    __call__: Incomplete

class laplacian_of_gaussian(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, scale: float = ...): ...
    __call__: Incomplete

class hessian_matrix_of_gaussian(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, scale: float = ...): ...
    __call__: Incomplete

class sobel_edge_detection(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    pure_python: bool
    doc_examples: Incomplete
    def __call__(self, scale: float = ...): ...
    __call__: Incomplete

class ConvolutionModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
BORDER_TREATMENT_AVOID: int
BORDER_TREATMENT_CLIP: int
BORDER_TREATMENT_REPEAT: int
BORDER_TREATMENT_REFLECT: int
BORDER_TREATMENT_WRAP: int
