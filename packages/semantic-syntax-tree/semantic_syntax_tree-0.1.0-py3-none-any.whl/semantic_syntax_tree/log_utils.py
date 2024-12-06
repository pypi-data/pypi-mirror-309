import logging
from contextlib import contextmanager
from typing import Any, Generator, Protocol


class LogMessageFormatter(Protocol):
    def __call__(self, msg: Any) -> Any: ...


@contextmanager
def log_message_formatter(
    formatter: LogMessageFormatter,
) -> Generator[None, None, None]:
    """Apply the formatter to all log records emitted within the context."""
    old_factory = logging.getLogRecordFactory()

    def new_factory(*args: Any, **kwargs: Any):
        record = old_factory(*args, **kwargs)
        record.msg = formatter(record.msg)
        return record

    try:
        logging.setLogRecordFactory(new_factory)
        yield
    finally:
        logging.setLogRecordFactory(old_factory)


@contextmanager
def log_message_prefix(prefix: str) -> Generator[None, None, None]:
    """Add a prefix to all log records emitted within the context."""
    with log_message_formatter(lambda msg: f"{prefix}{msg}"):
        yield
