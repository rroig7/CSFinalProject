"""import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt


def plot_specific_frequencies(audio_path, frequency_range):
    # Load the audio file
    audio = AudioSegment.from_file(audio_path)

    # Convert AudioSegment to NumPy array
    samples = np.array(audio.get_array_of_samples())

    # Perform Fourier Transform
    frequencies, amplitudes = calculate_frequency_spectrum(samples, audio.frame_rate)

    # Filter frequencies within the specified range
    mask = np.logical_and(frequencies >= frequency_range[0], frequencies <= frequency_range[1])
    filtered_frequencies = frequencies[mask]
    filtered_amplitudes = amplitudes[mask]

    # Plot the specific frequencies
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_frequencies, filtered_amplitudes)
    plt.title(f"Frequency Spectrum ({frequency_range[0]} Hz to {frequency_range[1]} Hz)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.show()


def calculate_frequency_spectrum(samples, frame_rate):
    # Perform Fourier Transform
    fft_result = np.fft.fft(samples)

    # Calculate the frequencies corresponding to the FFT result
    frequencies = np.fft.fftfreq(len(fft_result), 1 / frame_rate)

    # Take the absolute value to get the amplitude spectrum
    amplitudes = np.abs(fft_result)

    # Keep only the positive frequencies
    positive_frequencies = frequencies[:len(frequencies) // 2]
    positive_amplitudes = amplitudes[:len(amplitudes) // 2]

    return positive_frequencies, positive_amplitudes


# Example usage
audio_path = "C:/Users/Mynor/PycharmProjects/CSFinalProject/PinkPanther30.wav"
frequency_range = (3000,12000)  # Specify the frequency range of interest
plot_specific_frequencies(audio_path, frequency_range)"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment


def mp3_to_wav(input_mp3_path, output_wav_path):
    # Load the MP3 file
    audio = AudioSegment.from_file(input_mp3_path, format="mp3")
    audio = audio.set_channels(1)
    audio.export(output_wav_path, format="wav")


input_mp3_path = 'mgscodec.mp3'
output_wav_path = "output.wav"

mp3_to_wav(input_mp3_path, output_wav_path)

sample_rate, data = wavfile.read(output_wav_path)

spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024)
print("Shape of spectrum:", spectrum.shape)
print("Shape of freqs:", freqs.shape)


def find_target_frequency(freqs):
    for x in freqs:
        if x > 1001:
            break
    return x


def frequency_check():
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    index_of_frequency = np.where(freqs == target_frequency)[0][0]

    data_for_frequency = spectrum[index_of_frequency]

    data_in_db_fun = 10 * np.log10(data_for_frequency + 10)
    return data_in_db_fun


data_in_db = frequency_check()

plt.figure(2)

plt.plot(t, data_in_db, linewidth=1, alpha=.7, color='#004bc6')

plt.xlabel('Time (s)')

plt.ylabel('Power (db)')

index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

sliced_array = data_in_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5


def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'go')

value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'go')
# Assuming `spectrum` contains the spectrogram data

# Define frequency band ranges
low_freq_range = (0, 500)
mid_freq_range = (500, 2000)
high_freq_range = (2000, 8000)

# Calculate the sum of power across frequency bands for each time point
low_freq_power = np.sum(spectrum[(freqs >= low_freq_range[0]) & (freqs <= low_freq_range[1])], axis=0)
mid_freq_power = np.sum(spectrum[(freqs >= mid_freq_range[0]) & (freqs <= mid_freq_range[1])], axis=0)
high_freq_power = np.sum(spectrum[(freqs >= high_freq_range[0]) & (freqs <= high_freq_range[1])], axis=0)

# Find the index and value of the maximum power for each frequency band
index_of_max_low = np.argmax(low_freq_power)
index_of_max_mid = np.argmax(mid_freq_power)
index_of_max_high = np.argmax(high_freq_power)

value_of_max_low = low_freq_power[index_of_max_low]
value_of_max_mid = mid_freq_power[index_of_max_mid]
value_of_max_high = high_freq_power[index_of_max_high]

# Find the value 5 dB below the maximum power for each frequency band
value_of_max_low_less_5 = value_of_max_low - 5
value_of_max_mid_less_5 = value_of_max_mid - 5
value_of_max_high_less_5 = value_of_max_high - 5

index_of_max_low_less_5 = np.where(low_freq_power >= value_of_max_low_less_5)[0][0]
index_of_max_mid_less_5 = np.where(mid_freq_power >= value_of_max_mid_less_5)[0][0]
index_of_max_high_less_5 = np.where(high_freq_power >= value_of_max_high_less_5)[0][0]

# Find the value 25 dB below the maximum power for each frequency band
value_of_max_low_less_25 = value_of_max_low - 25
value_of_max_mid_less_25 = value_of_max_mid - 25
value_of_max_high_less_25 = value_of_max_high - 25

index_of_max_low_less_25 = np.where(low_freq_power >= value_of_max_low_less_25)[0][0]
index_of_max_mid_less_25 = np.where(mid_freq_power >= value_of_max_mid_less_25)[0][0]
index_of_max_high_less_25 = np.where(high_freq_power >= value_of_max_high_less_25)[0][0]

plt.plot(t[index_of_max_low], data_in_db[index_of_max_low], 'go')
plt.plot(t[index_of_max_mid], data_in_db[index_of_max_mid], 'go')
plt.plot(t[index_of_max_high], data_in_db[index_of_max_high], 'go')


plt.plot(t[index_of_max_low_less_5], data_in_db[index_of_max_low_less_5], 'yo')
plt.plot(t[index_of_max_mid_less_5], data_in_db[index_of_max_mid_less_5], 'yo')
plt.plot(t[index_of_max_high_less_5], data_in_db[index_of_max_mid_less_5], 'yo')


plt.plot(t[index_of_max_low_less_25], data_in_db[index_of_max_low_less_25], 'ro')
plt.plot(t[index_of_max_mid_less_25], data_in_db[index_of_max_mid_less_25], 'ro')
plt.plot(t[index_of_max_high_less_25], data_in_db[index_of_max_high_less_25], 'ro')


# Calculate RT20 and RT60 for each frequency band
rt20_low = (t[index_of_max_low_less_5] - t[index_of_max_low_less_25])
rt60_low = 3 * rt20_low

rt20_mid = (t[index_of_max_mid_less_5] - t[index_of_max_mid_less_25])
rt60_mid = 3 * rt20_mid

rt20_high = (t[index_of_max_high_less_5] - t[index_of_max_high_less_25])
rt60_high = 3 * rt20_high

print(f"The RT60 reverb time for low frequencies is {np.round(abs(rt60_low), 2)} seconds")
print(f"The RT60 reverb time for mid frequencies is {np.round(abs(rt60_mid), 2)} seconds")
print(f"The RT60 reverb time for high frequencies is {np.round(abs(rt60_high), 2)} seconds")

plt.grid()

plt.show()

