# nuitka-project: --company-name=Nerrader
# nuitka-project: --product-name=life_analytics
# nuitka-project: --output-filename=life
# nuitka-project: --product-version=2.0.0
# nuitka-project: --python-flag=no_docstrings
# nuitka-project: --python-flag=no_site
from rich.console import Console

from life_analytics.cli import app
from life_analytics.domain.errors import RequiredQuestionCancelledError

console = Console()


def main() -> None:
    try:
        app()
    except RequiredQuestionCancelledError as error:
        console.print(f"ERROR: {error!s}", style="red")


if __name__ == "__main__":
    main()
