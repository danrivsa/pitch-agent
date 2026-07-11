from __future__ import annotations

import sys
from typing import Any, Callable, TextIO

RESET = "\033[0m"


def _colorize(text: str, color_code: str) -> str:
    return f"{color_code}{text}{RESET}"


def cyan(text: str) -> str:
    return _colorize(text, "\033[96m")


def green(text: str) -> str:
    return _colorize(text, "\033[92m")


def purple(text: str) -> str:
    return _colorize(text, "\033[95m")


def yellow(text: str) -> str:
    return _colorize(text, "\033[93m")


def orange(text: str) -> str:
    return _colorize(text, "\033[38;5;208m")


def red(text: str) -> str:
    return _colorize(text, "\033[91m")


def _log(level: str, value: Any, colorizer: Callable[[str], str], *, stream: TextIO = sys.stdout) -> None:
    print(f"{colorizer(f'[{level}]')} {value}", file=stream)


def log_config(value: Any) -> None:
    _log("CONFIG", value, yellow)


def log_info(value: Any) -> None:
    _log("INFO", value, cyan)


def log_error(value: Any) -> None:
    _log("ERROR", value, red, stream=sys.stderr)
    
def log_agent(value: Any) -> None:
    _log("AGENT", value, green)
    
def log_reasoning(value: Any) -> None:
    _log("REASONING", value, purple)
    
def log_runtime(value: Any) -> None:
    _log("RUNTIME", value, purple)
    
def log_tool(value: Any) -> None:
    _log("TOOL", value, orange)


if __name__ == "__main__":
    log_config("This is a config message.")
    log_info("This is an info message.")
    log_error("This is an error message.")
    log_agent("This is an agent message.")
    log_runtime("This is a runtime message.")