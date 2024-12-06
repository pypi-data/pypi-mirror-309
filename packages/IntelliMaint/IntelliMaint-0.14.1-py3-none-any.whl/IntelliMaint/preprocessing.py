from scipy.signal import savgol_filter, butter, lfilter
from scipy.stats import skew, kurtosis
from scipy.fft import fft, fftfreq
import numpy as np

class DataPreprocessing:
    def __init__(self, filter_order=4, cutoff_frequency=0.1):
        self.filter_order = filter_order
        self.cutoff_frequency = cutoff_frequency

    def preprocess(self, signal, operations=None):
        if operations is None:
            operations = ['filter', 'smooth', 'normalize']

        for operation in operations:
            if operation == 'filter':
                signal = self.butter_lowpass_filter(signal)
            elif operation == 'smooth':
                signal = self.apply_savgol_filter(signal)
            elif operation == 'normalize':
                signal = self.normalize_data(signal)

        return signal

    def butter_lowpass_filter(self, data):
        b, a = butter(self.filter_order, self.cutoff_frequency, btype='low', analog=False)
        return lfilter(b, a, data)

    def apply_savgol_filter(self, data, window_length=51, polyorder=3):
        return savgol_filter(data, window_length, polyorder)

    def normalize_data(self, data):
        mean = np.mean(data)
        std = np.std(data)
        return (data - mean) / std
