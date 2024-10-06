from filters.filter import Filter
from obspy.signal.filter import  highpass

class HighpassFilter(Filter):
    name = "Highpass Filter"
    params = dict(
        frequency=0.1,
        filter_order= 4,
        zerophase=0
    )
    
    def process(self, data, params: dict):
        data_out = data.copy()

        freq = 1/data["velocity"].index.diff().median().total_seconds()

        data_out["velocity"] = highpass(data_out, params["frequency"], freq, params["filter_order"], params["zerophase"])

        return data_out