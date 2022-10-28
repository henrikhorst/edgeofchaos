# Defines a function to extract the spikes from the simulation data

import numpy as np

# Set spike threshold (above this value the output value of an oscillator is considered a spike)
th = 1


def get_spikes(arr, th=th, rise=True):
    '''
    Function for extracting spikes from a block of the oscillators output
    voltage values given the spiking threshold.
    Parameters:
        arr: array of voltage values, each column corresponds to one oscillator, a numpy array
        th: threshold value above which the output voltage is considered to be a spike, a scalar
        rise: For True get the time value where voltage goes above the threshold(beginning of the spike) and for False where the voltage
              goes below the threshold (end of spike)
    Returns:
        an array to filter the arr or any other corresponding array for the extracted values
        (think of this as an indexing block which gives you just the values which we want by the operation specified in this function)
  '''
    nst = np.diff(np.sign(arr - th), axis=0)
    # print(NST)
    if rise:
        nst = np.where(nst > 1)
    if not rise:
        nst = np.where(nst < -1)
    # print(NST)
    return nst
