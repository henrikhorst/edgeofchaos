# read in data from LTSpice into pandas dataframe
import pandas as pd
import numpy as np
import ltspice_automation.ltspy3 as ltspy3  # Third party Python module


def read_data(path):
    # path example: './data/180s/fireflys100_1megOhmCouplingResistance.txt'
    df = pd.read_csv(path, delimiter="\t")
    return df


def extract_data(df):
    # extract values from the dataframe
    spike_data = df.iloc[:, 1:].values  # now data in numpy array format
    # print(spike_data.shape)
    spike_data = np.concatenate((np.zeros((1, df.shape[1] - 1)), spike_data),
                                axis=0)
    # this is due to the np.diff in the get_spikes function which
    # takes the difference of two values, so to consider also the first value on its own we have to add a zero in
    # front, this is also necessary to not induce a time shift in the filtered time array with the return value from
    # get_spike()
    # print(spike_data.shape)
    time = df.iloc[:, 0].values

    return spike_data, time


def read_raw(raw_file_name):
    """
    This function provides functionality to read LTSpice .raw data into numpy arrays
    """
    sd = ltspy3.SimData(raw_file_name)  # to create a Python object called sd
    name = sd.variables  # variable names from .raw data. It is an attribute (data)
    names = [elem.decode('ascii') for elem in name]
    circuit_values = dict(zip(names, sd.values))  # creates a dictionary with name of each variable as key and data as corresponding values
    return circuit_values


if __name__ == '__main__':
    pass
