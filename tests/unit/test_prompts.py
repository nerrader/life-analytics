from typing import TYPE_CHECKING

import pytest

from life_analytics.logic import prompts

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_validate_datetime_with_valid_datetime() -> None:
    assert prompts._validate_datetime("00:00") is True
    assert prompts._validate_datetime("18:20") is True


def test_validate_datetime_with_invalid_datetime() -> None:
    assert isinstance(prompts._validate_datetime("25:00"), str)
    assert isinstance(prompts._validate_datetime("24:60"), str)
    assert isinstance(prompts._validate_datetime("7 :59 "), str)


def test_validate_rating_with_valid_rating() -> None:
    assert prompts._validate_rating("3") is True
    assert prompts._validate_rating("1.5") is True
    assert prompts._validate_rating("4.234758") is True
    assert prompts._validate_rating("1") is True
    assert prompts._validate_rating("5") is True


def test_validate_rating_with_invalid_rating() -> None:
    assert isinstance(prompts._validate_rating("11"), str)
    assert isinstance(prompts._validate_rating("-1"), str)
    assert isinstance(prompts._validate_rating("0"), str)


def test_rating_prompt_cancelled_raises_runtime_error(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")

    # simulate a keyboard interrupt
    mock_rating_prompt.return_value.ask.return_value = None

    with pytest.raises(RuntimeError):
        prompts.ask_rating_question(
            "If my code is correct, this should raise a RuntimeError"
        )


def test_rating_prompt_returns_correct_value(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")
    mock_rating_prompt.return_value.ask.return_value = 5

    assert (
        prompts.ask_rating_question("If my code is correct, this should return 5.") == 5
    )


def test_datetime_prompt_cancelled_raises_runtime_error(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")

    # simulate a keyboard interrupt
    mock_rating_prompt.return_value.ask.return_value = None

    with pytest.raises(RuntimeError):
        prompts.ask_datetime_question(
            "If my code is correct, this should raise a RuntimeError"
        )


def test_datetime_prompt_returns_correct_value(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")
    mock_rating_prompt.return_value.ask.return_value = "19:49"

    assert (
        prompts.ask_datetime_question("If my code is correct, this should return 19:49")
        == "19:49"
    )


def test_activity_name_prompt_cancelled_raises_runtime_error(
    mocker: MockerFixture,
) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")

    # simulate a keyboard interrupt
    mock_rating_prompt.return_value.ask.return_value = None

    with pytest.raises(RuntimeError):
        prompts.ask_activity_category(
            "If my code is correct, this should raise a RuntimeError"
        )


def test_activity_name_prompt_returns_correct_value(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")
    mock_rating_prompt.return_value.ask.return_value = "MAINT"

    assert (
        prompts.ask_activity_category("If my code is correct, this should return MAINT")
        == "MAINT"
    )


def test_ask_for_confirmation_skip_value() -> None:
    assert prompts.ask_for_confirmation("Continue?", True) is True
