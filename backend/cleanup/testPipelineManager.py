import unittest
from unittest.mock import MagicMock

import pandas as pd

from Filter import Filter
from PipelineManager import PipelineManager

# Assuming the Filter and PipelineManager classes are defined in a module named pipeline


class MockFilterA(Filter):
    def process(self, data):
        data['A'] = data['A'] + 1
        return data

class MockFilterB(Filter):
    def process(self, data):
        data['B'] = data['B'] * 2
        return data
    
class TestPipelineManager(unittest.TestCase):
    def setUp(self):
        self.manager = PipelineManager()
        self.manager.available_filters = {
            "MockFilterA": MockFilterA,
            "MockFilterB": MockFilterB
        }
        self.data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

    def test_sequencing_filter_a_then_b(self):
        order_of_operations = ["MockFilterA", "MockFilterB"]
        result = self.manager.process(order_of_operations, self.data.copy())
        expected = pd.DataFrame({
            'A': [2, 3, 4],
            'B': [8, 10, 12]
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_sequencing_filter_b_then_a(self):
        order_of_operations = ["MockFilterB", "MockFilterA"]
        result = self.manager.process(order_of_operations, self.data.copy())
        expected = pd.DataFrame({
            'A': [2, 3, 4],
            'B': [8, 10, 12]
        })
        pd.testing.assert_frame_equal(result, expected)

if __name__ == "__main__":
    unittest.main()