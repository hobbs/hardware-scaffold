PYTHON ?= python3.12
VENV_PYTHON := .venv/bin/python
PIO ?= pio
KICAD_SCH ?= electrical/kicad/project.kicad_sch
KICAD_PDF ?= electrical/reports/schematic.pdf
SCAFFOLD_ROOT ?= ../..

.PHONY: help check check-strict platformio-toolcheck platformio-build cad-setup cad cad-test cad-view wiring-setup wiring wiring-check kicad-toolcheck kicad-erc kicad-pdf clean-generated

help:
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check: ## Validate materialized project artifacts
	@python3 $(SCAFFOLD_ROOT)/scripts/check_project.py --root .

check-strict: ## Reject materialized placeholders and incomplete selected parts
	@python3 $(SCAFFOLD_ROOT)/scripts/check_project.py --root . --strict

platformio-toolcheck: ## Confirm pinned PlatformIO project configuration is readable
	@test -f firmware/platformio.ini || { echo "firmware/platformio.ini is required"; exit 1; }
	@command -v $(PIO) >/dev/null || { echo "PlatformIO Core is unavailable. Install it with the official isolated installer: https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html"; exit 1; }
	@$(PIO) --version
	@$(PIO) project config --project-dir firmware >/dev/null

platformio-build: platformio-toolcheck ## Build the pinned PlatformIO firmware target
	@$(PIO) run --project-dir firmware

cad-setup: ## Create .venv and install CadQuery, tests, and interactive viewer support
	@command -v $(PYTHON) >/dev/null || { echo "$(PYTHON) is required; install Python 3.12 or set PYTHON=/path/to/python3.12"; exit 1; }
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -e '.[mechanical,dev,viewer]'

cad: ## Generate mechanical STEP/STL exports and SVG previews
	@test -x $(VENV_PYTHON) || { echo "Run 'make cad-setup' first"; exit 1; }
	$(VENV_PYTHON) mechanical/build.py

cad-test: ## Run mechanical geometry tests
	@test -x $(VENV_PYTHON) || { echo "Run 'make cad-setup' first"; exit 1; }
	$(VENV_PYTHON) -m pytest

cad-view: ## Send the assembly to the VS Code OCP CAD Viewer
	@test -x $(VENV_PYTHON) || { echo "Run 'make cad-setup' first"; exit 1; }
	$(VENV_PYTHON) mechanical/view.py

wiring-setup: ## Install pinned WireViz into .venv (Graphviz is also required to render)
	@command -v $(PYTHON) >/dev/null || { echo "$(PYTHON) is required; install Python 3.12 or set PYTHON=/path/to/python3.12"; exit 1; }
	@test -x $(VENV_PYTHON) || $(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -e '.[wiring]'

wiring-check: ## Parse WireViz source and generate its tabular BOM without Graphviz
	@test -x .venv/bin/wireviz || { echo "Run 'make wiring-setup' first"; exit 1; }
	mkdir -p electrical/wiring/out
	.venv/bin/wireviz -f t -o electrical/wiring/out -O harness electrical/wiring/harness.yml

wiring: ## Render WireViz HTML/PNG/SVG/TSV outputs
	@test -x .venv/bin/wireviz || { echo "Run 'make wiring-setup' first"; exit 1; }
	@command -v dot >/dev/null || { echo "Graphviz 'dot' is required (for example: brew install graphviz)"; exit 1; }
	mkdir -p electrical/wiring/out
	.venv/bin/wireviz -o electrical/wiring/out -O harness electrical/wiring/harness.yml

kicad-toolcheck: ## Confirm native KiCad schematic and ERC tooling is available
	@$(MAKE) -s -C $(SCAFFOLD_ROOT) kicad-toolcheck

kicad-erc: kicad-toolcheck ## Run KiCad ERC against KICAD_SCH
	@test -f $(KICAD_SCH) || { echo "No schematic at $(KICAD_SCH); create it or override KICAD_SCH"; exit 1; }
	mkdir -p electrical/reports
	kicad-cli sch erc -o electrical/reports/erc.rpt $(KICAD_SCH)

kicad-pdf: kicad-toolcheck ## Export the schematic as a local review PDF
	@test -f $(KICAD_SCH) || { echo "No schematic at $(KICAD_SCH); create it or override KICAD_SCH"; exit 1; }
	mkdir -p $(dir $(KICAD_PDF))
	kicad-cli sch export pdf --output $(KICAD_PDF) $(KICAD_SCH)

clean-generated: ## Remove ignored generated outputs but preserve source
	@find mechanical/exports -type f -delete
	@find mechanical/previews -type f -delete
	@find electrical/wiring/out -type f -delete
	@find electrical/reports -type f -delete
