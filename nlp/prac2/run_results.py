import json
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix

from task2 import TextPreprocessor

DATA_PATH = "/Users/michael/Documents/study6/nlp/datasets/lenta-ru-news.csv"
SAMPLE_N = int(os.environ.get("SAMPLE_N", "10000"))
RANDOM_STATE = 42

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Load dataset
usecols = None
for cols in (["text"], ["text", "title"], None):
    try:
        df = pd.read_csv(DATA_PATH, usecols=cols)
        usecols = cols
        break
    except Exception:
        continue

if usecols is None:
    df = pd.read_csv(DATA_PATH)

if "text" not in df.columns:
    raise RuntimeError("Expected column 'text' in dataset.")

if len(df) > SAMPLE_N:
    df_sample = df.sample(n=SAMPLE_N, random_state=RANDOM_STATE)
else:
    df_sample = df.copy()

raw_docs = df_sample["text"].astype(str).tolist()

# Preprocess
preprocessor = TextPreprocessor(use_lemmatization=True)
preprocessed_docs = [preprocessor.preprocess_for_vectorizer(doc) for doc in raw_docs]

# CountVectorizer
vectorizer_base = CountVectorizer()
X_base = vectorizer_base.fit_transform(preprocessed_docs)

vectorizer_params = CountVectorizer(max_df=0.8, min_df=5, max_features=1000)
X_params = vectorizer_params.fit_transform(preprocessed_docs)

vectorizer_ngram = CountVectorizer(ngram_range=(1, 2), max_features=1000)
X_ngram = vectorizer_ngram.fit_transform(preprocessed_docs)

# TfidfVectorizer

# Base
tfidf_base = TfidfVectorizer()
X_tfidf_base = tfidf_base.fit_transform(preprocessed_docs)

# Params
tfidf_params = TfidfVectorizer(
    max_df=0.8,
    min_df=5,
    max_features=1000,
    norm="l2",
    use_idf=True,
    smooth_idf=True,
    sublinear_tf=True,
)
X_tfidf_params = tfidf_params.fit_transform(preprocessed_docs)

# Sparsity analysis

def analyze_sparsity(matrix):
    n_rows, n_cols = matrix.shape
    n_nonzero = matrix.nnz
    n_elements = n_rows * n_cols
    density = n_nonzero / n_elements * 100
    row_counts = np.array((matrix > 0).sum(axis=1)).flatten()
    return {
        "shape": [int(n_rows), int(n_cols)],
        "nnz": int(n_nonzero),
        "density": float(density),
        "mean_features": float(row_counts.mean()),
        "median_features": float(np.median(row_counts)),
        "min_features": int(row_counts.min()),
        "max_features": int(row_counts.max()),
    }

stats = {
    "count_base": analyze_sparsity(X_base),
    "count_params": analyze_sparsity(X_params),
    "tfidf_params": analyze_sparsity(X_tfidf_params),
}

# Histograms
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
matrices = [X_base, X_params, X_tfidf_params]
titles = [
    "CountVectorizer (базовый)",
    "CountVectorizer (с параметрами)",
    "TfidfVectorizer (с параметрами)",
]

for ax, matrix, title in zip(axes, matrices, titles):
    row_counts = np.array((matrix > 0).sum(axis=1)).flatten()
    ax.hist(row_counts, bins=30, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Признаков в документе")
    ax.set_ylabel("Частота")
    ax.set_title(title)
    ax.axvline(row_counts.mean(), color="red", linestyle="--", label=f"Среднее: {row_counts.mean():.1f}")
    ax.legend()

plt.tight_layout()
plt.savefig("sparsity_hist.svg")
plt.close(fig)

# Experiments min_df / max_df

def experiment_vectorizer_params(documents, param_name, param_values, **kwargs):
    results = []
    for value in param_values:
        params = kwargs.copy()
        params[param_name] = value
        vectorizer = TfidfVectorizer(**params)
        X = vectorizer.fit_transform(documents)
        n_features = X.shape[1]
        nnz = X.nnz
        density = nnz / (X.shape[0] * n_features) * 100
        mean_features = np.array((X > 0).sum(axis=1)).mean()
        results.append(
            {
                param_name: value,
                "n_features": int(n_features),
                "nnz": int(nnz),
                "density": float(density),
                "mean_features": float(mean_features),
            }
        )
    return pd.DataFrame(results)

min_df_values = [1, 2, 5, 10, 20, 50]
max_df_values = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

min_df_df = experiment_vectorizer_params(preprocessed_docs, "min_df", min_df_values, max_features=None)
max_df_df = experiment_vectorizer_params(preprocessed_docs, "max_df", max_df_values, min_df=2, max_features=None)

# Plots for experiments
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(min_df_df["min_df"], min_df_df["n_features"], "o-", linewidth=2)
axes[0, 0].set_xlabel("min_df")
axes[0, 0].set_ylabel("Размер словаря")
axes[0, 0].set_title("min_df и размер словаря")
axes[0, 0].grid(True)

axes[0, 1].plot(min_df_df["min_df"], min_df_df["density"], "o-", linewidth=2, color="orange")
axes[0, 1].set_xlabel("min_df")
axes[0, 1].set_ylabel("Плотность (%)")
axes[0, 1].set_title("min_df и плотность")
axes[0, 1].grid(True)

axes[1, 0].plot(max_df_df["max_df"], max_df_df["n_features"], "o-", linewidth=2, color="green")
axes[1, 0].set_xlabel("max_df")
axes[1, 0].set_ylabel("Размер словаря")
axes[1, 0].set_title("max_df и размер словаря")
axes[1, 0].grid(True)

axes[1, 1].plot(max_df_df["max_df"], max_df_df["density"], "o-", linewidth=2, color="red")
axes[1, 1].set_xlabel("max_df")
axes[1, 1].set_ylabel("Плотность (%)")
axes[1, 1].set_title("max_df и плотность")
axes[1, 1].grid(True)

plt.tight_layout()
plt.savefig("params_experiment.svg")
plt.close(fig)

# Save results
results = {
    "sample_n": int(len(preprocessed_docs)),
    "count_base": {
        "shape": list(X_base.shape),
        "nnz": int(X_base.nnz),
        "vocab_size": int(len(vectorizer_base.get_feature_names_out())),
        "density": float(X_base.nnz / (X_base.shape[0] * X_base.shape[1]) * 100),
        "features_preview": vectorizer_base.get_feature_names_out()[:10].tolist(),
    },
    "count_params": {
        "shape": list(X_params.shape),
        "nnz": int(X_params.nnz),
        "vocab_size": int(len(vectorizer_params.get_feature_names_out())),
        "density": float(X_params.nnz / (X_params.shape[0] * X_params.shape[1]) * 100),
        "features_preview": vectorizer_params.get_feature_names_out()[:10].tolist(),
    },
    "count_ngram": {
        "shape": list(X_ngram.shape),
        "nnz": int(X_ngram.nnz),
        "features_preview": vectorizer_ngram.get_feature_names_out()[:10].tolist(),
    },
    "tfidf_base": {
        "shape": list(X_tfidf_base.shape),
        "nnz": int(X_tfidf_base.nnz),
    },
    "tfidf_params": {
        "shape": list(X_tfidf_params.shape),
        "nnz": int(X_tfidf_params.nnz),
        "features_preview": tfidf_params.get_feature_names_out()[:10].tolist(),
        "idf_preview": [float(x) for x in tfidf_params.idf_[:10]],
    },
    "sparsity": stats,
    "min_df_table": min_df_df.to_dict(orient="records"),
    "max_df_table": max_df_df.to_dict(orient="records"),
}

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("OK", len(preprocessed_docs))
