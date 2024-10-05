from dataclasses import dataclass
from typing import Optional

@dataclass
class FilterParamDto:
    max_value: Optional[int]
    min_value: Optional[int]
    bool_value: Optional[bool]
    col_name: Optional[str]