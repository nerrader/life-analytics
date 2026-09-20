# nuitka-project: --company-name=Nerrader
# nuitka-project: --product-name=life_analytics
# nuitka-project: --output-filename=life
# nuitka-project: --product-version=2.0.0
# nuitka-project: --python-flag=no_docstrings
# nuitka-project: --python-flag=no_site
from life_analytics.cli.app import app
from life_analytics.cli.display import display_error
from life_analytics.domain.errors import RequiredQuestionCancelledError


def main() -> None:
    try:
        app()
    except RequiredQuestionCancelledError as error:
        display_error(error.diagnostic)


if __name__ == "__main__":
    main()
