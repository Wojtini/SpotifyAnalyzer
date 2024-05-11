# Spotify Analyzer

## Requirements
There are 2 sets of requirements.txt:
1. requirements.txt with requirements to 
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
mypy SpotifyAnalyzer --disallow-untyped-defs --warn-unreachable
```
