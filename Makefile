TYPST ?= typst
FONT_PATH ?= fonts
INPUT ?= main.typ
OUTPUT ?= output.pdf

.PHONY: build watch

build:
	$(TYPST) compile --font-path "$(FONT_PATH)" "$(INPUT)" "$(OUTPUT)"

watch:
	$(TYPST) watch --font-path "$(FONT_PATH)" "$(INPUT)" "$(OUTPUT)"
