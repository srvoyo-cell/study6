from sklearn.feature_extraction.text import TfidfVectorizer
from task3 import preprocessed_docs, X_base, X_params


tfidf_base = TfidfVectorizer()
X_tfidf_base = tfidf_base.fit_transform(preprocessed_docs)
print(f"Размер TF-IDF матрицы: {X_tfidf_base.shape}")
print(f"Количество ненулевых элементов: {X_tfidf_base.nnz}")

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
print(f"Размер матрицы: {X_tfidf_params.shape}")
print(f"Первые 10 признаков: {tfidf_params.get_feature_names_out()[:10]}")

print("IDF значения для первых 10 признаков:")
for i, term in enumerate(tfidf_params.get_feature_names_out()[:10]):
    print(f" {term}: {tfidf_params.idf_[i]:.4f}")

print("Сравнение плотности матриц")
print(f"CountVectorizer (базовый): {X_base.nnz / (X_base.shape[0] * X_base.shape[1]) * 100:.4f}%")
print(f"CountVectorizer (параметры): {X_params.nnz / (X_params.shape[0] * X_params.shape[1]) * 100:.4f}%")
print(f"TfidfVectorizer: {X_tfidf_params.nnz / (X_tfidf_params.shape[0] * X_tfidf_params.shape[1]) * 100:.4f}%")
