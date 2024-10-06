from abc import ABC

class Algorithm(ABC):
    name: str
    
    def process(self, data):
        pass