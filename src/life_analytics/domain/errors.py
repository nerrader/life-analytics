from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorDiagnostic:
    message: str
    description: str | None = None
    help: str | None = None


class RequiredQuestionCancelledError(Exception):
    """This error is raised when a required question, like activity category gets cancelled."""

    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class InvalidForceDetailModeConfigError(Exception):
    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class ValidCategoriesNotSettableError(Exception):
    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class InvalidConfigNameError(Exception):
    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class InvalidForceDetailModeConfig(Exception):
    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class NoCategoriesError(Exception):
    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class CategoryNotFoundError(Exception):
    """This error is raised when no categories are found."""

    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class NoUpdateFieldsError(Exception):
    """This error is raised when no valid fields are found."""

    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


class NoUpdateRecordsError(Exception):
    """This error is raised when no valid fields are found."""

    def __init__(self, diagnostic: ErrorDiagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic
