# This is the main Python script.
# import relevant libraries

import numpy as np
import pandas as pd

from utils import spike_extraction

# Set the random seed for data generation (just for test cases)

np.random.seed(42)

coupling_resistance = '10k'


def load_data(coupling_resistance):

    # read in data from LTSpice into pandas dataframe
    df = pd.read_csv('./data/fireflys100_' + coupling_resistance + 'OhmCouplingResistance.txt', delimiter="\t")
    print(df.head())
    # extract values from the dataframe
    spike_data = df.iloc[:, 1:].values  # now data in numpy array format
    # print(spike_data.shape)
    spike_data = np.concatenate((np.zeros((1, df.shape[1] - 1)), spike_data),
                                axis=0)  # this is due to the np.diff in the get_spikes function which
    # takes the difference of two values, so to consider also the first value on its own we have to add a zero in front, this is also
    # necessary to not induce a time shift in the filtered time array with the reurn value from get_spike()
    # print(spike_data.shape)
    time = df.iloc[:, 0].values

    return spike_data,time


spike_data, time = load_data(coupling_resistance)

number_of_oscillators = spike_data.shape[1]

# write spike times in form of different lengths numpy arrays into one list with each entry the spikes of one oscillator
all_spike_start_times = []
for i in range(number_of_oscillators):
    all_spike_start_times.append(time[spike_extraction.get_spikes(spike_data[:, i])])


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
