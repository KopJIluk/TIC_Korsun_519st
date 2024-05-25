import numpy as np
import matplotlib.pyplot as plt

# Параметри сигналу
n = 500
Fs = 1000
Fmax = 19

# Генерація випадкового сигналу з частотою Fmax
t = np.arange(0, n / Fs, 1 / Fs)
signal = np.sin(2 * np.pi * Fmax * t) + 0.5 * np.random.randn(n)

# Збереження результатів
quantized_signals = []
variances = []
snr_values = []

# Квантування сигналу на різні рівні
for M in [4, 16, 64, 256]:
    delta = (np.max(signal) - np.min(signal)) / (M - 1)
    quantized_signal = delta * np.round(signal / delta)
    quantized_signals.append(quantized_signal)

    # Розрахунок рівнів квантування
    quantize_levels = np.arange(np.min(quantized_signal), np.max(quantized_signal) + delta, delta)

    # Генерація бітів
    quantize_bits = np.arange(0, M)
    quantize_bits = [format(bits, '0' + str(int(np.log2(M))) + 'b') for bits in quantize_bits]

    # Таблиця квантування
    quantize_table = np.c_[quantize_levels[:M], quantize_bits[:M]]

    # Відображення таблиці
    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig(f'figures/quantization_table_M{M}.png', dpi=600)

    # Кодування сигналу
    bits = []
    for signal_value in quantized_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if np.round(np.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bits[index])
                break

    bits = [int(bit) for bit in ''.join(bits)]

    # Відображення бітової послідовності
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(np.arange(len(bits)), bits, linewidth=0.1)
    ax.set_xlabel('Відліки')
    ax.set_ylabel('Бітова послідовність')
    ax.set_title(f'Кодова послідовність для M={M}')
    fig.savefig(f'figures/bit_sequence_M{M}.png', dpi=600)

    # Розрахунок дисперсії та співвідношення сигнал/шум
    quantization_noise = quantized_signal - signal
    variance = np.var(quantization_noise)
    signal_power = np.mean(signal ** 2)
    snr = 10 * np.log10(signal_power / variance)

    variances.append(variance)
    snr_values.append(snr)

# Побудова графіків
fig, ax = plt.subplots(figsize=(14 / 2.54, 10 / 2.54))
for idx, M in enumerate([4, 16, 64, 256]):
    ax.plot(t, quantized_signals[idx], label=f'Квантування на {M} рівнів')
ax.plot(t, signal, 'k--', label='Оригінальний сигнал')
ax.set_xlabel('Час (с)')
ax.set_ylabel('Амплітуда')
ax.set_title('Цифрові сигнали з різними рівнями квантування')
ax.legend()
fig.savefig('figures/quantized_signals.png', dpi=600)

fig, ax = plt.subplots(figsize=(14 / 2.54, 10 / 2.54))
ax.plot([4, 16, 64, 256], variances, 'o-')
ax.set_xlabel('Кількість рівнів квантування')
ax.set_ylabel('Дисперсія')
ax.set_title('Залежність дисперсії від кількості рівнів квантування')
fig.savefig('figures/variance_vs_quantization_levels.png', dpi=600)

fig, ax = plt.subplots(figsize=(14 / 2.54, 10 / 2.54))
ax.plot([4, 16, 64, 256], snr_values, 'o-')
ax.set_xlabel('Кількість рівнів квантування')
ax.set_ylabel('Співвідношення сигнал/шум (дБ)')
ax.set_title('Залежність співвідношення сигнал/шум від кількості рівнів квантування')
fig.savefig('figures/snr_vs_quantization_levels.png', dpi=600)

plt.show()
