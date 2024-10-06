from dataclasses import dataclass

@dataclass
class FilterDto:
    name: str
    params: dict