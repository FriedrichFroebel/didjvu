from gamera.gui.gaoptimizer.ExpertSettingPanel import *
from gamera.gui.gaoptimizer.SelectionPanel import *
from gamera.gui.gaoptimizer.CrossoverPanel import *
from gamera.gui.gaoptimizer.MutationPanel import *
from gamera.gui.gaoptimizer.ReplacementPanel import *
from gamera.gui.gaoptimizer.StopCriteriaPanel import *
from gamera.gui.gaoptimizer.ParallelizationPanel import *
import threading
import wx
from _typeshed import Incomplete
from gamera import knnga as knnga
from gamera.gui import gui_util as gui_util

class GAWorker(threading.Thread):
    GAOptimizer: Incomplete
    frame: Incomplete
    def __init__(self, GAOptimizer, frame) -> None: ...
    def run(self) -> None: ...

class GAInitialLOOWorker(threading.Thread):
    classifier: Incomplete
    frame: Incomplete
    def __init__(self, classifier, frame) -> None: ...
    def run(self) -> None: ...

class SettingsPanel(wx.ScrolledWindow):
    frame: Incomplete
    workerThread: Incomplete
    initLOO: Incomplete
    selectingLabel: str
    weightingLabel: str
    featureSelection: Incomplete
    featureWeighting: Incomplete
    normalization: Incomplete
    popSize: Incomplete
    crossoverRate: Incomplete
    mutationRate: Incomplete
    startButton: Incomplete
    stopButton: Incomplete
    def __init__(self, parent, id, frame) -> None: ...
    selectionPanel: Incomplete
    crossoverPanel: Incomplete
    mutationPanel: Incomplete
    replacementPanel: Incomplete
    stopCriteriaPanel: Incomplete
    parallelizationPanel: Incomplete
    def MakeExpertPane(self, pane) -> None: ...
    def OnPaneChanged(self, event) -> None: ...
    def OnOpModeChange(self, event) -> None: ...
    def TriggerWidgetsInPanel(self, panel, widget, state) -> None: ...
    def OnButton(self, event) -> None: ...
    def startCalculation(self) -> None: ...
    def stopCalculation(self): ...
