"""
Задание 2. Регулярные выражения.
1. Поиск дат в заголовках (DD.MM.YYYY / YYYY год).
2. Извлечение упоминаний денежных сумм из заголовков.
3. Извлечение личных данных из текста (вариант 7).
"""

import re

import pandas as pd

# ---------------------------------------------------------------------------
# 2.1 — Даты в заголовках
# ---------------------------------------------------------------------------

DATE_DMY = re.compile(r"\d{1,2}\.\d{2}\.\d{4}")
DATE_YEAR = re.compile(r"\d{4}\s*год[а-я]?")


def find_dates_in_titles(df: pd.DataFrame) -> dict:
    results = {"dmy": [], "year": []}
    for title in df["title"]:
        title_clean = title.replace("\xa0", " ")
        for m in DATE_DMY.finditer(title_clean):
            results["dmy"].append((title_clean, m.group()))
        for m in DATE_YEAR.finditer(title_clean):
            results["year"].append((title_clean, m.group()))
    return results


# ---------------------------------------------------------------------------
# 2.2 — Денежные суммы в заголовках
# ---------------------------------------------------------------------------

MONEY_RE = re.compile(
    r"[\$€£]?\s*\d[\d\s,.]+"  # цифры (возможно с символом валюты)
    r"(?:млн|млрд|тыс\.?|миллиона|миллиард[а-я]*)?"  # множитель
    r"\s*(?:руб(?:лей|ля)?\.?|долларов?|долл\.?|евро|копеек)?",
    re.IGNORECASE,
)


def find_money_in_titles(df: pd.DataFrame) -> list[tuple[str, str]]:
    results = []
    currency_words = {
        "руб",
        "рубл",
        "долл",
        "доллар",
        "евро",
        "копеек",
        "млн",
        "млрд",
        "тыс",
        "миллион",
        "миллиард",
    }
    for title in df["title"]:
        title_clean = title.replace("\xa0", " ")
        for m in MONEY_RE.finditer(title_clean):
            matched = m.group().strip()
            # Фильтруем: требуем хотя бы одно «денежное» слово поблизости
            context = title_clean[max(0, m.start() - 15) : m.end() + 20].lower()
            if any(w in context for w in currency_words):
                results.append((title_clean, matched))
    return results


# ---------------------------------------------------------------------------
# 2.3 — Variant 7: извлечение личных данных одним сложным регулярным выражением
# ---------------------------------------------------------------------------

VARIANT7_TEXT = (
    "Личные данные: Фролова Мария, контакт: 8 (812) 444-55-66. "
    "Номер заказа: 334 от 22.09.2023. "
    "Заказ: планшет Apple iPad Air, 74,999.00 руб. "
    "Адрес: г. Сочи, ул. Навагинская, 9. "
    "Электронная почта: m.frolova.personal@gmail.com."
)

VARIANT7_RE = re.compile(
    r"Личные данные:\s+"
    r"(?P<name>[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+)"  # имя пользователя
    r",\s+контакт:\s+"
    r"(?P<phone>[\d\s()\-]+?)"  # номер телефона
    r"\.\s+Номер заказа:\s+"
    r"(?P<order_num>\d+)"  # номер заказа
    r"\s+от\s+"
    r"(?P<order_date>\d{2}\.\d{2}\.\d{4})"  # дата заказа
    r"\..*?"
    r"(?P<amount>\d[\d,]+\.\d{2})\s+руб\."  # сумма заказа
    r".*?"
    r"(?P<email>[\w.\-]+@[\w.\-]+\.\w+)"  # email
    r"\.",
    re.DOTALL,
)


def extract_variant7(text: str = VARIANT7_TEXT):
    m = VARIANT7_RE.search(text)
    if not m:
        print("Совпадение не найдено.")
        return None

    print("=== Извлечённые данные (вариант 7) ===")
    print(f"  Имя пользователя : {m.group('name')}")
    print(f"  Номер телефона   : {m.group('phone').strip()}")
    print(f"  Номер заказа     : {m.group('order_num')}")
    print(f"  Дата заказа      : {m.group('order_date')}")
    print(f"  Сумма заказа     : {m.group('amount')} руб.")
    print(f"  Email            : {m.group('email')}")
    print()
    print("  m.groups() →", m.groups())
    return m


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main():
    df = pd.read_csv("news.csv")

    # --- Даты ---
    print("=" * 60)
    print("2.1 Заголовки с датами")
    print("=" * 60)
    dates = find_dates_in_titles(df)

    if dates["dmy"]:
        print("Формат DD.MM.YYYY:")
        for title, d in dates["dmy"]:
            print(f"  [{d}]  {title}")
    else:
        print("Формат DD.MM.YYYY: совпадений не найдено.")

    if dates["year"]:
        print("\nФормат YYYY год[а]:")
        for title, d in dates["year"]:
            print(f"  [{d}]  {title}")
    else:
        print("Формат YYYY год[а]: совпадений не найдено.")

    all_dates = [d for _, d in dates["dmy"]] + [d for _, d in dates["year"]]
    print(f"\nВсего дат извлечено: {len(all_dates)}")
    if all_dates:
        print("Список:", all_dates)
    print()

    # --- Деньги ---
    print("=" * 60)
    print("2.2 Упоминания денежных сумм в заголовках")
    print("=" * 60)
    money = find_money_in_titles(df)
    if money:
        for title, amount in money:
            print(f"  [{amount.strip()}]  {title}")
    else:
        print("Упоминаний не найдено.")
    print()

    # --- Вариант 7 ---
    print("=" * 60)
    print("2.3 / 2.5  Вариант 7 — извлечение личных данных")
    print("=" * 60)
    print("Исходный текст:")
    print(" ", VARIANT7_TEXT)
    print()
    extract_variant7(VARIANT7_TEXT)


if __name__ == "__main__":
    main()
