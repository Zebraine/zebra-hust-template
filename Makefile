TYPST ?= typst
FONT_PATH ?= fonts
INPUT ?= main.typ
OUTPUT ?= output.pdf

.PHONY: build watch examples package submit-pr check-release

default: build

build:
	$(TYPST) compile --font-path "$(FONT_PATH)" "$(INPUT)" "$(OUTPUT)"

watch:
	$(TYPST) watch --font-path "$(FONT_PATH)" "$(INPUT)" "$(OUTPUT)"

examples:
	$(TYPST) compile --root . --font-path "$(FONT_PATH)" examples/course-report.typ examples/course-report.pdf
	$(TYPST) compile --root . --font-path "$(FONT_PATH)" examples/cs-thesis.typ examples/cs-thesis.pdf

package:
	python3 scripts/prepare-release.py

check-release:
	python3 scripts/submit-pr.py --dry-run

submit-pr:
	python3 scripts/submit-pr.py
