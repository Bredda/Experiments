##@ Utility
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: uv
uv:  ## Install uv if it's not present.
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	
.PHONY: install

install: uv ## Install dev dependencies
	uv sync --directory experiments
	uv sync --directory api
.PHONY: lint

lint:  ## Run linters
	uv run --directory experiments ruff check
	uv run --directory api ruff check

.PHONY: run
run: 
	uv run --directory experiments experiments run scenarios/basic.yml

.PHONY: test
test: 
	uv run --directory experiments pytest 