##@ Utility

.PHONY: help
help:  ## Display available engine commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

.PHONY: install
install:  ## Install dependencies
	uv sync

.PHONY: lint
lint:  ## Run linter
	uv run ruff check $(ARGS)

.PHONY: test
test:  ## Run tests
	uv run pytest

.PHONY: run
run:  ## Run the basic scenario
	uv run experiments run ./scenarios/basic.yml