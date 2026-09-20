import pytest
from pytest_mock import MockerFixture

from life_analytics.cli import prompts
from life_analytics.domain.errors import RequiredQuestionCancelledError


def test_rating_prompt_cancelled_raises_runtime_error(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")

    # simulate a keyboard interrupt
    mock_rating_prompt.return_value.ask.return_value = None

    with pytest.raises(RequiredQuestionCancelledError):
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

    with pytest.raises(RequiredQuestionCancelledError):
        prompts.ask_time_question(
            "If my code is correct, this should raise a RuntimeError"
        )


def test_datetime_prompt_returns_correct_value(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")
    mock_rating_prompt.return_value.ask.return_value = "19:49"

    assert (
        prompts.ask_time_question("If my code is correct, this should return 19:49")
        == "19:49"
    )


def test_activity_category_prompt_skips_if_skip_value_is_valid(
    mocker: MockerFixture,
) -> None:
    mock_activity_category_prompt = mocker.patch("questionary.text")

    mock_activity_category_prompt.assert_not_called()
    assert (
        prompts.ask_activity_category(
            "This question should be skipped.", skip_value="MAINT"
        )
        == "MAINT"
    )


def test_activity_category_prompt_cancelled_raises_runtime_error(
    mocker: MockerFixture,
) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")

    # simulate a keyboard interrupt
    mock_rating_prompt.return_value.ask.return_value = None

    with pytest.raises(RequiredQuestionCancelledError):
        prompts.ask_activity_category(
            "If my code is correct, this should raise a RuntimeError"
        )


def test_activity_category_prompt_returns_correct_value(mocker: MockerFixture) -> None:
    mock_rating_prompt = mocker.patch("questionary.text")
    mock_rating_prompt.return_value.ask.return_value = "MAINT"

    assert (
        prompts.ask_activity_category("If my code is correct, this should return MAINT")
        == "MAINT"
    )


# we will not test ask_activity_description()
# since theres literally nothing worthwhile to test


def test_ask_for_confirmation_skip_value() -> None:
    assert prompts.ask_for_confirmation("Continue?", True) is True
