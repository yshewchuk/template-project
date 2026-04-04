.PHONY: help validate-planning check-ownership lint test

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

validate-planning: ## Validate .planning/ YAML files against schemas
	@python3 scripts/planning/validate.py

check-ownership: ## Verify PR file changes against OWNERS.yaml
	@python3 scripts/ownership/check.py

extract-context: ## Extract filtered planning context for a persona (PERSONA=tech-lead)
	@python3 scripts/planning/extract-context.py --persona $(PERSONA)

lint: ## Run linters across all projects
	@echo "Linting not yet configured for individual projects."

test: ## Run tests across all projects
	@echo "Tests not yet configured for individual projects."
