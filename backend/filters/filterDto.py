from dataclasses import dataclass

from filters.filter import FilterParam



@dataclass
class FilterDto:
    name: str
    params: FilterParam