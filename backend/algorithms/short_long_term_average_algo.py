from algorithms.algorithm import Algorithm

from obspy.signal.trigger import classic_sta_lta, trigger_onset
import numpy as np

class ShortLongTermAverageAlgorithm(Algorithm):
    name = "ShortLong"
        
    def process(self, data):
        # Convert the DataFrame to a NumPy array
        tr_data = data["velocity"].to_numpy()
        # Sampling frequency of our trace
        df = 1/data["velocity"].index.diff().median().total_seconds()
        if df is None:
            raise ValueError("Sampling rate must be provided in the DataFrame attributes")
        
        # How long should the short-term and long-term window be, in seconds?
        sta_len = 120
        lta_len = 600
        
        # Run Obspy's STA/LTA to obtain a characteristic function
        # This function basically calculates the ratio of amplitude between the short-term
        # and long-term windows, moving consecutively in time across the data
        nsta = int(sta_len * df)
        nlta = int(lta_len * df)
        
        cft = classic_sta_lta(tr_data, nsta, nlta)
        print("cft : ", cft)
        
        # Play around with the on and off triggers, based on values in the characteristic function
        thr_on = 4
        thr_off = 1.5
        on_off = np.array(trigger_onset(cft, thr_on, thr_off))
        return on_off