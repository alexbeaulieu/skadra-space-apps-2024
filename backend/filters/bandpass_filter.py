from filters.filter import Filter
from scipy.signal import butter, lfilter

class BandpassFilter(Filter):
    name = "Bandpass Filter"
    params = dict(
        active= True,
        bool_value= None,
        col_name= None,
        max_value= 10,
        min_value= 0,
        order= 4,
    )


    def process(self, data, params: dict):
        fs = 1/data["velocity"].index.diff().median().total_seconds()

        b, a = butter(params["order"], [params["min_value"], params["max_value"]], fs=fs, btype='band')

        data_out = data.copy()
        data_out["velocity"] = lfilter(b, a, data["velocity"].fillna(method='ffill'))

        return data_out