import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

def load_audio(file_path):
    try:
        sr, data = wavfile.read(file_path)
        if data.dtype != np.float32:
            data = data.astype(np.float32)
        return data, sr
    except Exception as e:
        print(f"Ошибка при загрузке {file_path}: {e}")
        return None, None

def compute_statistics(data):
    mean_value = np.mean(data)
    variance_value = np.var(data)
    return mean_value, variance_value

def plot_waveforms(data1, data2, title1, title2):
    plt.figure(figsize=(12, 5))

    plt.subplot(2, 1, 1)
    plt.plot(data1[:5000], color='blue')
    plt.title(title1)

    plt.subplot(2, 1, 2)
    plt.plot(data2[:5000], color='red')
    plt.title(title2)

    plt.tight_layout()
    plt.show()

def analyze_audio(file1, file2):
    data1, sr1 = load_audio(file1)
    data2, sr2 = load_audio(file2)

    if data1 is None or data2 is None:
        print("Ошибка при загрузке файлов. Проверьте их формат.")
        return

    if sr1 != sr2:
        print("Несовпадение частот дискретизации! Проверьте файлы.")
        return

    mean1, var1 = compute_statistics(data1)
    mean2, var2 = compute_statistics(data2)

    print("Статистический анализ:")
    print(f"Оригинальный файл - Среднее: {mean1:.5f}, Дисперсия: {var1:.5f}")
    print(f"Измененный файл - Среднее: {mean2:.5f}, Дисперсия: {var2:.5f}")

    plot_waveforms(data1, data2, "Оригинальный файл", "Файл после LSB")

    diff = data1 - data2
    print(f"Максимальная разница: {np.max(diff)}")
    print(f"Минимальная разница: {np.min(diff)}")

    plt.figure(figsize=(12, 5))
    plt.plot(diff[:5000], color='black')
    plt.title("Разница между сигналами (первые 5000 отсчетов)")
    plt.show()

if __name__ == "__main__":
    file_original = "audio.wav"
    file_stego = "audioLSB.wav"

    if not os.path.exists(file_original) or not os.path.exists(file_stego):
        print("Один из файлов не найден!")
    else:
        analyze_audio(file_original, file_stego)

