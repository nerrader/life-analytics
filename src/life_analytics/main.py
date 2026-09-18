# nuitka-project: --company-name=Nerrader
# nuitka-project: --product-name=life_analytics
# nuitka-project: --output-filename=life
# nuitka-project: --product-version=2.0.0
# nuitka-project: --python-flag=no_docstrings
# nuitka-project: --python-flag=no_site

from life_analytics.cli import app


def main() -> None:
    app()


if __name__ == "__main__":
    main()
