#import "@preview/codly:2.0.0" as codly
#import "@preview/codly-languages:0.1.10": *

#let code_setup(body) = {
  show: codly.lang-set_(languages: codly-languages)
  show raw.where(block: true): codly.new
  body
}
