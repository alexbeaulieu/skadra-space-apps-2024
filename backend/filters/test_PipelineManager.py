import pytest
import pandas as pd
from unittest.mock import MagicMock

from pipelineManager import PipelineManager
from filters.filter import Filter
from filters.filterDto import FilterDto


def test_process_with_single_filter():
    manager = PipelineManager()
    filter = MagicMock(spec=Filter)
    filter.name = "SampleFilter"
    filter.process.return_value = pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    })
    manager.add_filter(filter)
    
    order = [FilterDto(name="SampleFilter", params={})]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    result = manager.process(order, data)
    filter.process.assert_called_once()
    assert result.equals(pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    }))


def test_process_with_multiple_filters():
    manager = PipelineManager()
    
    filter1 = MagicMock(spec=Filter)
    filter1.name = "Filter1"
    filter1.process.return_value = pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    })
    
    filter2 = MagicMock(spec=Filter)
    filter2.name = "Filter2"
    filter2.process.return_value = pd.DataFrame({
        'column1': [1],
        'column2': [4]
    })
    
    manager.add_filter(filter1)
    manager.add_filter(filter2)
    
    order = [FilterDto(name="Filter1", params={}), FilterDto(name="Filter2", params={})]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    result = manager.process(order, data)
    filter1.process.assert_called_once()
    filter2.process.assert_called_once()
    assert result.equals(pd.DataFrame({
        'column1': [1],
        'column2': [4]
    }))


def test_process_with_reversed_filter_order():
    manager = PipelineManager()
    
    filter1 = MagicMock(spec=Filter)
    filter1.name = "Filter1"
    filter1.process.return_value = pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    })
    
    filter2 = MagicMock(spec=Filter)
    filter2.name = "Filter2"
    filter2.process.return_value = pd.DataFrame({
        'column1': [1],
        'column2': [4]
    })
    
    manager.add_filter(filter1)
    manager.add_filter(filter2)
    
    order = [FilterDto(name="Filter2", params={}), FilterDto(name="Filter1", params={})]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    result = manager.process(order, data)
    filter2.process.assert_called_once()
    filter1.process.assert_called_once()
    assert result.equals(pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    }))


def test_process_with_nonexistent_filter():
    manager = PipelineManager()
    
    filter1 = MagicMock(spec=Filter)
    filter1.name = "Filter1"
    filter1.process.return_value = pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    })
    
    manager.add_filter(filter1)
    
    order = [FilterDto(name="NonExistentFilter", params={})]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    with pytest.raises(ValueError, match="Filter NonExistentFilter not found in the list of filters"):
        manager.process(order, data)


def test_process_with_empty_filter_list():
    manager = PipelineManager()
    
    order = [FilterDto(name="NonExistentFilter", params={})]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    with pytest.raises(ValueError, match="Filter NonExistentFilter not found in the list of filters"):
        manager.process(order, data)


def test_process_with_filter_params():
    manager = PipelineManager()
    
    filter = MagicMock(spec=Filter)
    filter.name = "SampleFilter"
    filter.process.return_value = pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    })
    manager.add_filter(filter)
    
    order = [FilterDto(name="SampleFilter", params={"param1": "value1", "param2": "value2"})]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    result = manager.process(order, data)
    filter.process.assert_called_once_with(data, param1="value1", param2="value2")
    assert result.equals(pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    }))


def test_process_with_multiple_filters_and_params():
    manager = PipelineManager()
    
    filter1 = MagicMock(spec=Filter)
    filter1.name = "Filter1"
    filter1.process.return_value = pd.DataFrame({
        'column1': [1, 2],
        'column2': [4, 5]
    })
    
    filter2 = MagicMock(spec=Filter)
    filter2.name = "Filter2"
    filter2.process.return_value = pd.DataFrame({
        'column1': [1],
        'column2': [4]
    })
    
    manager.add_filter(filter1)
    manager.add_filter(filter2)
    
    order = [
        FilterDto(name="Filter1", params={"param1": "value1"}),
        FilterDto(name="Filter2", params={"param2": "value2"})
    ]
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': [4, 5, 6]
    })
    
    result = manager.process(order, data)
    filter1.process.assert_called_once_with(data, param1="value1")
    filter2.process.assert_called_once_with(filter1.process.return_value, param2="value2")
    assert result.equals(pd.DataFrame({
        'column1': [1],
        'column2': [4]
    }))


if __name__ == "__main__":
    test_process_with_single_filter()
    test_process_with_multiple_filters()
    test_process_with_reversed_filter_order()
    test_process_with_nonexistent_filter()
    test_process_with_empty_filter_list()
    test_process_with_filter_params()
    test_process_with_multiple_filters_and_params()
    print("All tests passed.")


