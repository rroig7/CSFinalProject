import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile

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
audio_path = "PolyHallClap_10mM.WAV"
frequency_range = (20, 50000)  # Specify the frequency range of interest
plot_specific_frequencies(audio_path, frequency_range)
