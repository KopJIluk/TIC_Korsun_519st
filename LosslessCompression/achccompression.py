import matplotlib.pyplot as plt

# Функція для обчислення ентропії
def entropy(probabilities):
    return sum(-p * math.log2(p) for p in probabilities if p != 0)

# Функція для обчислення bps
def calculate_bps(compressed_data, sequence_length):
    return len(compressed_data) * 8 / sequence_length

# Дані для тестування (припустимо, що ми вже обчислили ентропію та bps для кожної послідовності)
sequences = ["Послідовність 1", "Послідовність 2", "Послідовність 3"]
entropy_values = [3.2, 2.8, 3.5]  # Припустимі значення ентропії
bps_ac_values = [0.7, 0.9, 1.2]    # Припустимі значення bps для методу AC
bps_ch_values = [0.6, 0.8, 1.1]    # Припустимі значення bps для методу CH

# Створення списку для збереження результатів
results = []

# Розрахунок значень для кожної послідовності
for i in range(len(sequences)):
    entropy_value = entropy_values[i]
    bps_ac = bps_ac_values[i]
    bps_ch = bps_ch_values[i]
    results.append([round(entropy_value, 2), bps_ac, bps_ch])

# Зберігання результатів у файлі
with open("results_AC_CH.txt", "w") as f:
    for i, sequence in enumerate(sequences):
        f.write(f"Послідовність {i + 1}:\n")
        f.write(f"Ентропія: {results[i][0]}\n")
        f.write(f"bps AC: {results[i][1]}\n")
        f.write(f"bps CH: {results[i][2]}\n\n")

# Побудова таблиці
fig, ax = plt.subplots(figsize=(14/1.54, len(sequences)/1.54))
headers = ['Ентропія', 'bps AC', 'bps CH']
row_labels = sequences
ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=row_labels, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)

# Збереження зображення
fig.savefig("Результати стиснення методами AC та CH.png")
plt.show()
