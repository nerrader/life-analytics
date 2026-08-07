from datetime import datetime
from typing import TYPE_CHECKING

import questionary

if TYPE_CHECKING:
    from life_analytics.constants import Rating


def _validate_rating(value: str) -> bool | str:
    """To be passed into questionary validate keyword to validate rating questions.

    Args:
        value (str): The variable/value to be validated.

    Returns:
        bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
    """

    if value.isdigit() and 1 <= int(value) <= 10:
        return True
    return "Please enter a value between 1 and 10."


def ask_rating_question(prompt_var_name: str) -> Rating:
    """The helper function to ask questions requiring rating in 1-10.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.

    Returns:
        Rating: The rating value between 1 and 10.
    """
    rating = questionary.text(
        f"Where 5 is the average, Rate your {prompt_var_name} out of 10:",
        validate=_validate_rating,
    ).ask()

    return rating


def _validate_datetime(value: str) -> bool | str:
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


def ask_datetime_question(prompt_var_name: str, skip_value: str | None = None) -> str:
    """The helper function to ask questions requiring datetime in HH:MM.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str: The datetime value in HH:MM format.
    """
    if isinstance(skip_value, str) and skip_value.strip:
        return skip_value

    datetime_value = questionary.text(
        f"Please enter the {prompt_var_name} in HH:MM format:",
        validate=_validate_datetime,
    ).ask()

    return datetime_value


def ask_activity_name(prompt: str, skip_value: str | None = None) -> str:
    """The helper function to ask questions requiring datetime in HH:MM.

    Args:
        prompt (str): The questionary prompt.
        skip_value (str | None): If the provided value is valid, skip this question.

    Returns:
        str: The datetime value in HH:MM format.
    """
    if isinstance(skip_value, str) and skip_value.strip:
        return skip_value

    activity_name = questionary.text(
        prompt,
        validate=lambda text: (
            True if text.strip() else "Please enter a valid activity."
        ),
    ).ask()

    return activity_name


def ask_for_confirmation(prompt: str, skip_value: bool | None = None):
    if skip_value:
        return True
    return questionary.confirm(prompt, default=False).ask()
