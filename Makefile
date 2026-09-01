PYTHON ?= python3
PIO ?= pio
PROJECT ?=
NAME ?=
SLUG ?=
GOAL ?=

.PHONY: help check init check-project check-strict kicad-toolcheck platformio-toolcheck platformio-build

help: ## Show workspace commands
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check: ## Validate the workspace and test project initialization
	@$(PYTHON) scripts/check_scaffold.py
	@$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

init: ## Initialize projects/SLUG from NAME and GOAL
	@test -n "$(SLUG)" || { echo "SLUG is required"; exit 1; }
	@test -n "$(NAME)" || { echo "NAME is required"; exit 1; }
	@test -n "$(GOAL)" || { echo "GOAL is required"; exit 1; }
	@$(PYTHON) scripts/init_project.py "$(SLUG)" --name "$(NAME)" --goal "$(GOAL)"

check-project: ## Validate a progressive project at PROJECT
	@test -n "$(PROJECT)" || { echo "PROJECT is required"; exit 1; }
	@$(PYTHON) scripts/check_project.py --root "$(PROJECT)"

check-strict: ## Reject placeholders and incomplete selected parts in PROJECT
	@test -n "$(PROJECT)" || { echo "PROJECT is required"; exit 1; }
	@$(PYTHON) scripts/check_project.py --root "$(PROJECT)" --strict

kicad-toolcheck: ## Confirm native KiCad schematic and ERC tooling is available
	@command -v kicad-cli >/dev/null || { echo "kicad-cli is unavailable. Install KiCad before creating or validating .kicad_sch source; until then, keep work in the interface contract, net registry, and signal-name wiring plan."; exit 1; }
	@kicad-cli version

platformio-toolcheck: ## Confirm pinned PlatformIO project configuration is readable
	@test -n "$(PROJECT)" || { echo "PROJECT is required"; exit 1; }
	@test -f "$(PROJECT)/firmware/platformio.ini" || { echo "$(PROJECT)/firmware/platformio.ini is required"; exit 1; }
	@command -v $(PIO) >/dev/null || { echo "PlatformIO Core is unavailable. Install it with the official isolated installer: https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html"; exit 1; }
	@$(PIO) --version
	@$(PIO) project config --project-dir "$(PROJECT)/firmware" >/dev/null

platformio-build: platformio-toolcheck ## Build the pinned PlatformIO firmware target
	@$(PIO) run --project-dir "$(PROJECT)/firmware"
