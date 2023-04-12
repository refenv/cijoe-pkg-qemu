#
# This Makefile serves as convenient command-line auto-completion
#
PROJECT_NAME=cijoe-pkg-qemu
PYTEST=$(shell pipx environment -v PIPX_LOCAL_VENVS)/${PROJECT_NAME}/bin/pytest
PYTHON_SYS=python3
PYTHON_VENV=$(shell pipx environment -v PIPX_LOCAL_VENVS)/${PROJECT_NAME}/bin/python3
PIPX=pipx
TWINE=twine

define default-help
# invoke: 'make uninstall', 'make install'
endef
.PHONY: default
default: build
	@echo "## ${PROJECT_NAME}: make default"
	@echo "## ${PROJECT_NAME}: make default [DONE]"

define  all-help
# Do all: clean uninstall build install
endef
.PHONY: all
all: uninstall clean deps build install info test

define deps-help
# Dependencies
endef
.PHONY: deps
deps:
	${PIPX} install twine || true

define info-help
# Dump various Python / tooling information
endef
.PHONY: info
info:
	@echo "## ${PROJECT_NAME}: make info"
	${PYTEST} --version || true
	${PYTHON_SYS} --version || true
	${PYTHON_VENV} --version || true
	${PIPX} --version || true
	${TWINE} --version || true
	@echo "## ${PROJECT_NAME}: make info [DONE]"

define docker-help
# drop into a docker instance with the repository bind-mounted at /tmp/source
endef
.PHONY: docker
docker:
	@echo "## ${PROJECT_NAME}: docker"
	@docker run -it -w /tmp/source --mount type=bind,source="$(shell pwd)",target=/tmp/source ghcr.io/xnvme/xnvme-deps-debian-bullseye:next bash
	@echo "## ${PROJECT_NAME}: docker [DONE]"

define format-help
# run code format (style, code-conventions and language-integrity) on staged changes
endef
.PHONY: format
format:
	@echo "## ${PROJECT_NAME}: format"
	@pre-commit run
	@echo "## ${PROJECT_NAME}: format [DONE]"

define format-all-help
# run code format (style, code-conventions and language-integrity) on staged and committed changes
endef
.PHONY: format-all
format-all:
	@echo "## ${PROJECT_NAME}: format-all"
	@pre-commit run --all-files
	@echo "## ${PROJECT_NAME}: format-all [DONE]"

define build-help
# Build the package (source distribution package)
endef
.PHONY: build
build:
	@echo "## ${PROJECT_NAME}: make build-sdist"
	@${PYTHON_SYS} setup.py sdist
	@${PYTHON_SYS} setup.py bdist_wheel
	@echo "## ${PROJECT_NAME}: make build-sdist [DONE]"

define install-help
# install for current user
endef
.PHONY: install
install:
	@echo "## ${PROJECT_NAME}: make install"
	@${PIPX} install dist/*.tar.gz --include-deps
	@echo "## ${PROJECT_NAME}: make install [DONE]"

define uninstall-help
# uninstall
#
# Prefix with 'sudo' when uninstalling a system-wide installation
endef
.PHONY: uninstall
uninstall:
	@echo "## ${PROJECT_NAME}: make uninstall"
	@${PIPX} uninstall ${PROJECT_NAME} || echo "Cannot uninstall => That is OK"
	@echo "## ${PROJECT_NAME}: make uninstall [DONE]"

define examples-help
# Run pytest on the testcase-test
endef
.PHONY: test
test:
	@echo "## ${PROJECT_NAME}: make test"
	${PYTEST} --pyargs cijoe.qemu.selftest --config src/cijoe/qemu/configs/default-config.toml
	@echo "## ${PROJECT_NAME}: make test [DONE]"

define examples-help
# Run pytest on the testcase-test
endef
.PHONY: release
release: all
	@echo "## ${PROJECT_NAME}: make release"
	@echo -n "# rel: "; date
	@${TWINE} upload dist/*
	@echo "## ${PROJECT_NAME}: make release"

define clean-help
# clean the Python build dirs (build, dist)
endef
.PHONY: clean
clean:
	@echo "## ${PROJECT_NAME}: clean"
	@git clean -fdx || echo "Failed git-clean ==> That is OK"
	@echo "## ${PROJECT_NAME}: clean [DONE]"
