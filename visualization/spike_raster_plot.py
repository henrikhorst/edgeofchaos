#spike raster plot

import matplotlib.pyplot as plt
import numpy as np

def plot(neuralData):
    # Set spike colors for each neuron
    colorCodes = ('tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
                  'tab:olive', 'tab:cyan', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',
                  'tab:pink', 'tab:gray',
                  'tab:olive', 'tab:cyan')
    # Draw a spike raster plot
    fig, ax = plt.subplots()
    ax.eventplot(neuralData, color=colorCodes, lineoffsets=1, linewidths=0.5, linelengths=0.6)
    ax.set_yticks(np.arange(20))
    # Provide the title for the spike raster plot
    plt.title('Spike raster plot')
    # Give x axis label for the spike raster plot
    plt.xlabel('time[s]')
    # Give y axis label for the spike raster plot
    plt.ylabel('Oscillator')
    plt.show()
