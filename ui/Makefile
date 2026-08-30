##@ Utility

.PHONY: help
help:  ## Display available API commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\n\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

.PHONY: install
install:  ## Install dependencies
	pnpm install

.PHONY: lint
lint:  ## Run linters
	pnpm lint

.PHONY: dev
dev:  ## Start the development server
	pnpm dev

.PHONY: sync-types
sync-types:
	pnpm dlx openapi-typescript http://localhost:8000/openapi.json \
	-o lib/api-types.ts