from matplotlib.animation import FuncAnimation
from matplotlib import rc

# equivalent to rcParams['animation.html'] = 'html5'
rc('animation', html='html5')

#set interval time in seconds (this is how long it will last until the animation renders the next image)
interval_in_s=0.05
#create spike data array for the animation
spike_ani_array=np.zeros((20,int(90/interval_in_s)+1))
spikes=np.zeros((20,int(90/interval_in_s)+1))
spike_ani_array.shape

'''
the concept is to have an array of length n*interval+1=simulation time in LTSpice(currently 90s => 90s/0.05s=1800 + 1)
and then to map each spike to the closest index (e.g. a spike at time 0.051 seconds would be mapped to index 1 corresponding to 0.05s)
Hence we went from a not equidistant time array from our LTSpice data to an equidistant array necessary for animation in python since the interval
time has to be constant for animation. To ensure visibility of the spike also the next two indexes of the array a set to 1 (so that the spike is not
just a 50ms blink). Then the following array index is set to -1 so that the program can know when to stop displaying the spike.
'''
for i in range(number_of_oscillators):
    for j in range(len(all_spike_start_times[i])):
        index = int(np.round(all_spike_start_times[i][j] / 0.05))
        spike_ani_array[i, index] = 1
    for n in range(spike_ani_array.shape[1]):
        if spike_ani_array[i, n] == 1:
            spikes[i, n] = 1
            try:
                spikes[i, n + 1] = 1
            except:
                pass
            try:
                spikes[i, n + 2] = 1
            except:
                pass
            try:
                spikes[i, n + 3] = -1
            except:
                pass

spike_plt_arr = np.ones((4, 5, 3), dtype=int) * 255
fig, axes = plt.subplots()


def spike_animation(i):
    axes.clear()
    axes.tick_params(
        left=False,
        bottom=False,
        labelleft=False,
        labelbottom=False)

    for j in range(20):

        if spikes[j, i] == -1:
            spike_plt_arr[j // 5, j % 5, 1] = 255
            spike_plt_arr[j // 5, j % 5, 0] = 255
            spike_plt_arr[j // 5, j % 5, 2] = 255


        elif spikes[j, i] == 1:
            spike_plt_arr[j // 5, j % 5, 1] = 216
            spike_plt_arr[j // 5, j % 5, 0] = 149
            spike_plt_arr[j // 5, j % 5, 2] = 64
    axes.imshow(spike_plt_arr)


playback_speed = 0.5
spike_animation = FuncAnimation(fig, func=spike_animation, frames=int(spikes.shape[1]),
                                interval=1000 * interval_in_s / playback_speed)