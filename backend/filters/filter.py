from abc import ABC
from typing import Optional
from dataclasses import dataclass

class Filter(ABC):
    name: str
    params: dict
    
    def process(self, data, params: dict):
        pass