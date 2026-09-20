# nuitka-project: --company-name=Nerrader
# nuitka-project: --product-name=life_analytics
# nuitka-project: --output-filename=life
# nuitka-project: --product-version=2.0.0
# nuitka-project: --python-flag=no_docstrings
# nuitka-project: --python-flag=no_site
from rich.console import Console

from life_analytics.cli import app
from life_analytics.domain.errors import RequiredQuestionCancelledError
from life_analytics.logic.display import display_error

console = Console()


def main() -> None:
    try:
        app()
    except RequiredQuestionCancelledError as error:
        display_error(error.diagnostic)


if __name__ == "__main__":
    main()
