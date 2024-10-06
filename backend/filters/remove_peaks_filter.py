from filters.filter import Filter
from scipy.signal import find_peaks

class RemovePeaksFilter(Filter):
    name = "Remove Peaks"
    params = dict(
        prominence_valley_time=15,
        width_time_min=0,
        width_time_max=15,
        distance_time=1,
        prominence_percent=60
    )
    
    def process(self, data, params: dict):
        freq = 1/data["velocity"].index.diff().median().total_seconds()
    
        dataframe_max = max(data["velocity"])
        dataframe_min = min(data["velocity"])

        abs_max = max(dataframe_max, abs(dataframe_min))

        wlen = params["prominence_valley_time"] * freq # prominence_valley_time [s] * freq [samples/sec]

        peaks, props = find_peaks(abs(data["velocity"]),
                                width=[params["width_time_min"]*freq, params["width_time_max"]*freq],
                                distance=params["distance_time"]*freq,
                                prominence=params["prominence_percent"]/100*abs_max,
                                wlen=wlen)
        
        data_out = data.copy()
        for peak in peaks:
            data_out.iloc[peak-1000:peak+1000] = 0

        return data_out