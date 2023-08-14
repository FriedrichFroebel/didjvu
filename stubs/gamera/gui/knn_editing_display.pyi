from _typeshed import Incomplete
from gamera.gui import compat_wx as compat_wx
from gamera.knn_editing import AlgoRegistry as AlgoRegistry

class EditingDialog:
    selection: int
    panel: Incomplete
    def __init__(self) -> None: ...
    def show(self, classifier): ...
