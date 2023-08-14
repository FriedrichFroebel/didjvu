from gamera.gui.gaoptimizer.ExpertSettingPanel import *
from _typeshed import Incomplete
from gamera.gui import compat_wx as compat_wx

class MutationPanel(ExpertSettingPanel):
    shiftMutation: Incomplete
    swapMutation: Incomplete
    inversionOrderMutation: Incomplete
    binaryMutation: Incomplete
    binaryMutationRate: Incomplete
    gaussMutation: Incomplete
    gaussMutationSigma: Incomplete
    gaussMutationPchance: Incomplete
    def __init__(self, parent, id) -> None: ...
