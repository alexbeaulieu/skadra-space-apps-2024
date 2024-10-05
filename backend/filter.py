from abc import ABC
from typing import Optional
from dataclasses import dataclass

@dataclass
class FilterParam:
    max_value: Optional[int]
    min_value: Optional[int]
    bool_value: Optional[bool]
    col_name: Optional[str]

class Filter(ABC):
    name: str
    params: FilterParam
    
    def process(self, data, params: FilterParam):
        pass