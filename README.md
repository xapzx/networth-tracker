### Python Package Manager
uv - [Documentation](https://docs.astral.sh/uv/)

Install uv:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone project:
```
```

Initialise uv:
```
cd network-tracker
uv init .
```

To add packages:
```
uv add <package>

# Add to dev dependencies
uv add --dev

# Installing production dependencies
uv sync --no-dev --locked
```

Run server
```
uv run manage.py runserver
```

### Pytest
```
uv run pytest
```

### Pytest Coverage
```
python -m pytest --cov=networth_tracker networth_tracker/tests
```
