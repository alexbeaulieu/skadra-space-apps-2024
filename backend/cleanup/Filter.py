from abc import ABC


class Filter(ABC):
    name: str
    
    def process(self, data):
        pass