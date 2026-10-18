#import "@preview/pointless-size:0.1.2": zh

#let references-page(
  source: "/references.bib",
  title: [参考文献],
  full: true,
  style: "gb-7714-2015-numeric",
  font: ("TeX Gyre Termes", "FandolSong"),
  title-font: ("TeX Gyre Termes", "FandolHei"),
) = {
  pagebreak()

  align(center, text(
    font: title-font,
    size: zh(2),
    weight: "bold",
  )[#title])

  v(2em)

  set text(font: font, size: zh(-4), lang: "zh")
  set par(leading: 1em, first-line-indent: 0em)

  bibliography(source, title: none, full: full, style: style)
}
