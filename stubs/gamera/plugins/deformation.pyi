from gamera.plugin import *
from gamera.core import *
from _typeshed import Incomplete
from gamera.core import RGBPixel as RGBPixel

class wave(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    def __call__(self, amplitude, period, direction, waveform_type: int = ..., offset: int = ..., turbulence: float = ..., random_seed: int = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class noise(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, amplitude, direction, random_seed: int = ...): ...
    __call__: Incomplete

class inkrub(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, transcription_prob, random_seed: int = ...): ...
    __call__: Incomplete

class ink_diffuse(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete
    def __call__(self, diffusion_type, exponential_decay_constant, random_seed: int = ...): ...
    __call__: Incomplete

class degrade_kanungo(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    doc_examples: Incomplete

class white_speckles(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    doc_examples: Incomplete

class DefModule(PluginModule):
    cpp_headers: Incomplete
    category: str
    functions: Incomplete
    author: str
    url: str

module: Incomplete
