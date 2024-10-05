import copy
from typing import List

from Filter import Filter


class PipelineManager:
    def __init__(self):
        self.filters = [] # List of filters
        
    def add_filter(self, filter: Filter):
        self.filters.append(filter)

    def process(self, order: List[str], data):
        pipe = copy.deepcopy(data)
        filters_sorted = sorted(self.filters, key=lambda f: order.index(f.name))
        for filter in filters_sorted:
            pipe = filter.process(pipe)
        return pipe