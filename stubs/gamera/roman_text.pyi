from _typeshed import Incomplete
from gamera import core as core

class Page:
    sections: Incomplete
    image: Incomplete
    glyphs: Incomplete
    section_search_size: int
    def __init__(self, image, glyphs) -> None: ...
    def segment(self) -> None: ...
    def find_lines(self) -> None: ...
    def find_sections(self): ...
    def display_sections(self, clear: int = ...) -> None: ...
    def display_lines(self, clear: int = ...) -> None: ...
    def display_glyphs(self, clear: int = ...) -> None: ...
    def display_segmentation(self) -> None: ...

class Section:
    bbox: Incomplete
    lines: Incomplete
    glyphs: Incomplete
    avg_glyph_area: int
    avg_glyph_height: int
    avg_glyph_width: int
    avg_line_height: int
    agv_line_width: int
    def __init__(self, bbox) -> None: ...
    def find_tall_glyphs(self, stdev: int = ...): ...
    def add_line(self, line): ...
    def add_glyph(self, glyph) -> None: ...
    def calculate_bbox(self) -> None: ...
    def calculate_stats(self) -> None: ...
    def calculate_glyph_stats(self) -> None: ...
    avg_line_width: Incomplete
    def calculate_line_stats(self) -> None: ...
    def find_lines(self) -> None: ...

class Line:
    center: int
    bbox: Incomplete
    glyphs: Incomplete
    def __init__(self, glyph) -> None: ...
    def add_glyph(self, glyph): ...
    def calculate_stats(self) -> None: ...
    def contains_glyph(self, glyph): ...
    def merge(self, line) -> None: ...

def name_lookup_old(id_name): ...
def name_lookup_unicode(id_name): ...
def make_string(lines, name_lookup_func=...): ...
def output(lines, filename: str = ...) -> None: ...
def ocr(image, classifier: Incomplete | None = ..., glyphs: Incomplete | None = ...): ...