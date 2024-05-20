import os
import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt


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
plt.xlabel('Частота,FS (Гц)')
plt.ylabel('Модуль спектру')
plt.grid(True)
plt.savefig(os.path.join(save_dir, 'signal_spectrum.png'))
plt.show()
