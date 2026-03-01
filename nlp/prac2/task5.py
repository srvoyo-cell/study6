import numpy as np
import matplotlib.pyplot as plt
from task3 import X_base, X_params
from task4 import X_tfidf_params


def analyze_sparsity(matrix, name="Матрица"):
    n_rows, n_cols = matrix.shape
    n_nonzero = matrix.nnz
    n_elements = n_rows * n_cols
    density = n_nonzero / n_elements * 100

    print(f"\nАнализ разреженности: {name}")
    print(f" Размерность: {n_rows} x {n_cols}")
    print(f" Всего элементов: {n_elements:,}")
    print(f" Ненулевых элементов: {n_nonzero:,}")
    print(f" Плотность: {density:.6f}%")
    print(f" Разреженность: {100 - density:.6f}%")

    row_counts = np.array((matrix > 0).sum(axis=1)).flatten()
    print(f" Среднее количество признаков в документе: {row_counts.mean():.2f}")
    print(f" Медианное количество признаков: {np.median(row_counts):.2f}")
    print(f" Минимум признаков в документе: {row_counts.min()}")
    print(f" Максимум признаков в документе: {row_counts.max()}")

    return {
        "density": density,
        "mean_features": row_counts.mean(),
        "std_features": row_counts.std(),
    }


stats_base = analyze_sparsity(X_base, "CountVectorizer (базовый)")
stats_params = analyze_sparsity(X_params, "CountVectorizer (с параметрами)")
stats_tfidf = analyze_sparsity(X_tfidf_params, "TfidfVectorizer")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
matrices = [X_base, X_params, X_tfidf_params]
titles = [
    "CountVectorizer\n(базовый)",
    "CountVectorizer\n(с параметрами)",
    "TfidfVectorizer\n(с параметрами)",
]

for ax, matrix, title in zip(axes, matrices, titles):
    row_counts = np.array((matrix > 0).sum(axis=1)).flatten()
    ax.hist(row_counts, bins=30, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Количество признаков в документе")
    ax.set_ylabel("Частота")
    ax.set_title(title)
    ax.axvline(row_counts.mean(), color="red", linestyle="--", label=f"Среднее: {row_counts.mean():.1f}")
    ax.legend()

plt.tight_layout()
plt.show()
