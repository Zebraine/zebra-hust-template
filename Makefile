TYPST ?= typst
FONT_PATH ?= fonts
INPUT ?= main.typ
OUTPUT ?= output.pdf

.PHONY: build watch examples

default: build

build:
	$(TYPST) compile --font-path "$(FONT_PATH)" "$(INPUT)" "$(OUTPUT)"

watch:
	$(TYPST) watch --font-path "$(FONT_PATH)" "$(INPUT)" "$(OUTPUT)"

examples:
	$(TYPST) compile --root . --font-path "$(FONT_PATH)" examples/course-report.typ examples/course-report.pdf
	$(TYPST) compile --root . --font-path "$(FONT_PATH)" examples/cs-thesis.typ examples/cs-thesis.pdf
