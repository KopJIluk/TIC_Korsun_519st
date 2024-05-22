import os
import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt

# Вихідні параметри
n = 500  # Довжина сигналу у відліках
Fs = 1000  # Частота дискретизації (Гц)
F_max = 19  # Максимальна частота сигналу (Гц)

# Генерація сигналу
signal_values = np.random.normal(0, F_max, n)

# Визначення відліків часу
time_values = np.arange(n) / Fs

# Розрахунок параметрів фільтру
w = F_max / (Fs / 2)
b, a = signal.butter(3, w, 'low')

# Фільтрація сигналу
filtered_signal = signal.filtfilt(b, a, signal_values)

# Розрахунок спектру сигналу
spectrum = fft.fft(filtered_signal)
spectrum_abs = np.abs(fft.fftshift(spectrum))
freqs = fft.fftfreq(n, 1/Fs)
freqs_shifted = fft.fftshift(freqs)

# Створення директорії для збереження файлів, якщо вона ще не існує
save_dir = 'figures'
os.makedirs(save_dir, exist_ok=True)

# Відображення результатів
plt.figure(figsize=(8.27, 5.83))
plt.plot(time_values, filtered_signal)
plt.title('Згенерований сигнал')
plt.xlabel('Час (с)')
plt.ylabel('Значення сигналу')
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'generated_signal.png'))
plt.show()

plt.figure(figsize=(8.27, 5.83))
plt.plot(freqs_shifted, spectrum_abs)
plt.title('Спектр сигналу')
plt.xlabel('Частота (Гц)')
plt.ylabel('Модуль спектру')
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'signal_spectrum.png'))
plt.show()

# Дискретизація сигналу з різними кроками
steps = [2, 4, 8, 16]
discrete_signals = []
discrete_spectrums = []
restored_signals = []
variances = []
snr_values = []

for Dt in steps:
    discrete_signal = np.zeros(n)
    for i in range(0, round(n/Dt)):
        discrete_signal[i * Dt] = filtered_signal[i * Dt]
    discrete_signals.append(discrete_signal)

    # Розрахунок спектру дискретизованого сигналу
    spectrum = fft.fft(discrete_signal)
    spectrum_abs = np.abs(fft.fftshift(spectrum))
    discrete_spectrums.append(spectrum_abs)

    # Відновлення сигналу
    w = F_max / (Fs / 2)
    sos = signal.butter(3, w, 'low', output='sos')
    restored_signal = signal.sosfiltfilt(sos, discrete_signal)
    restored_signals.append(restored_signal)

    # Розрахунок дисперсії та співвідношення сигнал-шум
    E1 = restored_signal - filtered_signal
    var_original = np.var(filtered_signal)
    var_difference = np.var(E1)
    snr = var_original / var_difference
    variances.append(var_difference)
    snr_values.append(snr)

# Відображення дискретизованих сигналів
fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
fig.suptitle('Дискретизовані сигнали', fontsize=14)

s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(time_values, discrete_signals[s], linewidth=1)
        s += 1

fig.supxlabel('Час (с)', fontsize=14)
fig.supylabel('Значення сигналу', fontsize=14)
plt.savefig(os.path.join(save_dir, 'discrete_signals.png'))
plt.show()

# Відображення спектрів дискретизованих сигналів
fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
fig.suptitle('Спектри дискретизованих сигналів', fontsize=14)

s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(freqs_shifted, discrete_spectrums[s], linewidth=1)
        s += 1

fig.supxlabel('Частота (Гц)', fontsize=14)
fig.supylabel('Модуль спектру', fontsize=14)
plt.savefig(os.path.join(save_dir, 'discrete_spectrums.png'))
plt.show()

# Відображення відновлених сигналів
fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))
fig.suptitle('Відновлені сигнали', fontsize=14)

s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(time_values, restored_signals[s], linewidth=1)
        s += 1

fig.supxlabel('Час (с)', fontsize=14)
fig.supylabel('Значення сигналу', fontsize=14)
plt.savefig(os.path.join(save_dir, 'restored_signals.png'))
plt.show()

# Відображення залежності дисперсії різниці від кроку дискретизації
plt.figure(figsize=(8.27, 5.83))
plt.plot(steps, variances, marker='o')
plt.title('Залежність дисперсії різниці від кроку дискретизації')
plt.xlabel('Крок дискретизації')
plt.ylabel('Дисперсія різниці')
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'variance_vs_step.png'))
plt.show()

# Відображення співвідношення сигнал-шум від кроку дискретизації
plt.figure(figsize=(8.27, 5.83))
plt.plot(steps, snr_values, marker='o')
plt.title('Залежність співвідношення сигнал-шум від кроку дискретизації')
plt.xlabel('Крок дискретизації')
plt.ylabel('Співвідношення сигнал-шум')
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'snr_vs_step.png'))
plt.show()
