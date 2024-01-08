# GPT-Crawler Backend

Frontend repo is [here](https://github.com/astelmach01/GPT-crawler-frontend)

## Installation

To setup the project use this set of commands:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Running the app

```shell
python -m app
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

An example of .env file:

```bash
BACKEND_RELOAD="True"
BACKEND_PORT="8000"
BACKEND_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs ruff for code formatting and mypy for type checking.

You can read more about pre-commit here: https://pre-commit.com/
