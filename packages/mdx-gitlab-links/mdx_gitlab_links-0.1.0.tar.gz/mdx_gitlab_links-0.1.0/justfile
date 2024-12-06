[private]
default:
  @just --list

# Run command within environment
run +args: uv
  uv run -- {{args}}

# Clean caches and artifacts
clean:
  rm -rf dist/ .coverage

# Run linter
lint: uv
  uv run --only-group lint -- ruff check --output-format concise

# Dry run formatter and output the diffs
fmt: uv
  uv run --only-group lint -- ruff format --diff

# Run the mypy type-checker
mypy: uv
  uv run --only-group mypy -- mypy

# Build -----------------------------------------------------------------------

# Print project version
version: uv
  @uv run --only-group build -- python -m setuptools_scm

# Build project
build: uv
  uv build --no-sources
  uv run --only-group build -- check-wheel-contents dist/*-$(just version)-*.whl

# Print wheel contents
whl-contents:
  @file=dist/*-$(just version)-*.whl; \
  [ -e $file ] \
  && unzip -Z1 $file | tree -a --fromfile . \
  || (echo 'whl not found.'; exit 1)

# Print sdist contents
sdist-contents:
  @file=dist/*-$(just version).tar.gz; \
  [ -e $file ] \
  && tar -tf $file | tree -a --fromfile . \
  || (echo 'sdist not found.'; exit 1)

# Test & coverage -------------------------------------------------------------

# Run the test suite with coverage
test *args: uv
  uv run --group testcov -- coverage run -m pytest {{args}}

# Report coverage of the last runned test
report *args:
  uv run --only-group coverage -- coverage report {{args}}

# Run test suite and report coverage
testcov *args: (test args) report

# Private ---------------------------------------------------------------------

# Ensure uv is installed
[private]
uv:
  @uv -V > /dev/null || (echo 'Please install uv: https://github.com/astral-sh/uv'; exit 1)

