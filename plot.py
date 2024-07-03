import numpy as np
import matplotlib.pyplot as plt

# Sample minute-level data
minute_level_data = [
    {'Breathing Rate (bpm)': [18, 20, 21, 20, 22, 23, 19, 20], 'Sound Amplitude (dB)': [68, 70, 71, 72, 74, 75, 70, 72]},  # Day 1
    {'Breathing Rate (bpm)': [21, 22, 23, 22, 24, 25, 21, 22], 'Sound Amplitude (dB)': [71, 72, 73, 74, 75, 76, 73, 74]},  # Day 2
    {'Breathing Rate (bpm)': [20, 21, 22, 23, 21, 22, 20, 21], 'Sound Amplitude (dB)': [70, 71, 72, 73, 72, 74, 71, 72]},  # Day 3
    {'Breathing Rate (bpm)': [22, 23, 24, 23, 24, 25, 23, 24], 'Sound Amplitude (dB)': [73, 74, 75, 74, 75, 76, 74, 75]},  # Day 4
    {'Breathing Rate (bpm)': [23, 24, 25, 24, 26, 27, 24, 25], 'Sound Amplitude (dB)': [74, 75, 76, 75, 77, 78, 75, 76]},  # Day 5
    {'Breathing Rate (bpm)': [25, 26, 27, 26, 28, 29, 26, 27], 'Sound Amplitude (dB)': [76, 77, 78, 77, 79, 80, 77, 78]},  # Day 6
    {'Breathing Rate (bpm)': [26, 27, 28, 27, 29, 30, 27, 28], 'Sound Amplitude (dB)': [77, 78, 79, 78, 80, 81, 78, 79]},  # Day 7
]

# Define thresholds for peak state
breathing_threshold = 22
sound_threshold = 73

# Function to calculate intensity
def calculate_intensity(br, sa):
    normalized_br = (br - breathing_threshold) / (30 - breathing_threshold)
    normalized_sa = (sa - sound_threshold) / (81 - sound_threshold)
    intensity = normalized_br + normalized_sa
    return intensity

# Initialize lists to store peak state AUCs and their start times
peak_aucs = []
peak_start_times = []

for day_index, day_data in enumerate(minute_level_data):
    breathing_rate = day_data['Breathing Rate (bpm)']
    sound_amplitude = day_data['Sound Amplitude (dB)']
    
    current_peak_intensities = []
    current_start_time = None
    
    for minute_index, (br, sa) in enumerate(zip(breathing_rate, sound_amplitude)):
        time_index = day_index * len(breathing_rate) + minute_index + 1
        if br > breathing_threshold and sa > sound_threshold:
            intensity = calculate_intensity(br, sa)
            if current_start_time is None:
                current_start_time = time_index
            current_peak_intensities.append(intensity)
        else:
            if current_peak_intensities:
                auc = np.trapz(current_peak_intensities)
                peak_aucs.append(auc)
                peak_start_times.append(current_start_time)
                current_peak_intensities = []
                current_start_time = None
    
    # Capture any remaining peak at the end of the day
    if current_peak_intensities:
        auc = np.trapz(current_peak_intensities)
        peak_aucs.append(auc)
        peak_start_times.append(current_start_time)

# Plot the AUCs over time
plt.figure(figsize=(12, 6))
plt.plot(peak_start_times, peak_aucs, marker='o', linestyle='-', color='b')
plt.title('Area Under the Curve (AUC) for Each Peak State')
plt.xlabel('Time (minutes)')
plt.ylabel('AUC')
plt.grid(True)
plt.show()
