#import "modules/page_settings.typ": page-setup
#import "modules/figure_setup.typ": figure_setup
#import "modules/code_setup.typ": code_setup
#import "modules/cover.typ": cover-page
#import "modules/outline.typ": outline_with_sizes
#import "modules/references.typ": references-page

#let font_config = (
  latin: "TeX Gyre Termes",
  song: "FandolSong",
  hei: "FandolHei",
  kai: "FandolKai",
  cover: "FandolSong",
)

#let page_config = (
  paper: "a4",
  margin: (top: 9.5em),
  header-font: font_config.kai,
  footer-font: font_config.cover,
)

#let bibliography_config = (
  style: "gb-7714-2015-numeric",
  font: (font_config.latin, font_config.song),
  title-font: (font_config.latin, font_config.hei),
)

#let report(cover: (:), outline: (depth: 3, font_sizes: (12pt, 12pt, 12pt)), references: (:), body) = {
  show: page-setup.with(..page_config)
  show: figure_setup.with(font: (font_config.latin, font_config.hei))
  show: code_setup

  set text(font: (font_config.latin, font_config.song), size: 12pt, lang: "zh")
  show heading: set text(font: (font_config.latin, font_config.hei))

  cover-page(title-font: font_config.cover, font: font_config.cover, ..cover)
  outline_with_sizes(
    font: (font_config.latin, font_config.song),
    title-font: (font_config.latin, font_config.hei),
    ..outline,
  )
  body
  references-page(..bibliography_config, ..references)
}
