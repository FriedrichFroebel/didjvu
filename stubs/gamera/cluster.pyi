from _typeshed import Incomplete
from gamera import core as core, gamera_xml as gamera_xml, graph as graph, knn as knn

def get_lengths(node, depth, lengths, cur_depth: int = ..., path=...) -> None: ...
def label(graph, node, label_start, label) -> None: ...
def make_subtrees_stddev(graph, ratio, distance, relabel: int = ..., lab: str = ...): ...
def make_spanning_tree(glyphs, k: Incomplete | None = ...): ...
def cluster(glyphs, ratio: float = ..., distance: int = ..., label: str = ..., k: Incomplete | None = ..., relabel: int = ...): ...
def cluster2(glyphs): ...
def do_tests(filename) -> None: ...
def make_unique_names(glyphs) -> None: ...
def graphvis_output(G, filename) -> None: ...