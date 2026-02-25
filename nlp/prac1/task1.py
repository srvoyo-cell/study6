"""
Задание 1. Базовое.
Загрузка CSV-файла с новостными заголовками,
очистка текста с помощью функции clean_text_v2.
"""

import re

import pandas as pd


def clean_text_v2(text: str) -> str:
    """
    Очистка текста:
    - приводит к нижнему регистру;
    - удаляет пунктуацию и цифры;
    - удаляет слова короче 3 символов;
    - возвращает очищенную строку.
    """
    # 1. Нижний регистр
    text = text.lower()
    # 2. Убираем неразрывные пробелы
    text = text.replace("\xa0", " ")
    # 3. Удаляем пунктуацию и цифры
    text = re.sub(r"[^а-яёa-z\s]", " ", text)
    # 4. Нормализуем пробелы
    text = re.sub(r"\s+", " ", text).strip()
    # 5. Удаляем слова короче 3 символов
    words = [w for w in text.split() if len(w) >= 3]
    return " ".join(words)


def main():
    df = pd.read_csv("news.csv")

    print("=== Структура датасета ===")
    print(df.shape)
    print(df.dtypes)
    print()

    print("=== Первые 5 заголовков (оригинал) ===")
    for i, title in enumerate(df["title"].head(5), 1):
        print(f"  {i}. {title}")
    print()

    # Применяем функцию очистки к колонке title
    df["cleaned"] = df["title"].apply(clean_text_v2)

    print("=== Первые 5 заголовков (после очистки) ===")
    for i, row in df[["title", "cleaned"]].head(5).iterrows():
        print(f"  Оригинал : {row['title']}")
        print(f"  Очищено  : {row['cleaned']}")
        print()

    # Сохраняем результат
    df.to_csv("news_cleaned.csv", index=False, encoding="utf-8")
    print("Файл news_cleaned.csv сохранён.")
    return df


if __name__ == "__main__":
    main()
