# set frame duration -> in the paper this ranged from 1 to 16ms
frame_duration = [0.003, 0.001, 0.0005, 0.0001]  # 50ms
for f in frame_duration:

    frames = np.linspace(0, 90, int(90 / f) + 1)

    spiking_neurons_per_frame = np.zeros(len(frames))
    for i in range(len(all_spike_start_times)):
        for j in np.digitize(all_spike_start_times[i], frames):
            spiking_neurons_per_frame[j - 1] += 1

    avalanche_sizes = []
    curr_avalanche = False
    for elem in spiking_neurons_per_frame:
        if elem > 0:
            if curr_avalanche == False:
                avalanche_sizes.append(elem)
                curr_avalanche = True
            else:
                avalanche_sizes[-1] += elem


        else:
            curr_avalanche = False

    import powerlaw

    results = powerlaw.Fit(avalanche_sizes, discrete=True)
    print(results.power_law.alpha)
    print(results.power_law.xmin)
    R, p = results.distribution_compare('power_law', 'exponential',
                                        normalized_ratio=True)  # 'truncated_power_law', 'lognormal'
    print(f"R: {R}, p: {p}")
