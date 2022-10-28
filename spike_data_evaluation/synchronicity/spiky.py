import numpy as np
import pyspike as spk

import utils.save_and_load_spike_data as sl



class Spiky:
    def __init__(self, coupling_rs='1', folder='Same'):
        self.coupling_rs = coupling_rs
        self.folder = folder

    def load(self, coupling_r):
        path = '../' + sl.PATH + self.FOLDER + '/fireflys100_' + self.coupling_r + 'OhmCouplingResistance' + sl.END
        data = sl.load_spike_data(path)
        return data

    def create_spike_trains(self, data, start_time=0.0, end_time=180.0):
        self.fireflies_spike_trains=[]
        for elem in data:
            spike_train = spk.SpikeTrain(elem,
                                         np.array([start_time, end_time]))  # 0.0 Start time, 180.0 End time from the Simulation
            self.fireflies_spike_trains.append(spike_train)

        return self.fireflies_spike_trains





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass