// ── listings.typ ─────────────────────────────────────────────────────────────
// Модуль оформления листингов и подписей к таблицам.
//
// Использование в основном документе:
//   #import "listings.typ": setup-listings, listing, tbl-caption
//   #show: setup-listings
// ─────────────────────────────────────────────────────────────────────────────

/// Применяет правила оформления блочного кода ко всему документу.
/// Использовать как: #show: setup-listings
#let setup-listings(body) = {
  show raw.where(block: true): it => {
    set text(font: "JetBrains Mono", size: 10pt)
    set par(first-line-indent: 0pt, leading: 0.5em, spacing: 0.6em)
    let lines = it.text.split("\n")
    block(
      fill: luma(245),
      inset: (x: 10pt, y: 8pt),
      radius: 3pt,
      width: 100%,
      stroke: (left: 2pt + luma(180)),
      grid(
        columns: (auto, 1fr),
        column-gutter: 8pt,
        row-gutter: 2pt,
        ..lines.enumerate(start: 1).map(((i, line)) => (
          align(right, text(fill: luma(160), size: 9.5pt, str(i))),
          raw(line, lang: it.lang),
        )).flatten()
      )
    )
  }
  body
}

/// Оформляет подпись листинга над кодом.
/// Пример: #listing("1.1", "Загрузка датасета")[ ```python ... ``` ]
#let listing(num, caption, body) = {
  set par(first-line-indent: 0pt)
  v(0.3em)
  align(left)[#text(weight: "bold")[Листинг #num] — #caption]
  v(0.15em)
  body
  v(0.3em)
}

/// Оформляет подпись таблицы над ней, выровненную по левому краю таблицы.
/// Пример: #tbl-caption("1.1", "Результаты обработки")
#let tbl-caption(num, caption) = {
  set par(first-line-indent: 0pt)
  v(0.3em)
  align(left)[#text(weight: "bold")[Таблица #num] — #caption]
  v(0.2em)
}
