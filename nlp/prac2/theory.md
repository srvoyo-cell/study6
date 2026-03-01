# Практическая работа 2. Создание признакового пространства

## Цель работы
освоить методы построения признакового пространства для коллекции
текстовых документов путем реализации конвейера лингвистической предобработки,
векторизации с использованием CountVectorizer и TfidfVectorizer, а также анализа
разреженности матрицы «документ-термин» и эффективности различных форматов её
хранения.

## Порядок выполнения работы
Шаг 1. Импорт библиотек и загрузка данных
Листинг 2.1. Импорт библиотек и загрузка данных
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import time
from collections import Counter
# Библиотеки для предобработки
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pymorphy2
# Библиотеки для векторизации
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# Работа с разреженными матрицами
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix, save_npz, load_npz
import scipy.sparse as sp
# Загрузка необходимых ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
```

Шаг 2. Реализация конвейера предобработки
Листинг 2.2. Реализация конвейера предобработки
```python
class TextPreprocessor:
"""
Класс для предобработки текстовых данных
"""
def __init__(self, language='russian', use_lemmatization=True):
self.language = language
self.use_lemmatization = use_lemmatization
# Инициализация стоп-слов
self.stop_words = set(stopwords.words(language))
# Инициализация стеммера/лемматизатора
if use_lemmatization:
self.lemmatizer = pymorphy2.MorphAnalyzer()
else:
self.stemmer = SnowballStemmer(language)
def clean_text(self, text):
"""Базовая очистка текста"""
if not isinstance(text, str):
return ""
# Приведение к нижнему регистру
text = text.lower()
# Удаление HTML-тегов
text = re.sub(r'<[^>]+>', ' ', text)
# Удаление URL
text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
# Удаление email
text = re.sub(r'\S+@\S+', ' ', text)
# Удаление цифр
text = re.sub(r'\d+', ' ', text)
# Удаление пунктуации (оставляем только буквы и пробелы)
text = re.sub(r'[^\w\s]', ' ', text)
text = re.sub(r'[^а-яёa-z\s]', ' ', text)
# Удаление лишних пробелов
text = re.sub(r'\s+', ' ', text)
text = text.strip()
return text
def tokenize(self, text):
"""Токенизация текста"""
return word_tokenize(text, language=
'russian')
def normalize_token(self, token):
"""Нормализация токена (стемминг или лемматизация)"""
if self.use_lemmatization:
# Лемматизация с помощью pymorphy2
parsed = self.lemmatizer.parse(token)[0]
return parsed.normal_form
else:
# Стемминг
return self.stemmer.stem(token)
def preprocess(self, text):
"""Полный конвейер предобработки"""
# Очистка текста
cleaned = self.clean
_
text(text)
# Токенизация
tokens = self.tokenize(cleaned)
# Удаление стоп-слов и коротких токенов, нормализация
processed_
tokens = []
for token in tokens:
if token not in self.stop_
words and len(token) > 2:
normalized = self.normalize
_
token(token)
processed_
tokens.append(normalized)
return processed_
tokens
def preprocess_
for
_
vectorizer(self, text):
    """Предобработка для передачи в CountVectorizer/TfidfVectorizer"""
    processed_
    tokens = self.preprocess(text)
    return ' '.join(processed_
    tokens)
    # Пример использования
    preprocessor = TextPreprocessor(use_lemmatization=True)
    sample_
    text =
    "Это пример текста! Он содержит различные слова, включая числа 123 и знак
    и пунктуации."
    processed = preprocessor.preprocess(sample_text)
    print(f"Исходный текст: {sample_text}")
    print(f"После предобработки: {processed}")
```
Шаг 3. Построение матрицы с CountVectorizer
Листинг 2.3. Построение матрицы с CountVectorizer
```python
#Загрузка примера данных (можно заменить на свой датасет)
from sklearn.datasets import fetch_20newsgroups
# Загружаем небольшую выборку для демонстрации
categories = ['sci.space', 'rec.sport.baseball']
newsgroups = fetch_20newsgroups(subset='train', categories=categories,
remove=('headers', 'footers', 'quotes'))
documents = newsgroups.data
labels = newsgroups.target
print(f"Загружено документов: {len(documents)}")
print(f"Пример документа:\n{documents[0][:500]}...")
# Применяем предобработку к документам
preprocessed_docs = [preprocessor.preprocess_for_vectorizer(doc) for doc in documents]
# 1. Базовый CountVectorizer
print("\n" + "="*60)
print("Базовый CountVectorizer")
print("="*60)
vectorizer_base = CountVectorizer()
X_base = vectorizer_base.fit_transform(preprocessed_docs)
print(f"Размер матрицы: {X_base.shape}")
print(f"Количество ненулевых элементов: {X_base.nnz}")
print(f"Плотность матрицы: {X_base.nnz / (X_base.shape[0] * X_base.shape[1]) * 100:.4f}
%")
print(f"Размер словаря: {len(vectorizer_base.get_feature_names_out())}")
print(f"Первые 10 признаков: {vectorizer_base.get_feature_names_out()[:10]}")
# 2. CountVectorizer с ограничениями
print("\n" + "="*60)
print("CountVectorizer с параметрами")
print("="*60)
vectorizer_params = CountVectorizer(
max_df=0.8, # игнорировать слова, встречающиеся в >80% документов
min_df=5, # игнорировать слова, встречающиеся менее чем в 5 документах
max_features=1000, # ограничить словарь 1000 наиболее частотных слов
stop_words='english' # использовать стандартные английские стоп-слова
)
X_params = vectorizer_params.fit_transform(preprocessed_docs)
print(f"Размер матрицы: {X_params.shape}")
print(f"Количество ненулевых элементов: {X_params.nnz}")
print(f"Плотность матрицы: {X_params.nnz / (X_params.shape[0] * X_params.shape[1]) * 10
0:.4f}%")
print(f"Размер словаря: {len(vectorizer_params.get_feature_names_out())}")
print(f"Первые 10 признаков: {vectorizer_params.get_feature_names_out()[:10]}")
# 3. CountVectorizer с биграммами
print("\n" + "="*60)
print("CountVectorizer с биграммами")
print("="*60)
vectorizer_ngram = CountVectorizer(
ngram_range=(1, 2), # униграммы и биграммы
max_features=1000
)
X_ngram = vectorizer_ngram.fit_transform(preprocessed_docs)
print(f"Размер матрицы: {X_ngram.shape}")
print(f"Количество ненулевых элементов: {X_ngram.nnz}")
print(f"Примеры признаков: {vectorizer_ngram.get_feature_names_out()[:20]}")
```

Шаг 4. Построение TF-IDF матрицы
Листинг 2.4. Построение TF-IDF матрицы
```python
print("\n" + "="*60)
print("TfidfVectorizer")
print("="*60)
# 1. Базовый TfidfVectorizer
tfidf_base = TfidfVectorizer()
X_tfidf_base = tfidf_base.fit_transform(preprocessed_docs)
print(f"Размер TF-IDF матрицы: {X_tfidf_base.shape}")
print(f"Количество ненулевых элементов: {X_tfidf_base.nnz}")
# 2. TfidfVectorizer с различными параметрами
tfidf_params = TfidfVectorizer(
max_df=0.8,
min_df=5,
max_features=1000,
norm='l2', # L2 нормализация векторов
use_idf=True, # использовать IDF
smooth_idf=True, # сглаженный IDF
sublinear_tf=True # сублинейное масштабирование TF: 1 + log(TF)
)
X_tfidf_params = tfidf_params.fit_transform(preprocessed_docs)
print(f"\nTfidfVectorizer с параметрами:")
print(f"Размер матрицы: {X_tfidf_params.shape}")
print(f"Первые 10 признаков: {tfidf_params.get_feature_names_out()[:10]}")
# Анализ IDF значений
print(f"\nIDF значения для первых 10 признаков:")
for i, term in enumerate(tfidf_params.get_feature_names_out()[:10]):
print(f" {term}: {tfidf_params.idf_[i]:.4f}")
# 3. Сравнение с CountVectorizer
print("\n" + "="*60)
print("Сравнение плотности матриц")
print("="*60)
print(f"CountVectorizer (базовый): плотность {X_base.nnz / (X_base.shape[0] * X_base.sh
ape[1]) * 100:.4f}%")
print(f"CountVectorizer (параметры): плотность {X_params.nnz / (X_params.shape[0] * X_p
arams.shape[1]) * 100:.4f}%")
print(f"TfidfVectorizer: плотность {X_tfidf_params.nnz / (X_tfidf_params.shape[0] * X_t
fidf_params.shape[1]) * 100:.4f}%")
```

Шаг 5. Анализ разреженности матрицы
Листинг 2.5 Анализ разреженности матрицы
```python
def analyze_sparsity(matrix, name="Матрица"):
"""
Анализ разреженности матрицы
"""
n
_
rows, n
_
cols = matrix.shape
n
nonzero = matrix.nnz
_
n
elements = n
rows * n
_
_
_
cols
density = n
nonzero / n
elements * 100
_
_
print(f"\nАнализ разреженности: {name}")
print(f" Размерность: {n
_
rows} x {n
_
cols}")
print(f" Всего элементов: {n
_
elements:,}")
print(f" Ненулевых элементов: {n
_
nonzero:,}")
print(f" Плотность: {density:.6f}%")
print(f" Разреженность: {100 - density:.6f}%")
# Статистика по строкам
row
_
counts = np.array((matrix > 0).sum(axis=1)).flatten()
print(f" Среднее количество признаков в документе: {row
_
counts.mean():.2f}")
print(f" Медианное количество признаков: {np.median(row
_
counts):.2f}")
print(f" Минимум признаков в документе: {row
_
counts.min()}")
print(f" Максимум признаков в документе: {row
_
counts.max()}")
return {
'density': density,
'mean
features': row
_
_
counts.mean(),
'std
features': row
_
_
counts.std()
}
# Анализ разреженности для разных матриц
stats
_
base = analyze_sparsity(X
_
base,
"CountVectorizer (базовый)")
stats
_params = analyze_sparsity(X
_params,
"CountVectorizer (с параметрами)")
stats
_
tfidf = analyze_sparsity(X
tfidf
_
_params,
"TfidfVectorizer")
# Визуализация распределения количества признаков
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
matrices = [X
_
base, X
_params, X
tfidf
_
_params]
titles = ["CountVectorizer\n(базовый)",
"CountVectorizer\n(с параметрами)",
"TfidfVectorizer\n(с параметрами)"]
for ax, matrix, title in zip(axes, matrices, titles):
row
_
counts = np.array((matrix > 0).sum(axis=1)).flatten()
ax.hist(row
_
counts, bins=30, edgecolor=
'black'
, alpha=0.7)
ax.set
_
xlabel('Количество признаков в документе')
ax.set
_ylabel('Частота')
ax.set
_
title(title)
ax.axvline(row
_
counts.mean(), color=
'red'
, linestyle=
'
--
'
, label=f'Среднее: {row
_
co
unts.mean():.1f}')
ax.legend()
plt.tight_layout()
plt.show()
```

Шаг 6. Работа с форматами хранения разреженных матриц
Листинг 2.6 Работа с форматами хранения разреженных матриц
```python
print("\n" + "="*60)
print("Форматы хранения разреженных матриц")
print("="*60)
# Создаем небольшую тестовую матрицу для демонстрации
data = [1, 2, 3, 4, 5]
rows = [0, 1, 2, 0, 1]
cols = [0, 2, 1, 3, 4]
# COO формат (Coordinate format)
coo = coo_matrix((data, (rows, cols)), shape=(3, 5))
print("\nCOO формат:")
print(f" Данные: {coo.data}")
print(f" Строки: {coo.row}")
print(f" Столбцы: {coo.col}")
print(f" Матрица:\n{coo.toarray()}")
# CSR формат (Compressed Sparse Row)
csr = coo.tocsr()
print("\nCSR формат:")
print(f" Данные: {csr.data}")
print(f" Индексы столбцов: {csr.indices}")
print(f" Указатели строк: {csr.indptr}")
# CSC формат (Compressed Sparse Column)
csc = coo.tocsc()
print("\nCSC формат:")
print(f" Данные: {csc.data}")
print(f" Индексы строк: {csc.indices}")
print(f" Указатели столбцов: {csc.indptr}")
# Сравнение размеров в памяти
import sys
def get_size(obj):
return sys.getsizeof(obj)
print("\n" + "="*60)
print("Сравнение размеров в памяти")
print("="*60)
# Плотная матрица
dense_matrix = X_base.toarray()
dense_size = get_size(dense_matrix) + dense_matrix.nbytes
# Разреженные форматы
coo_matrix_sp = coo_matrix(X_base)
csr_matrix_sp = csr_matrix(X_base)
csc_matrix_sp = csc_matrix(X_base)
print(f"Плотная матрица: {dense_size / 1024:.2f} KB")
print(f"COO формат: {get_size(coo_matrix_sp) / 1024:.2f} KB")
print(f"CSR формат: {get_size(csr_matrix_sp) / 1024:.2f} KB")
print(f"CSC формат: {get_size(csc_matrix_sp) / 1024:.2f} KB")
print(f"Экономия памяти (CSR vs плотная): {(1 - get_size(csr_matrix_sp) / dense_size) *
100:.2f}%")
# Сохранение и загрузка разреженных матриц
print("\n" + "="*60)
print("Сохранение и загрузка разреженных матриц")
print("="*60)
# Сохранение в формате .npz
save_npz('sparse_matrix.npz', X_base)
print("Матрица сохранена в файл 'sparse_matrix.npz'")
# Загрузка
X_loaded = load_npz('sparse_matrix.npz')
print(f"Загруженная матрица: размер {X_loaded.shape}, ненулевых {X_loaded.nnz}")
# Проверка идентичности
print(f"Матрицы идентичны: {(X_base != X_loaded).nnz == 0}")
```

Шаг 7. Исследование влияния параметров на разреженность
Листинг 2.6 Исследование влияния параметров на разреженность
```python
def experiment_vectorizer_params(documents, param_name, param_values, **kwargs):
"""
Эксперимент по исследованию влияния параметров на разреженность
"""
results = []
for value in param_values:
# Создаем вектор с текущим параметром
params = kwargs.copy()
params[param_name] = value
vectorizer = TfidfVectorizer(**params)
X = vectorizer.fit_transform(documents)
# Собираем статистику
n_features = X.shape[1]
nnz = X.nnz
density = nnz / (X.shape[0] * n_features) * 100
mean_features = np.array((X > 0).sum(axis=1)).mean()
results.append({
param_name: value,
'n_features': n_features,
'nnz': nnz,
'density': density,
'mean_features': mean_features
})
return pd.DataFrame(results)
# Эксперимент с min_df
print("\n" + "="*60)
print("Эксперимент: влияние min_df")
print("="*60)
min_df_values = [1, 2, 5, 10, 20, 50]
df_min_df = experiment_vectorizer_params(
preprocessed_docs,
'min_df',
min_df_values,
max_features=None
)
print(df_min_df.to_string())
# Эксперимент с max_df
print("\n" + "="*60)
print("Эксперимент: влияние max_df")
print("="*60)
max_df_values = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
df_max_df = experiment_vectorizer_params(
preprocessed_docs,
'max_df',
max_df_values,
min_df=2,
max_features=None
)
print(df_max_df.to_string())
# Визуализация результатов
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# График 1: min_df vs количество признаков
axes[0, 0].plot(df_min_df['min_df'], df_min_df['n_features'], 'o-
', linewidth=2)
axes[0, 0].set_xlabel('min_df')
axes[0, 0].set_ylabel('Количество признаков')
axes[0, 0].set_title('Влияние min_df на размер словаря')
axes[0, 0].grid(True)
# График 2: min_df vs плотность
axes[0, 1].plot(df_min_df['min_df'], df_min_df['density'], 'o-
', linewidth=2, color='or
ange')
axes[0, 1].set_xlabel('min_df')
axes[0, 1].set_ylabel('Плотность (%)')
axes[0, 1].set_title('Влияние min_df на плотность')
axes[0, 1].grid(True)
# График 3: max_df vs количество признаков
axes[1, 0].plot(df_max_df['max_df'], df_max_df['n_features'], 'o-
', linewidth=2, color=
'green')
axes[1, 0].set_xlabel('max_df')
axes[1, 0].set_ylabel('Количество признаков')
axes[1, 0].set_title('Влияние max_df на размер словаря')
axes[1, 0].grid(True)
# График 4: max_df vs плотность
axes[1, 1].plot(df_max_df['max_df'], df_max_df['density'], 'o-
', linewidth=2, color='re
d')
axes[1, 1].set_xlabel('max_df')
axes[1, 1].set_ylabel('Плотность (%)')
axes[1, 1].set_title('Влияние max_df на плотность')
axes[1, 1].grid(True)
plt.tight_layout()
plt.show()
```


# Задание на самостоятельную работу
1. Загрузить корпус текстовых документов новостной ленты с Kaggle: News dataset from
Lenta.Ru. Данные содержат более 800 тыс. новостей с сайта lenta.ru за период с 1999 по
2019 годы. Размер файла lenta-ru-news.csv более 500 Мб в сжатом виде и 2 Гб после
разархивации. Случайным образом выберите не более 100 тыс. новостей для обработки.
2. Реализовать конвейер предобработки (токенизация, удаление стоп-слов,
лемматизация/стемминг).
3. Построить матрицы с помощью CountVectorizer и TfidfVectorizer с различными
параметрами.
4. Провести анализ разреженности полученных матриц.
5. Сравнить эффективность различных форматов хранения (CSR, CSC, COO).
6. Исследовать влияние параметров min_df, max_df, max_features на характеристики
матриц.
7. Выполнить индивидуальное задание вручную.
8. Подготовить отчет с визуализацией результатов.

## Варианты заданий
Варианты индивидуальных заданий
Общие указания:
- для каждого варианта дан корпус из 3–4 коротких документов (предложений);
- выполните все задания письменно, с подробными вычислениями;
- при расчётах используйте натуральный логарифм (ln). Ответы округляйте до двух
знаков после запятой;
- стоп-слова и правила стемминга/лемматизации указаны в каждом варианте;
- форматы разреженных матриц: CSR, CSC, COO.

ВАРИАНТ 6 (русский, тема «погода»)
Корпус:
1. Сегодня идёт дождь.
2. Дождь идёт второй день.
3. Завтра дождя не будет.
Стоп-слова: и, не.
Лемматизация:
• идёт → идти
• дождь → дождь
• второй → второй
• день → день
• завтра → завтра
• будет → быть
Задания:
1. Удалите стоп-слова, выполните лемматизацию.
2. Постройте словарь.
3. Вычислите DF и IDF.
4. Для документа 3 постройте вектор TF (нормированный на длину документа) и вектор
TF‑IDF.
5. Постройте частотную матрицу, вычислите плотность.
6. Представьте матрицу в формате CSC.
