#let appendix-pages(entries: (), font: ("TeX Gyre Termes", "FandolHei"), size: 18pt) = {
  for (index, entry) in entries.enumerate() {
    pagebreak(weak: true)

    let title = entry.at("title", default: none)
    let appendix-title = [附录 #numbering("A", index + 1)]
    if title != none {
      appendix-title += h(1em) + title
    }

    show heading.where(level: 1): set align(center)
    show heading.where(level: 1): set text(font: font, size: size, weight: "bold")

    heading(level: 1, numbering: none, appendix-title)
    entry.body
  }
}
