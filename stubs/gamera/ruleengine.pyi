from .fudge import Fudge as Fudge
from _typeshed import Incomplete
from gamera import group as group, util as util

class RuleEngineError(Exception): ...

class RuleEngine:
    rules: Incomplete
    def __init__(self, rules=..., reapply: int = ...) -> None: ...
    def add_rule(self, rule) -> None: ...
    def get_rules(self): ...
    def perform_rules(self, glyphs, grid_size: int = ..., recurse: int = ..., progress: Incomplete | None = ..., _recursion_level: int = ...): ...