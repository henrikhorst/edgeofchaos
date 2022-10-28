import numpy as np

import data.dataloader
import utils.spike_extraction as spike_extraction


class SpikeData:
    def __init__(self, folder, file_name):
        self.spike_path = '../spike_data/'
        self.spike_path_end = '.npy'
        self.spike_folder = folder
        self.spike_file = file_name.replace('.raw', self.spike_path_end)
        self.spike_folder_path = self.spike_path + self.spike_folder
        self.spike_file_path = self.spike_folder_path + self.spike_file

        self.data_path = '../data/'
        self.data_folder = folder
        self.data_file = file_name
        self.data_folder_path = self.data_path + self.data_folder
        self.data_file_path = self.data_folder_path + self.data_file

    def save_spike_data(self):
        if self.data_file_path[-4:] == '.raw':
            circuit_values = data.dataloader.read_raw(self.data_file_path)
            number_of_oscillators = 0
            for elem in circuit_values.keys():
                if 'gate' in elem:
                    number_of_oscillators += 1

            all_spike_start_times = []
            for i in range(number_of_oscillators):
                # print(i)
                all_spike_start_times.append(
                    circuit_values['time'][
                        spike_extraction.get_spikes(circuit_values[f'V(cathode{i + 1})'], th=spike_extraction.th,
                                                    rise=True)])
            np.save(self.spike_file_path, all_spike_start_times, allow_pickle=True)
            return all_spike_start_times

        elif self.data_file_path[-4:] == '.txt':
            df = data.dataloader.read_data(self.data_file_path)
            voltage_data, time = data.dataloader.extract_data(df)
            number_of_oscillators = voltage_data.shape[1]
            # spike_data = spike_extraction.get_spikes(voltage_data, th=spike_extraction.th, rise=True)
            # write spike times in form of different lengths numpy arrays into one list with each entry the spikes of one
            # oscillator
            all_spike_start_times = []
            for i in range(number_of_oscillators):
                # print(i)
                all_spike_start_times.append(
                    time[spike_extraction.get_spikes(voltage_data[:, i], th=spike_extraction.th, rise=True)])
            np.save(self.spike_file_path, all_spike_start_times, allow_pickle=True)

        else:
            print('Data format or file could not be read')



    def load_spike_data(self):
        spike_start_times = np.load(self.spike_file_path, allow_pickle=True)
        return spike_start_times


if __name__ == '__main__':
    save_path = PATH + FOLDER + 'fireflys100_4900OhmCouplingResistance' + END
    save_spike_data('../data/3fold/fireflys100_4900.txt', save_path)
    spike_start_times = load_spike_data(save_path)
    print(type(spike_start_times), len(spike_start_times))
    for i in range(len(spike_start_times)):
        print(spike_start_times[i].shape)
