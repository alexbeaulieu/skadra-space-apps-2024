from dataclasses import dataclass

from filter import FilterParam
@dataclass
class FilterDto:
    name: str
    params: FilterParam