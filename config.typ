#import "modules/page_settings.typ": page-setup
#import "modules/figure_setup.typ": figure_setup
#import "modules/code_setup.typ": code_setup
#import "modules/cover.typ": cover-page
#import "modules/outline.typ": outline_with_sizes
#import "modules/references.typ": references-page
#import "modules/appendix.typ": appendix-pages
#import "presets/course-report.typ": course-report
#import "presets/cs-thesis.typ": cs-thesis
#import "modules/thesis.typ": thesis-report

#let presets = (
  "course-report": course-report,
  "cs-thesis": cs-thesis,
)

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

#let appendix_style = (
  font: (font_config.latin, font_config.hei),
  size: 18pt,
)

#let thesis_config = (
  margin: (left: 1.25in, right: 1.25in, top: 1.28in, bottom: 1.06in),
  leading: 0.8em,
  heading-sizes: (18pt, 14pt, 12pt),
  cover: (
    logo-top: 151pt,
    heading-top: 221pt,
    title-top: 326pt,
    fields-top: 441pt,
    row-height: 46.656pt,
    date-top: 703pt,
    min-gap: 18pt,
  ),
)

#let report(
  preset: "course-report", cover: (:), outline: (:), references: (:), appendices: auto,
  front-matter: (:), statement: auto, acknowledgments: auto, body,
) = {
  assert(preset in presets, message: "未知配置集：" + preset)
  let defaults = presets.at(preset)
  let cover = defaults.cover + cover
  let outline = defaults.outline + outline
  let references = defaults.references + references
  let appendices = if appendices == auto { defaults.appendices } else { appendices }

  if defaults.at("layout", default: "course-report") == "cs-thesis" {
    return thesis-report(
      cover, outline, references, appendices,
      defaults.front-matter + front-matter,
      if statement == auto { defaults.statement } else { statement },
      if acknowledgments == auto { defaults.acknowledgments } else { acknowledgments },
      font_config, thesis_config, bibliography_config, appendix_style, body,
    )
  }

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
  appendix-pages(entries: appendices, ..appendix_style)
}
