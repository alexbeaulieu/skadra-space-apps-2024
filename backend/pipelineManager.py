import copy
from typing import List

from filter import Filter
from filterDto import FilterDto
from flask import g


class PipelineManager:
    def __init__(self):
        self.filters = [] # List of filters

    def add_filter(self, filter: Filter):
        self.filters.append(filter)

    def process(self, order: List[FilterDto], data):
        pipe = copy.deepcopy(data)
        for filter_dto in order:
            filter = next((f for f in self.filters if f.name == filter_dto.name), None)
            if filter is None:
                raise ValueError(f"Filter {filter_dto.name} not found in the list of filters")
            pipe = filter.process(pipe, **filter_dto.params)
        return pipe
    
    
def pipeline_manager():
    if 'pipeline_manager' not in g:
        g.pipeline_manager = PipelineManager()
    return g.pipeline_manager