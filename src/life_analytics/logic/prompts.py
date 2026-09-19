from collections.abc import Iterable
from datetime import datetime
from typing import Literal

import questionary

from life_analytics.errors import RequiredQuestionCancelledError
from life_analytics.utils.time_utils import normalize_datetime, validate_datetime


def _validate_rating(value: str) -> Literal[True] | str:
    """To be passed into questionary validate keyword to validate rating questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """

    try:
        rating = float(value)
    except ValueError:
        return "Please enter a value between 1 and 5."

    if 1 <= rating <= 5:
        return True
    return "Please enter a value between 1 and 5."


def ask_rating_question(prompt: str) -> float:
    """The helper function to ask questions requiring rating in 1-5.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.

    Returns:
        float: The rating value between 1 and 10.
    """
    rating: float | None = questionary.text(
        prompt,
        validate=_validate_rating,
    ).ask()

    if rating is None:
        raise RequiredQuestionCancelledError("User skipped the rating question prompt.")

    return rating


def _validate_time(value: str) -> Literal[True] | str:
    """To be passed into questionary validate keyword to validate datetime questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return "Please enter a valid time in HH:MM format."


# only reason default exists is for the activity_end prompt to have a default value
def ask_time_question(
    prompt: str, skip_value: str | None = None, default: str | None = None
) -> str:
    """The helper function to ask questions requiring datetime in HH:MM.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str: The datetime value in HH:MM format.
    """
    if isinstance(skip_value, str) and _validate_time(skip_value):
        return skip_value

    time_value: str | None = questionary.text(
        prompt, validate=_validate_time, default=default if default else ""
    ).ask()

    if time_value is None:
        raise RequiredQuestionCancelledError("User cancelled the time question prompt.")

    # so 6:03 gets turned to 06:03
    time_value = datetime.strptime(time_value, "%H:%M").strftime("%H:%M")

    return time_value


def _validate_datetime(value: str) -> Literal[True] | str:
    """To be passed into questionary validate keyword to validate datetime questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """
    is_valid_datetime = validate_datetime(value)
    if not is_valid_datetime:
        return "Please enter a valid time in HH:MM format."
    return True


def ask_datetime_question(prompt: str, skip_value: str | None) -> str:
    if isinstance(skip_value, str) and _validate_datetime(skip_value) is True:
        return skip_value

    datetime_value: str | None = questionary.text(
        prompt,
        validate=_validate_datetime,
    ).ask()

    if datetime_value is None:
        raise RequiredQuestionCancelledError(
            "User cancelled the datetime question prompt."
        )

    return normalize_datetime(datetime_value)


def ask_activity_category(
    prompt: str,
    valid_activity_categories: Iterable[str] | None = None,
    skip_value: str | None = None,
) -> str:
    """The helper function to ask questions about the category of an activity.

    Args:
        prompt (str): The questionary prompt.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str: The category of the activity
    """

    def validate_categories(text: str) -> Literal[True] | str:
        if not text.strip():
            return "Category field may not be empty."

        if valid_activity_categories is None:
            return True

        return (
            True
            if text in valid_activity_categories
            else "This is not a valid category."
        )

    if isinstance(skip_value, str) and skip_value.strip():
        # shouldnt even reach inside this if condition
        # cuz the cli.py should already raise a typer.BadParameter error
        # if activity_input aka skip_value isn't valid
        # but its good to have i guess
        if (
            valid_activity_categories is not None
            and skip_value not in valid_activity_categories
        ):
            raise ValueError(f"Invalid activity category: {skip_value!s}")
        return skip_value

    activity_category: str | None = questionary.text(
        prompt, validate=validate_categories
    ).ask()

    if activity_category is None:
        raise RequiredQuestionCancelledError(
            "The activity category prompt is cancelled."
        )

    return activity_category


def ask_activity_description(prompt: str, skip_value: str | None = None) -> str | None:
    """The helper function to ask questions about the description of an activity.

    Args:
        prompt (str): The questionary prompt.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str | None: The description of an activity.
    """
    if skip_value:
        return skip_value

    activity_description: str | None = questionary.text(
        prompt,
    ).ask()

    return activity_description


def ask_for_confirmation(prompt: str, skip_value: bool | None = None) -> bool:
    if skip_value:
        return True
    return questionary.confirm(prompt, default=False).ask() or False
