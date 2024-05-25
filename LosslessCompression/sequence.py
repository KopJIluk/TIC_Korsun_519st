import random
import string
import collections
import math
import matplotlib.pyplot as plt

# Завдання 5: Генерування послідовності з випадковим розподілом ймовірностей
def generate_sequence_5(N_sequence):
    # Отримання перших двох літер прізвища та цифр номеру групи
    surname_letters = "TG"  # Ваші ініціали
    group_digits = "561"  # Номер групи

    # Створення списку символів алфавіту
    alphabet = [char for char in surname_letters] + [digit for digit in group_digits]

    # Генерування випадкової послідовності
    sequence = [random.choice(alphabet) for _ in range(N_sequence)]
    random.shuffle(sequence)
    return sequence

# Завдання 6: Генерування послідовності з нерівномірним розподілом ймовірностей
def generate_sequence_6(N_sequence):
    # Отримання перших двох літер прізвища
    surname_letters = "TG"  # Ваші ініціали

    # Отримання цифр номеру групи
    group_digits = "561"  # Номер групи

    # Сумарна ймовірність появи букв та цифр
    prob_letters = 0.7
    prob_digits = 0.3

    # Кількість букв та цифр у послідовності
    n_letters = int(prob_letters * N_sequence)
    n_digits = int(prob_digits * N_sequence)

    # Створення списку букв та цифр
    letters = [char for char in surname_letters]
    digits = [digit for digit in group_digits]

    # Генерування послідовності
    sequence = []
    for _ in range(n_letters):
        sequence.append(random.choice(letters))
    for _ in range(n_digits):
        sequence.append(random.choice(digits))
    random.shuffle(sequence)
    return sequence

# Завдання 7: Генерування послідовності з англійським алфавітом та цифрами
def generate_sequence_7(N_sequence):
    # Англійський алфавіт та цифри
    elements = string.ascii_lowercase + string.digits

    # Генерування випадкової послідовності
    sequence = [random.choice(elements) for _ in range(N_sequence)]
    return sequence

# Завдання 8: Генерування послідовності з одного символу
def generate_sequence_8(N_sequence):
    # Створення послідовності з одного символу '1'
    sequence = ['1'] * N_sequence
    return sequence

# Збереження послідовностей у файл
def save_sequences_to_file(sequences, file_name):
    with open(file_name, 'w') as file:
        for i, sequence in enumerate(sequences, start=1):
            file.write(f"Тестова послідовність №{i}: {''.join(sequence)}\n")

# Обчислення характеристик послідовності
def compute_sequence_characteristics(sequence, N_sequence):
    # Підрахунок кількості входжень кожного символу
    counts = collections.Counter(sequence)

    # Обчислення ймовірності появи кожного символу
    probability = {symbol: count / N_sequence for symbol, count in counts.items()}

    # Обчислення середньої ймовірності
    mean_probability = sum(probability.values()) / len(probability)

    # Визначення типу розподілу ймовірностей
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
    if equal:
        uniformity = "рівна"
    else:
        uniformity = "нерівна"

    # Обчислення ентропії
    entropy = -sum(p * math.log2(p) for p in probability.values())

    # Обчислення надмірності джерела
    sequence_alphabet_size = len(probability)
    if sequence_alphabet_size > 1:
        source_excess = 1 - entropy / math.log2(sequence_alphabet_size)
    else:
        source_excess = 1

    return probability, entropy, source_excess, uniformity

# Генерація послідовностей
N_sequence = 100
sequences = [generate_sequence_5(N_sequence), generate_sequence_6(N_sequence),
             generate_sequence_7(N_sequence), generate_sequence_8(N_sequence)]

# Збереження послідовностей у файл
save_sequences_to_file(sequences, 'sequence.txt')

# Обчислення та вивід характеристик
results = []
for i, sequence in enumerate(sequences, start=1):
    probability, entropy, source_excess, uniformity = compute_sequence_characteristics(sequence, N_sequence)
    results.append([sequence, round(entropy, 2), round(source_excess, 2), uniformity])

# Побудова таблиці
fig, ax = plt.subplots(figsize=(14, len(sequences)))
ax.axis('off')
headers = ['Послідовність', 'Ентропія', 'Надмірність', 'Тип ймовірності']
table = ax.table(cellText=results, colLabels=headers, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

# Збереження таблиці
fig.savefig('Характеристики сформованих послідовностей.png')
plt.show()
