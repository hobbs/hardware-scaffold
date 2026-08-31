PYTHON ?= python3
PROJECT ?=
NAME ?=
SLUG ?=
GOAL ?=

.PHONY: help check init check-project check-strict

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
