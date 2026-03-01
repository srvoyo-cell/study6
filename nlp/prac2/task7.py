import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


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
                "n_features": n_features,
                "nnz": nnz,
                "density": density,
                "mean_features": mean_features,
            }
        )
    return pd.DataFrame(results)


min_df_values = [1, 2, 5, 10, 20, 50]
max_df_values = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

if __name__ == "__main__":
    from task3 import preprocessed_docs

    df_min_df = experiment_vectorizer_params(
        preprocessed_docs,
        "min_df",
        min_df_values,
        max_features=None,
    )
    print(df_min_df.to_string(index=False))

    df_max_df = experiment_vectorizer_params(
        preprocessed_docs,
        "max_df",
        max_df_values,
        min_df=2,
        max_features=None,
    )
    print(df_max_df.to_string(index=False))
