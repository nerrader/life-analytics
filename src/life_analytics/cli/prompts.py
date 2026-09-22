from collections.abc import Iterable
from datetime import datetime
from typing import Literal

import questionary

from life_analytics.domain import validation
from life_analytics.domain.errors import ErrorDiagnostic, RequiredQuestionCancelledError
from life_analytics.utils.time_utils import datetime_string_to_iso


def ask_rating_question(prompt: str) -> float:
    def validate_rating(value: str) -> Literal[True] | str:
        """To be passed into questionary validate keyword to validate rating questions.

        Args:
            value (str): The variable/value to be validated.

        Returns:
            bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
        """
        if not value.strip():
            return "Rating cannot be empty"

        try:
            is_valid_rating = validation.is_valid_rating(float(value))
        except ValueError:
            is_valid_rating = False

        return (
            True if is_valid_rating is True else "Please enter a value between 1 and 5."
        )

    """The helper function to ask questions requiring rating in 1-5.

    Args:
        prompt_var_name (str): The name of the variable to be prompted for.

    Returns:
        float: The rating value between 1 and 10.
    """
    rating: float | None = questionary.text(
        prompt,
        validate=validate_rating,
    ).ask()

    if rating is None:
        raise RequiredQuestionCancelledError(
            ErrorDiagnostic(
                message="rating prompt was cancelled",
                description="required questions must be completed to add a record to the database.",
            )
        )

    return rating


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

    def validate_time(value: str) -> Literal[True] | str:
        """To be passed into questionary validate keyword to validate datetime questions.

        Args:
            value (str): The variable/value to be validated.

        Returns:
            bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
        """
        is_valid_time = validation.is_valid_time(value)
        return (
            True
            if is_valid_time is True
            else "Please enter a valid time in HH:MM format."
        )

    if isinstance(skip_value, str) and validation.is_valid_time(skip_value) is True:
        return skip_value

    time_value: str | None = questionary.text(
        prompt, validate=validate_time, default=default if default else ""
    ).ask()

    if time_value is None:
        raise RequiredQuestionCancelledError(
            ErrorDiagnostic(
                message="time prompt was cancelled",
                description="required questions must be completed to add a record to the database.",
            )
        )

    # so 6:03 gets turned to 06:03
    time_value = datetime.strptime(time_value, "%H:%M").strftime("%H:%M")

    return time_value


def ask_datetime_question(prompt: str, skip_value: str | None) -> str:
    def validate_datetime(value: str) -> Literal[True] | str:
        """To be passed into questionary validate keyword to validate datetime questions.

        Args:
            value (str): The variable/value to be validated.

        Returns:
            bool | str: Returns True if the value is valid, otherwise returns a string with an error message.
        """
        is_valid_datetime = validation.is_valid_datetime(value)
        if not is_valid_datetime:
            return "Please enter a valid time in HH:MM format."
        return True

    if isinstance(skip_value, str) and validation.is_valid_datetime(skip_value) is True:
        return skip_value

    datetime_value: str | None = questionary.text(
        prompt,
        validate=validate_datetime,
    ).ask()

    if datetime_value is None:
        raise RequiredQuestionCancelledError(
            ErrorDiagnostic(
                message="the datetime prompt was cancelled.",
                description="required questions must be completed to add a record to the database.",
            )
        )

    return datetime_string_to_iso(datetime_value)


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
            ErrorDiagnostic(
                message="the activity category prompt was cancelled.",
                description="required questions must be completed to add a record to the database.",
            )
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
