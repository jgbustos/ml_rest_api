# CLAUDE.md

## Project Overview
A RESTful API that serves predictions from a trained ML model, built with Python 3 and Flask-RESTX.

## Environment
- Python 3.13 (venv at `venv/`)
- Activate venv: `source venv/Scripts/activate` (bash on Windows)

## Quality Gate
Run before committing:
```
powershell.exe -File make.ps1
```
Checks: black (formatter) → pylint → mypy. Must score 10.00/10 and zero mypy errors.

## Dependencies
- `requirements.txt` — pinned runtime deps (Flask, flask-restx, numpy, pandas, loguru, etc.)
- `requirements-dev.txt` — dev tools (black, pylint, mypy)
- `tests/requirements.txt` — test deps (pytest, requests, openapi-spec-validator)
- Update all three when installing new packages in the venv

## Git Workflow
- Branch: `master`
- Remote: `https://github.com/jgbustos/ml_rest_api.git`
- Git user email: `35463898+jgbustos@users.noreply.github.com` (GitHub no-reply, required to push)
- Run quality gate before every commit
- Never commit `.claude/` directory

## Key Architecture Decisions

### Logging (loguru)
- Entry point: `ml_rest_api/logging_setup.py` → `setup_logging()`
- Called once in `app.py` after `Flask(__name__)`
- `InterceptHandler` redirects all stdlib `logging` calls to loguru
- Multi-line log messages are split per line so each gets a loguru header
- `click.echo` and `click.secho` are monkey-patched to capture Flask/Werkzeug `* startup lines`
- All modules keep using `getLogger(__name__)` — no need to import loguru directly

### CSRF Protection
- `CSRFProtect` is bound to the app in `initialize_app()` after `configure_app()`
- Controlled via `WTF_CSRF_ENABLED` setting (default: `True`)

### Type Annotations
- Use built-in generics (`dict[str, Any]`, `list[str]`) not `typing.Dict`/`typing.List`
- flask-restx has incomplete stubs — suppress with `# type: ignore` at import and decorator sites
- Pylance strictness is high; suppress false positives with `# type: ignore[specific-code]`

### ML Model
- Model module loaded dynamically via `TrainedModelWrapper` in `wrapper.py`
- Module name configured via `TRAINED_MODEL_MODULE_NAME` env var or settings
- `ml_trained_model.py` is the default/example model module

## Docker
- `Dockerfile` uses `ENTRYPOINT ["python3"]` + `CMD ["ml_rest_api/app.py"]`
- `docker-compose.yml` `command` must only pass the script path, not `python3` again
- `.dockerignore` excludes: venv, tests, nginx, docker-compose, CI config, dev requirements

## CI/CD
- CircleCI config: `.circleci/config.yml`
- Python image: `cimg/python:3.13`
- Cache key: `v1-dependencies-py313-...`
- Requires a CircleCI checkout key (User Key via GitHub OAuth)
