##@ Utility

.PHONY: help
help:  ## Display available commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: uv
uv:  ## Install uv if it's not present
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh

##@ Project

.PHONY: install
install: uv  ## Install all project dependencies
	$(MAKE) -C experiments install
	$(MAKE) -C api install
	$(MAKE) -C ui install

.PHONY: lint
lint:  ## Run all linters
	$(MAKE) -C experiments lint
	$(MAKE) -C api lint
	$(MAKE) -C ui lint

.PHONY: test
test:  ## Run all tests
	$(MAKE) -C experiments test

.PHONY: run
run:  ## Run the default experiment
	$(MAKE) -C experiments run

##@ Development

.PHONY: dev
dev:  ## Start API development server
	@$(MAKE) -C api dev & \
	$(MAKE) -C ui dev & \
	wait
>>>>>>> Stashed changes
