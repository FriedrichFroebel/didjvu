import wx
from _typeshed import Incomplete
from gamera.gui import compat_wx as compat_wx, gui_util as gui_util, toolbar as toolbar

class RuleEngineRunnerTree(wx.TreeCtrl):
    toplevel: Incomplete
    modules: Incomplete
    undo_history: Incomplete
    added: Incomplete
    removed: Incomplete
    root: Incomplete
    def __init__(self, toplevel, parent) -> None: ...
    def add_module(self, module) -> None: ...

class RuleEngineRunnerPanel(wx.Panel):
    toplevel: Incomplete
    toolbar: Incomplete
    tree: Incomplete
    def __init__(self, toplevel, parent: Incomplete | None = ..., id: int = ...) -> None: ...
    def open_module(self, filename) -> None: ...
