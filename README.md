# Cosmo Backend

This project was generated using fastapi_template.

## Installation

To setup the project use this set of commands:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the app
```shell
uvicorn app.web.application:get_app --reload --factory
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## Project structure

```bash
$ tree "backend"
app
├── conftest.py  # Fixtures for all tests.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

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

By default it runs:
* black (formats your code);
* isort (sorts imports in all files);

You can read more about pre-commit here: https://pre-commit.com/
