import copy
from typing import List

from filters.filter import Filter
from filters.filterDto import FilterDto

class PipelineManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PipelineManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.filters = [] # List of filters

    def add_filter(self, filter: Filter):
        self.filters.append(filter)
        
    def get_filters(self):
        return self.filters

    def process(self, order: List[FilterDto], data):
        for filter_dto in order:
            filter = next((f for f in self.filters if f.name == filter_dto.name), None)
            if filter is None:
                raise ValueError(f"Filter {filter_dto.name} not found in the list of filters")
            data = filter.process(data, filter_dto.params)
        return data
    
    
