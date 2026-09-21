import pytest
from pytest_mock import MockerFixture

from life_analytics.cli.diagnostics import (
    CLIErrorDiagnostic,
    get_argument_source,
    get_flag_source,
    get_user_commands,
    to_cli_diagnostic,
)
from life_analytics.domain.errors import ErrorDiagnostic


def test_get_user_commands(mocker: MockerFixture) -> None:
    mocker.patch("sys.argv", ["program", "foo", "bar", "--baz"])

    assert get_user_commands() == "foo bar --baz"


def test_to_cli_diagnostic() -> None:
    diagnostic = ErrorDiagnostic(
        message="invalid value",
        description="the value is not valid.",
        help="use a positive integer.",
    )

    result = to_cli_diagnostic(
        diagnostic,
        source="foo --count -1",
        source_highlight="--count -1",
    )

    assert result == CLIErrorDiagnostic(
        message="invalid value",
        source="foo --count -1",
        source_highlight="--count -1",
        description="the value is not valid.",
        help="use a positive integer.",
    )


def test_to_cli_diagnostic_without_optional_fields() -> None:
    diagnostic = ErrorDiagnostic(
        message="Invalid value",
        description=None,
        help=None,
    )

    result = to_cli_diagnostic(
        diagnostic,
        source="foo",
        source_highlight="foo",
    )

    assert result == CLIErrorDiagnostic(
        message="Invalid value",
        source="foo",
        source_highlight="foo",
        description=None,
        help=None,
    )


def test_get_flag_source_uses_short_flag(mocker: MockerFixture) -> None:
    mocker.patch(
        "sys.argv",
        ["program", "foo", "-c", "123"],
    )

    assert get_flag_source("c", "count", "123") == (
        "foo -c 123",
        "-c 123",
    )


def test_get_flag_source_falls_back_to_long_flag(
    mocker: MockerFixture,
) -> None:
    mocker.patch(
        "sys.argv",
        ["program", "foo", "--count", "123"],
    )

    assert get_flag_source("c", "count", "123") == (
        "foo --count 123",
        "--count 123",
    )


def test_get_argument_source(mocker: MockerFixture) -> None:
    mocker.patch(
        "sys.argv",
        ["program", "foo", "123", "bar"],
    )

    assert get_argument_source("123") == (
        "foo 123 bar",
        "123",
    )


def test_get_argument_source_raises_when_value_is_missing(
    mocker: MockerFixture,
) -> None:
    mocker.patch(
        "sys.argv",
        ["program", "foo", "bar"],
    )

    with pytest.raises(ValueError):
        get_argument_source("123")
