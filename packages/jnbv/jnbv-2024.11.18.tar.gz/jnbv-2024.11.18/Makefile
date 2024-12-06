###############################################################################
# This makefile is made to simplify development work
###############################################################################

# Makefile stuff
.DEFAULT_GOAL := help
SHELL := /bin/bash
.ONESHELL:
THIS_FILE := $(lastword $(MAKEFILE_LIST))

# Set the umask so that everyone has atleast read access to results
UMASK := umask 002

# Colors
LIGHTPURPLE := \033[1;35m
GREEN := \033[32m
CYAN := \033[36m
BLUE := \033[34m
RED := \033[31m
NC := \033[0m

# Separator between output, 80 characters wide
define print_separator
	printf "$1"; printf "%0.s*" {1..80}; printf "$(NC)\n"
endef
print_line_green = $(call print_separator,$(GREEN))
print_line_blue = $(call print_separator,$(BLUE))
print_line_red = $(call print_separator,$(RED))


###############################################################################
##@ Help
###############################################################################

.PHONY: help

help:  ## Display this help message
	@printf "\n"
	$(print_line_blue)
	printf "$(BLUE)Jupyter Notebook and Kernel Validation $(CYAN)Makefile$(NC)\n"
	printf "    This makefile has been created to simplify development \n"
	printf "    work on Jupyter notebook and kernel validation routines.\n"
	$(print_line_blue)
	printf "\n"
	$(print_line_blue)
	printf "$(BLUE)Usage\n    $(CYAN)make $(NC)<target>\n"
	awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_-].*##/ \
	{ printf "    $(CYAN)%-27s$(NC) %s\n", $$1, $$2} /^##@/ \
	{ printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	$(print_line_blue)


###############################################################################
##@ Development of jnbv code
###############################################################################

.PHONY: venv clean-venv hdf5-kernel cli-execution

# Define the name of the virtual environment directory
VENV := venv

# Installation of conda & required modules
$(VENV)/bin/activate: development/venv-requirements.yml
	@printf "\n"
	$(MAKE) -s -f $(THIS_FILE) clean-venv

	# Use mamba instead of conda
	$(print_line_blue)
	miniconda_installer=Miniforge3-$$(uname)-$$(uname -m).sh
	miniconda_url="https://github.com/conda-forge/miniforge/releases/latest/download/$$miniconda_installer"
	printf "\n$(BLUE)Downloading miniconda from $$miniconda_url$(NC)\n"
	wget $$miniconda_url
	sh $$miniconda_installer -s -p $(VENV) -b
	rm $$miniconda_installer

	printf "\n$(BLUE)Installing development requirements$(NC)\n"
	./$(VENV)/bin/mamba env update \
		--name base \
		--file development/venv-requirements.yml

	printf "\n$(BLUE)Installing jnbv$(NC)\n"
	./$(VENV)/bin/pip install -e .

	printf "\n$(GREEN)DONE INSTALLING VENV$(NC)\n"
	$(print_line_green)
	printf "\n"

venv: $(VENV)/bin/activate ## Create virtual environment with conda

KERNEL_ENV_FILE := development/hdf5-kernel-env.yml
KERNEL_SPEC_FILE := $(VENV)/share/jupyter/kernels/hdf5-kernel/kernel.json

$(KERNEL_SPEC_FILE): $(VENV)/bin/activate $(KERNEL_ENV_FILE)
	@printf "\n"
	source $(VENV)/bin/activate
	$(print_line_blue)
	printf "\n$(BLUE)Creating hdf5-kernel conda environment$(NC)\n"
	mamba env create --file $(KERNEL_ENV_FILE)
	conda activate hdf5-kernel-environment
	printf "\n$(BLUE)Creating hdf5-kernel$(NC)\n"
	python -m ipykernel install --name=hdf5-kernel --prefix=$(VENV)/
	cat $(KERNEL_SPEC_FILE)
	printf "\n$(GREEN)DONE CREATING HDF5 KERNEL$(NC)\n"
	$(print_line_green)

hdf5-kernel: $(KERNEL_SPEC_FILE) ## Install example Jupyter kernel locally into venv

cli-execution: $(KERNEL_SPEC_FILE) ## Test CLI execution with example Jupyter kernel
	source $(VENV)/bin/activate
	jnbv development/example-hdf5-notebook.ipynb --kernel hdf5-kernel --validate

clean-venv: ## Remove virtual environment
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	rm -rf .tox


###############################################################################
##@ Testing of the jnbv code itself
###############################################################################

.PHONY: tox-lint tox-build-tests tox-execution-tests tox-reading-tests tox-testing-tests tox-comparison-tests tox-validation-tests tox-validation-tests-cli

tox-lint: $(VENV)/bin/activate ## Lint python code
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -r -e lint

tox-build-tests: $(VENV)/bin/activate ## run build tests 
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-build"

tox-execution-tests: $(VENV)/bin/activate ## Run execution tests
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-execution-tests-{valid,invalid}-kernel"

tox-reading-tests: $(VENV)/bin/activate ## Run reading tests
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-reading-tests"

tox-testing-tests: $(VENV)/bin/activate ## Run testing tests
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-testing-tests"

tox-comparison-tests: $(VENV)/bin/activate ## Run comparison tests
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-comparison-tests"

tox-validation-tests: $(VENV)/bin/activate ## Run validation tests
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-validation-tests-{valid,invalid}-kernel"

tox-validation-tests-cli: $(VENV)/bin/activate ## Run validation tests with CLI
	source $(VENV)/bin/activate
	export CONDA_EXE=mamba
	tox -e "py3{8,9,10,11,12}-validation-tests-cli"

clean-test: ## Remove tox and pytest files
	rm -rf .tox .pytest_cache

###############################################################################
##@ Building of the jnbv module
###############################################################################

.PHONY: build upload clean-build bump-version changelog

BUILD_OUTPUT_FILE := dist/jnbv-*.tar.gz

# Building of the module package
$(BUILD_OUTPUT_FILE): $(VENV)/bin/activate 
	source $(VENV)/bin/activate
	python -m build

# build is a shortcut target
build: $(BUILD_OUTPUT_FILE) ## Build the module package 

bump-version: ## Set version number & git tag - today's date plus count for today
	@printf "\n"

	# Create the version number from today's date
	datestamp=`date +"%Y.%-m.%-d"`
	daycommitcount=`git tag --list $$datestamp* | wc -w`
	versiontag=$${datestamp}
	if [ "$$daycommitcount" -gt 0 ]; then
		versiontag=$${datestamp}.$${daycommitcount}
	fi

	$(print_line_blue)
	printf "$(CYAN)datestamp:       $(NC)$$datestamp\n"
	printf "$(CYAN)daycommitcount:  $(NC)$$daycommitcount\n"
	printf "$(CYAN)versiontag:      $(NC)$$versiontag\n"
	$(print_line_blue)
	printf "\n"

	# Set package version number
	$(print_line_blue)
	printf "$(CYAN)Changing version in pyproject.toml$(NC)\n\n"
	sed -i "/^version =.*/ s//version = \"$$versiontag\"/" pyproject.toml
	printf "$(CYAN)New version of pyproject.toml: $(NC)\n"
	cat pyproject.toml
	$(print_line_blue)
	printf "\n"

	# Update changelog after a new tag is created, so that all the recent
	# commit information is in it
	git tag $$versiontag
	$(MAKE) -s -f $(THIS_FILE) changelog

	# Make a git commit
	$(print_line_blue)
	printf "$(CYAN)Commit changes$(NC)\n\n"
	git add -A
	git commit -m "bumped version in pyproject.toml to $$versiontag"
	$(print_line_blue)
	printf "\n"

	# Set git tag to be the same as the package version number
	$(print_line_blue)
	printf "$(CYAN)Setting new git tag:$(NC)\n  $$versiontag\n"
	# Some trickery with tags inorder to have most recent info in the changelog
	git tag -d $$versiontag
	git tag $$versiontag
	printf "\n$(CYAN)List of git tags:$(NC)\n"
	git tag
	$(print_line_blue)
	printf "\n"

	# Do not push - allow time for checks to be made first
	$(print_line_blue)
	printf "$(CYAN)If everything looks ok, push to gitlab:$(NC)\n"
	printf "  git push origin master\n"
	printf "  git push origin $$versiontag\n"
	$(print_line_blue)
	printf "\n"

changelog: ## Generate simple changelog from git tags and commits
	@printf "\n"
	$(print_line_blue)

	previous_tag=0
	printf "# JNBV CHANGELOG\n\n" > CHANGELOG.md

	# Loop over tags, oldest to newest
	for current_tag in `git tag --sort=-creatordate`
	do
		if [ "$$previous_tag" != 0 ];then
			# Print the current tag and date of the tag
			tag_date=`git log -1 --pretty=format:'%ad' --date=short $${previous_tag}`
			printf "## $${previous_tag} ($${tag_date})\n\n" >> CHANGELOG.md

			# Print all commit messages between this tag and the previous
			git log $${current_tag}...$${previous_tag} --pretty=format:'*  %s [View](https://gitlab.com/MAXIV-SCISW/JUPYTERHUB/jnbv/-/commit/%H)' --reverse | grep -v Merge >> CHANGELOG.md
			printf "\n\n" >> CHANGELOG.md
		fi
		previous_tag=$${current_tag}
	done

	printf "$(GREEN)Done generating CHANGELOG.md$(NC)\n"
	$(print_line_blue)
	printf "\n"

upload-testpypi: $(BUILD_OUTPUT_FILE) ## Upload the module to TestPyPi
	@printf "\n"
	source $(VENV)/bin/activate
	python3 -m twine upload --repository testpypi dist/*

upload-pypi: $(BUILD_OUTPUT_FILE) ## Upload the module to PyPi
	@printf "\n"
	source $(VENV)/bin/activate
	python3 -m twine upload --repository pypi dist/*

clean-build: ## Remove build files
	rm -rf dist build jnbv.egg-info
