"""
Задание 3. Статистика.
1. Общее и уникальное количество слов, средняя и медианная длина заголовков.
2. Топ-20 самых частых слов (Counter).
3. Топ-20 значимых слов (без стоп-слов).
4. Визуализация обоих топов (столбчатые диаграммы, matplotlib).
"""

import re
from collections import Counter
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

matplotlib.rcParams["font.family"] = "DejaVu Sans"

# Скачиваем нужные ресурсы NLTK (если ещё не скачаны)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


# ---------------------------------------------------------------------------
# Функция очистки (повторяется из task1 для автономности модуля)
# ---------------------------------------------------------------------------


def clean_text_v2(text: str) -> str:
    text = text.lower()
    text = text.replace("\xa0", " ")
    text = re.sub(r"[^а-яёa-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    words = [w for w in text.split() if len(w) >= 3]
    return " ".join(words)


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def tokenize_ru(text: str) -> list[str]:
    """Токенизация с помощью NLTK (русский язык)."""
    return word_tokenize(text, language="russian")


def build_all_words(df: pd.DataFrame) -> list[str]:
    all_words: list[str] = []
    for text in df["cleaned"]:
        all_words.extend(tokenize_ru(text))
    return all_words


def doc_length(text: str) -> int:
    return len(tokenize_ru(text))


# ---------------------------------------------------------------------------
# Основная статистика
# ---------------------------------------------------------------------------


def compute_statistics(df: pd.DataFrame) -> dict:
    all_words = build_all_words(df)
    df = df.copy()
    df["doc_len"] = df["cleaned"].apply(doc_length)

    stats = {
        "total_words": len(all_words),
        "unique_words": len(set(all_words)),
        "mean_len": df["doc_len"].mean(),
        "median_len": df["doc_len"].median(),
        "all_words": all_words,
        "doc_len_series": df["doc_len"],
    }
    return stats


# ---------------------------------------------------------------------------
# Топ-20
# ---------------------------------------------------------------------------


def top20_all(all_words: list[str]) -> list[tuple[str, int]]:
    freq = Counter(all_words)
    return freq.most_common(20)


def top20_no_stopwords(all_words: list[str]) -> list[tuple[str, int]]:
    ru_stop = set(stopwords.words("russian"))
    filtered = [w for w in all_words if w not in ru_stop and len(w) > 2]
    freq = Counter(filtered)
    return freq.most_common(20)


# ---------------------------------------------------------------------------
# Визуализация
# ---------------------------------------------------------------------------


def _plot_bar(
    data: list[tuple[str, int]],
    title: str,
    filename: str,
    color: str = "steelblue",
) -> Path:
    words, counts = zip(*data)
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(
        range(len(words)), counts, color=color, edgecolor="white", linewidth=0.6
    )
    ax.set_xticks(range(len(words)))
    ax.set_xticklabels(words, rotation=40, ha="right", fontsize=11)
    ax.set_ylabel("Частота", fontsize=12)
    ax.set_title(title, fontsize=13, pad=12)
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    plt.tight_layout()
    out = Path(filename)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  График сохранён: {out}")
    return out


def plot_top20(top_all: list[tuple[str, int]], top_sig: list[tuple[str, int]]):
    _plot_bar(top_all, "Топ-20 самых частых слов", "top20_all.png", color="steelblue")
    _plot_bar(
        top_sig,
        "Топ-20 значимых слов (без стоп-слов)",
        "top20_significant.png",
        color="tomato",
    )


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main():
    df = pd.read_csv("news.csv")
    df["cleaned"] = df["title"].apply(clean_text_v2)

    stats = compute_statistics(df)

    print("=" * 60)
    print("3.1 Общая статистика по корпусу заголовков")
    print("=" * 60)
    print(f"  Всего слов (токенов)     : {stats['total_words']}")
    print(f"  Уникальных слов          : {stats['unique_words']}")
    print(f"  Средняя длина заголовка  : {stats['mean_len']:.1f} слов")
    print(f"  Медианная длина заголовка: {stats['median_len']:.1f} слов")
    print()

    top_all = top20_all(stats["all_words"])
    top_sig = top20_no_stopwords(stats["all_words"])

    print("=" * 60)
    print("3.2 Топ-20 самых частых слов")
    print("=" * 60)
    for rank, (word, cnt) in enumerate(top_all, 1):
        print(f"  {rank:2}. {word:<20} {cnt}")
    print()

    print("=" * 60)
    print("3.3 Топ-20 значимых слов (без стоп-слов)")
    print("=" * 60)
    for rank, (word, cnt) in enumerate(top_sig, 1):
        print(f"  {rank:2}. {word:<20} {cnt}")
    print()

    print("=" * 60)
    print("3.4 Сохранение графиков")
    print("=" * 60)
    plot_top20(top_all, top_sig)


if __name__ == "__main__":
    main()
