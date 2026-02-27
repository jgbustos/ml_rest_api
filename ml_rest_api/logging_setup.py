"""Loguru-based logging setup that intercepts all stdlib logging."""

import inspect
import logging
import sys
from typing import Any
import click
from loguru import logger


class InterceptHandler(logging.Handler):
    """Intercepts stdlib logging calls and redirects them to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        for _ in range(6):
            if frame is not None:
                frame = frame.f_back
                depth += 1
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1

        for line in record.getMessage().splitlines():
            logger.opt(depth=depth, exception=record.exc_info).log(level, line)


def setup_logging(level: str = "DEBUG") -> None:
    """Configure loguru and intercept all stdlib logging."""
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )
    # Replace root logger handler — all child loggers propagate here by default
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    # Clear handlers on existing child loggers and ensure they propagate to root
    for name in logging.root.manager.loggerDict:  # pylint: disable=no-member
        existing = logging.getLogger(name)
        existing.handlers.clear()
        existing.propagate = True
    # Intercept click.echo (used by Flask/Werkzeug for * startup lines)
    _original_echo = click.echo

    def _echo_to_loguru(
        message: Any = None,
        file: Any = None,
        nl: bool = True,
        err: bool = False,
        color: Any = None,
    ) -> None:
        if message is not None and file is None and not err:
            logger.opt(depth=1).info(str(message))
        else:
            _original_echo(message, file=file, nl=nl, err=err, color=color)

    click.echo = _echo_to_loguru  # type: ignore[assignment]

    # Also intercept click.secho (used by Werkzeug for * Running on lines)
    _original_secho = click.secho

    def _secho_to_loguru(
        message: Any = None,
        file: Any = None,
        nl: bool = True,
        err: bool = False,
        color: Any = None,
        **styles: Any,
    ) -> None:
        if message is not None and file is None and not err:
            logger.opt(depth=1).info(str(message))
        else:
            _original_secho(message, file=file, nl=nl, err=err, color=color, **styles)

    click.secho = _secho_to_loguru  # type: ignore[assignment]
