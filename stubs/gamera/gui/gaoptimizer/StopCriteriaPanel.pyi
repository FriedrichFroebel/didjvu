from gamera.gui.gaoptimizer.ExpertSettingPanel import *
from _typeshed import Incomplete
from gamera.gui import compat_wx as compat_wx

class StopCriteriaPanel(ExpertSettingPanel):
    bestFitness: Incomplete
    maxGeneration: Incomplete
    maxGenerationCount: Incomplete
    maxFitnessEval: Incomplete
    maxFitnessEvalCount: Incomplete
    steadyContinue: Incomplete
    steadyContinueMin: Incomplete
    steadyContinueNoChange: Incomplete
    def __init__(self, parent, id) -> None: ...
