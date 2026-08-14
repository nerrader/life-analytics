from datetime import datetime
from typing import Literal, cast

import questionary

from life_analytics import constants as const


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
        raise RuntimeError("User skipped the rating question prompt.")

    return rating


def _validate_datetime(value: str) -> Literal[True] | str:
    """To be passed into questionary validate keyword to validate datetime questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """
    try:
        datetime.strptime(value, "%H:%M")  # noqa: DTZ007
        return True
    except ValueError:
        return "Please enter a valid time in HH:MM format."


def ask_datetime_question(prompt: str, skip_value: str | None = None) -> str:
    """The helper function to ask questions requiring datetime in HH:MM.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str: The datetime value in HH:MM format.
    """
    if isinstance(skip_value, str) and _validate_datetime(skip_value):
        return skip_value

    datetime_value: str | None = questionary.text(
        prompt,
        validate=_validate_datetime,
    ).ask()

    if datetime_value is None:
        raise RuntimeError("User cancelled the datetime question prompt.")

    return datetime_value


def ask_activity_category(
    prompt: str, skip_value: str | None = None
) -> const.ActivityCategory:
    """The helper function to ask questions about the category of an activity.

    Args:
        prompt (str): The questionary prompt.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str: The category of the activity
    """
    if skip_value in const.VALID_ACTIVITY_CATEGORIES:
        return cast(const.ActivityCategory, skip_value)

    activity_category: const.ActivityCategory | None = questionary.text(
        prompt,
        validate=lambda text: (
            True
            if text in const.VALID_ACTIVITY_CATEGORIES
            else "Please enter a valid activity category."
        ),
    ).ask()

    if activity_category is None:
        raise RuntimeError("The activity category prompt is cancelled.")

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
