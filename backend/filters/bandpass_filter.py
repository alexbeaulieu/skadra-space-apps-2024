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
    
    def calc_sampling_freq(df):
        t_s = df["velocity"].index.diff().median().total_seconds()

        return 1/t_s

    def process(self, data, params: dict):
        print(data)
        #fs = self.calc_sampling_freq(data)
        fs = 1/data["velocity"].index.diff().median().total_seconds()

        b, a = butter(params["order"], [params["min_value"], params["max_value"]], fs=fs, btype='band')

        data_out = data.copy()
        data_out["velocity"] = lfilter(b, a, data["velocity"])

        return data_out