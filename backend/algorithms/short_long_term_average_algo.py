from algorithms.algorithm import Algorithm

from obspy.signal.invsim import cosine_taper
from obspy.signal.filter import highpass
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
import numpy as np

class ShortLongTermAverageAlgorithm(Algorithm):
    name = "ShortLong"
        
    def process(self, data):
        
        #tr = data.traces[0].copy()
        #tr_times = tr.times()
        tr_data = data
        
        # Sampling frequency of our trace
        df = data.stats.sampling_rate
        
        # How long should the short-term and long-term window be, in seconds?
        sta_len = 120
        lta_len = 600
        
        # Run Obspy's STA/LTA to obtain a characteristic function
        # This function basically calculates the ratio of amplitude between the short-term
        # and long-term windows, moving consecutively in time across the data
        cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))
        
        # Play around with the on and off triggers, based on values in the characteristic function
        thr_on = 4
        thr_off = 1.5
        on_off = np.array(trigger_onset(cft, thr_on, thr_off))
        return on_off