import sys
from dataclasses import dataclass

from life_analytics.domain.errors import ErrorDiagnostic


def get_user_commands() -> str:
    return " ".join(sys.argv[1:])


@dataclass(frozen=True)
class CLIErrorDiagnostic:
    message: str
    source: str
    source_highlight: str
    description: str | None = None
    help: str | None = None


def to_cli_diagnostic(
    diagnostic: ErrorDiagnostic, source: str, source_highlight: str
) -> CLIErrorDiagnostic:
    return CLIErrorDiagnostic(
        message=diagnostic.message,
        source=source,
        source_highlight=source_highlight,
        description=diagnostic.description,
        help=diagnostic.help,
    )


def get_flag_source(short_flag: str, long_flag: str, value: str) -> tuple[str, str]:
    user_commands = get_user_commands()
    source_highlight = f"-{short_flag} {value}"

    if source_highlight not in user_commands:
        source_highlight = f"--{long_flag} {value}"

    return user_commands, source_highlight


def get_argument_source(value: str) -> tuple[str, str]:
    user_commands = get_user_commands()

    if value not in user_commands:
        raise ValueError("value in get_flag_source() has to be in user_commands")

    return user_commands, value
