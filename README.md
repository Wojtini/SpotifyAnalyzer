<<<<<<< HEAD
# Spotify Analyzer

## Requirements
There are 2 sets of requirements.txt:
1. requirements.txt with requirements to 
=======
<h1 align="center">
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
>>>>>>> 83db2983746822ff757f30bdeb7a4d0434944290
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