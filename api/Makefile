##@ Utility

.PHONY: help
help:  ## Display available API commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

.PHONY: install
install:  ## Install dependencies
	uv sync

.PHONY: lint
lint:  ## Run linters
	uv run ruff check

.PHONY: dev
dev:  ## Start the development server
	uv run uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload