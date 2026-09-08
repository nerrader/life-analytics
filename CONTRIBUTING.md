# CONTRIBUTING

In this project, contributions are welcome, and whether you are fixing a bug,
adding a new feature, or just improving the documentation of this project,
you can get started by just following these steps:

1. Fork this repository

1. Clone that forked repository on your computer

    ```bash
    git clone https://github.com/[YOUR-USERNAME]/life-analytics.git
    ```

1. It is recommended that you make a separate branch instead of working on `main`.

    ```bash
    git switch -c [NEW-BRANCH-NAME]
    ```

    Branches should start with a branch prefix. Some examples include:
    - `feature/` for new features.
    - `fix/` to fix a known issue/bug.
    - `refactor/` to refactor a part of the codebase.

1. Use `uv sync` to automatically set up the virtual environment and grab all
the dependencies for you.

1. Run `uv run pre-commit install` and `uv run pre-commit install --hook-type commit-msg` to initialize all the pre-commit hooks in
the repository.

1. Commit your changes. Make sure your commit messages are clear and concise.

1. Push changes to your fork of the repository.

1. Open a pull request from your working branch to the `main` branch of the
original repository. Describe your changes and why they should be
implemented in the project, then submit.

> [!IMPORTANT]
> Please make sure your code works properly before submitting.
>
> - Follow PEP 8 guidelines
> - Make sure all tests pass
> - Make sure all pre-commit hooks pass, including mypy and ruff checks.
> - Maintain consistent styling
> - Include type annotations and documentation for any new functions.

By contributing to this project, you agree that your contribution will be
**licensed under the MIT License.**
