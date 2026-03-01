import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from task2 import TextPreprocessor


DATA_PATH = "/Users/michael/Documents/study6/nlp/datasets/lenta-ru-news.csv"
SAMPLE_N = 100000
RANDOM_STATE = 42

df = pd.read_csv(DATA_PATH, usecols=["text"])
df_sample = df.sample(n=min(SAMPLE_N, len(df)), random_state=RANDOM_STATE)
documents = df_sample["text"].astype(str).tolist()

print(f"Загружено документов: {len(documents)}")
print(f"Пример документа:\n{documents[0][:500]}...")

preprocessor = TextPreprocessor(use_lemmatization=True)
preprocessed_docs = [preprocessor.preprocess_for_vectorizer(doc) for doc in documents]

vectorizer_base = CountVectorizer()
X_base = vectorizer_base.fit_transform(preprocessed_docs)
print(f"Размер матрицы: {X_base.shape}")
print(f"Количество ненулевых элементов: {X_base.nnz}")
print(f"Плотность матрицы: {X_base.nnz / (X_base.shape[0] * X_base.shape[1]) * 100:.4f}%")
print(f"Размер словаря: {len(vectorizer_base.get_feature_names_out())}")
print(f"Первые 10 признаков: {vectorizer_base.get_feature_names_out()[:10]}")

vectorizer_params = CountVectorizer(
    max_df=0.8,
    min_df=5,
    max_features=1000,
    stop_words="english",
)
X_params = vectorizer_params.fit_transform(preprocessed_docs)
print(f"Размер матрицы: {X_params.shape}")
print(f"Количество ненулевых элементов: {X_params.nnz}")
print(f"Плотность матрицы: {X_params.nnz / (X_params.shape[0] * X_params.shape[1]) * 100:.4f}%")
print(f"Размер словаря: {len(vectorizer_params.get_feature_names_out())}")
print(f"Первые 10 признаков: {vectorizer_params.get_feature_names_out()[:10]}")

vectorizer_ngram = CountVectorizer(ngram_range=(1, 2), max_features=1000)
X_ngram = vectorizer_ngram.fit_transform(preprocessed_docs)
print(f"Размер матрицы: {X_ngram.shape}")
print(f"Количество ненулевых элементов: {X_ngram.nnz}")
print(f"Примеры признаков: {vectorizer_ngram.get_feature_names_out()[:20]}")
