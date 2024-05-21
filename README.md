# 
<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
  <strong>Spotify Analyzer</strong>
</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-v3.11-yellow" alt="Python Badge">
  <img src="https://img.shields.io/badge/Contributors-3-green" alt="Contributors Badge">
  <img src="https://img.shields.io/badge/Version-0.0-red" alt="Hello World Badge">
</div>

## Requirements
There are 2 sets of requirements.txt:
1. requirements.txt
2. requirements_dev.txt - superset of 1. which additionally contains libraries
for development (tests and linters)

Installing;
```shell
pip install -r {requirements_file}
# or using pip-tools
pip-sync {requirements_file}
```

## Linters
### Style - ruff
Main linter rules are defined in pyproject.toml
```shell
ruff check
```
### Typing mypy
For check typing mypy is used. Command:
```shell
mypy app --disallow-untyped-defs --warn-unreachable
```

## Running
```shell
fastapi dev app/main.py
```