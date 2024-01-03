from _typeshed import Incomplete
from gamera.core import Dim as Dim, Point as Point, Rect as Rect

FUDGE_AMOUNT: int
FUDGE_AMOUNT_2: int

def Fudge(o, amount=...): ...
F = Fudge

class FudgeNumber:
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

class FudgeInt(FudgeNumber, int):
    below: Incomplete
    above: Incomplete
    def __init__(self, value, amount=...) -> None: ...

class FudgeFloat(FudgeNumber, float):
    below: Incomplete
    above: Incomplete
    def __init__(self, value, amount=...) -> None: ...