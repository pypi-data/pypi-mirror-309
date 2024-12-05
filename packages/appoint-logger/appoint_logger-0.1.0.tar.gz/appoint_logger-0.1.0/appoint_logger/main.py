
from colorama import Fore, Style, init
import logging
import logging.handlers
import threading
import queue
from datetime import datetime, UTC
from httpx import Client, RequestError
from pathlib import Path
from typing import Dict, Any, List
import signal
import atexit
import json


init(autoreset=True)

LOG_COLORS = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA
}


class BackgroundHandler(logging.Handler):
    def __init__(self, target_handler):
        super().__init__()
        self.target_handler = target_handler
        self.log_queue = queue.Queue()
        self.thread = threading.Thread(target=self._process_logs, daemon=True)
        self.running = True
        self.thread.start()

    def emit(self, record):
        if self.running:
            self.log_queue.put(record)

    def _process_logs(self):
        while True:
            record = self.log_queue.get()
            if record is None:  # Stop signal
                break
            self.target_handler.emit(record)

    def shutdown(self):
        """Flush the queue and stop the thread."""
        self.running = False
        self.log_queue.put(None)
        self.thread.join()


class JsonFormatter(logging.Formatter):
    def __init__(self, tz=UTC):
        super().__init__()
        self.timezone = tz

    def formatTime(self, record):
        dt = datetime.fromtimestamp(record.created, self.timezone)
        return dt.isoformat()

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", None),
            "module": record.module,
            "filename": record.filename,
            "line": record.lineno,
        }
        return json.dumps(log_record)


class Formatter(logging.Formatter):
    def __init__(self, fmt: str, tz=UTC, colorize: bool = False):
        super().__init__()
        self.default_format = fmt
        self.timezone = tz
        self.colorize = colorize

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

    def format(self, record):
        record.timestamp = self.formatTime(record)
        record.context = getattr(record, "context", "")
        formatted_message = super().format(record)

        formatted_message = self.default_format.format(
            timestamp=record.timestamp, context=record.context, name=record.name, level=record.levelname, message=record.msg)

        if self.colorize:
            color = LOG_COLORS.get(record.levelname, Style.RESET_ALL)
            formatted_message = f"{color}{formatted_message}{Style.RESET_ALL}"

        return formatted_message


class HttpHandler(logging.Handler):
    def __init__(self, url, headers: Dict[str, str] = None):
        super().__init__()
        self.url = url
        self.headers = headers or {}
        self.http_client = Client()

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.http_client.post(
                self.url, json={"log": log_entry}, headers=self.headers)
        except RequestError:
            pass


class SeqHandler(logging.Handler):
    def __init__(self, url, headers=None, tz=UTC):
        super().__init__()
        self.url = url
        self.headers = headers or {}
        self.headers["Content-Type"] = "application/json"
        self.http_client: Client = Client()
        self.timezone = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.timezone)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat().replace("+00:00", "Z")

    def format(self, record):

        event = {
            "Timestamp": self.formatTime(record=record),
            "Level": record.levelname,
            "MessageTemplate": record.msg,
            "MinimumLevelAccepted": logging.INFO,
            "Properties": {
                "module": record.module,
                "filename": record.filename,
                "line": record.lineno,
                "context": getattr(record, "context", None),
                **getattr(record, "kwargs", {})
            },
        }
        return event

    def emit(self, record):
        log_event = self.format(record)
        try:
            payload = {
                "Events": [log_event]  # Wrap the log event in an Events array
            }
            response = self.http_client.post(
                self.url, json=payload, headers=self.headers)
            print(response.text)
        except RequestError:
            pass


class AppointLogger:

    background_handlers: List[BackgroundHandler] = []

    def __init__(self, name: str, level=logging.DEBUG, format: str = "[{timestamp}] {name} {level}: {message}", timezone=UTC):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.format = format
        self.timezone = timezone
        self.level = level

    def add_console_output(self, level=None, colorize: bool = True):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level or self.level)
        console_handler.setFormatter(
            Formatter(fmt=self.format, tz=self.timezone, colorize=colorize))
        self.logger.addHandler(console_handler)

    def add_file_output(self, file_path: str, level=None):

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level or self.level)
        file_handler.setFormatter(Formatter(
            fmt=self.format, tz=self.timezone))

        handler = BackgroundHandler(file_handler)
        self.background_handlers.append(handler)
        self.logger.addHandler(handler)

    def add_json_output(self, file_path: str, level=None):
        json_handler = logging.FileHandler(file_path)
        json_handler.setLevel(level or self.level)
        json_handler.setFormatter(JsonFormatter(self.timezone))
        handler = BackgroundHandler(json_handler)
        self.background_handlers.append(handler)
        self.logger.addHandler(handler)

    def add_rotating_file_output(self, file_path: str, interval="midnight", level=None):
        rotating_handler = logging.handlers.TimedRotatingFileHandler(
            file_path, when=interval
        )
        rotating_handler.setLevel(level or self.level)
        rotating_handler.setFormatter(
            Formatter(fmt=self.format, tz=self.timezone))
        handler = BackgroundHandler(rotating_handler)
        self.background_handlers.append(handler)
        self.logger.addHandler(handler)

    def add_http_output(self, url: str, level=None):
        http_handler = HttpHandler(url)
        http_handler.setLevel(level or self.level)
        http_handler.setFormatter(Formatter(
            fmt=self.format, tz=self.timezone))
        handler = BackgroundHandler(http_handler)
        self.background_handlers.append(handler)
        self.logger.addHandler(handler)

    def add_seq_output(self, url: str, headers: Dict[str, str] = None, level=None):
        seq_handler = SeqHandler(url, headers)
        seq_handler.setLevel(level or self.level)
        handler = BackgroundHandler(seq_handler)
        self.background_handlers.append(handler)
        self.logger.addHandler(handler)

    def log(self, level, message, context=None, params: Dict[str, Any] = None):

        formatted_message = message.format(**params) if params else message
        extra = {"kwargs": params}
        if context:
            extra["context"] = context
        self.logger.log(level, formatted_message, extra=extra, exc_info=params)

    def debug(self, message, **kwargs):
        self.log(level=logging.DEBUG, message=message, params=kwargs)

    def info(self, message, **kwargs):
        self.log(level=logging.INFO, message=message, params=kwargs)

    def warning(self, message, **kwargs):
        self.log(level=logging.WARNING, message=message, params=kwargs)

    def error(self, message, **kwargs):
        self.log(level=logging.ERROR, message=message, params=kwargs)

    def critical(self, message, **kwargs):
        self.log(level=logging.CRITICAL, message=message, params=kwargs)

    @staticmethod
    def shutdown(*args, **kwargs):
        for handler in AppointLogger.background_handlers:
            handler.shutdown()


signal.signal(signal.SIGINT, AppointLogger.shutdown)
signal.signal(signal.SIGTERM, AppointLogger.shutdown)
atexit.register(AppointLogger.shutdown)
