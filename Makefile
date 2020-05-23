help:
	@echo "This project supports the following targets"
	@echo ""
	@echo " make help - show this text"
	@echo " make env - Install and update the env folder"
	@echo " make submodules - make sure that the submodules are up-to-date"
	@echo " make lint - run flake8"
	@echo " make unittest - run the tests defined in the unittest subdirectory"
	@echo " make functional - run the tests defined in the functional subdirectory"
	@echo " make test - run the unittests and lint"
	@echo ""

env:
	@echo "Installing/updating env from requirements.txt"
	@pip3 install --target=./env -r requirements.txt

submodules:
	@echo "Cloning submodules"
	@git submodule update --init --recursive

lint:
	@echo "Running flake8"
	@tox -e lint

test: lint unittest functional

unittest:
	@tox -e unit

functional:
	@tox -e functional

# The targets below don't depend on a file
.PHONY: lint test unittest functional help submodules env
