from _typeshed import Incomplete
from gamera.args import Args as Args, Check as Check, Int as Int
from gamera.knn import kNNInteractive as kNNInteractive
from gamera.util import ProgressFactory as ProgressFactory

class AlgoRegistry:
    algorithms: Incomplete
    def registerData(algoData) -> None: ...
    registerData: Incomplete
    def register(name, callable, args=..., doc: str = ...) -> None: ...
    register: Incomplete

class AlgoData:
    name: Incomplete
    callable: Incomplete
    args: Incomplete
    doc: Incomplete
    def __init__(self, name, callable, args=..., doc: str = ...) -> None: ...

class EditingAlgorithm:
    def __init__(self) -> None: ...

class EditMnn(EditingAlgorithm):
    name: str
    args: Incomplete
    def __call__(self, classifier, k: int = ..., protectRare: bool = ..., rareThreshold: int = ...): ...

edit_mnn: Incomplete

class EditCnn(EditingAlgorithm):
    name: str
    args: Incomplete
    def __call__(self, classifier, k: int = ..., randomize: bool = ...): ...

edit_cnn: Incomplete

class EditMnnCnn(EditingAlgorithm):
    name: str
    args: Incomplete
    def __call__(self, classifier, k: int = ..., protectRare: bool = ..., rareThreshold: int = ..., randomize: bool = ...): ...

edit_mnn_cnn: Incomplete
