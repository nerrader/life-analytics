# Life Analytics Project

This is a simple personal data analytics project I made to observe and track my
own daily life, which includes:

- my activities
- sleep duration
- sleep quality
- mood
- productivity
- stress
- and more!

My goal with this project is to learn at least a little bit more about myself by
discovering patterns in my daily life, and using data to improve my overall
decision making and quality of life.

## Features

- Local data storage, which you can use to analyze data yourself.
- Tracking daily summaries, activities, and sleep.
- Displaying all-time daily summaries, activities and sleep in a table.

## Upcoming Features

- `undo` and `redo` commands to reverse mistakes
- To make activity entry more convenient: `start` and `stop` commands.
- Make listing UX better, by adding extra commands like `recent`, and `today`
- GUI version of this tool.

## How to Install

pass

## How to use

For more information about the life tracker's CLI commands, use the `--help` menu.

```bash
life activity --help
```

> [!TIP]
> You can rename the `.exe` file to rename the master command.
> As an example, you can rename `life.exe` into `lf.exe` to make it easier to
> type in.
>
> So instead of `life stats`, its `lf stats`.
> Though for the examples, I will be using `life` as the master command.

### Using Command Options

Command options allow you to provide values directly instead of entering them
through interactive mode prompts. This can make data entry faster, and also
allows commands to be automated or scripted.

You also need to use command options/flags for editing, which we will cover
in the next section.

Again, the easiest way to see the available options/flags for each command
is to use its `--help` flag.

### Editing Records

The `--edit` option is used to edit records through their respective commands.

> [!IMPORTANT]
> Editing currently does not have an interactive mode, so you'll need to provide
> the values using command flags.

For example, I overestimated my mood on 2026-08-23 daily summary record,
I think my mood then was neutral and didn't deserve the high number I gave it, so:

```bash
life summary --edit 2026-08-23 --mood 3
```

For `life activity` and `life sleep`, you instead pass in the ID for `--edit`.

```bash
life sleep --edit 3 -ss 21:00
```

You can also pass in multiple values to update, like this:

```bash
life activity --edit 5 --category SOCIAL --energy-before 2 --energy-after 5
```

## Contributing

In this project, contributions are welcome, and whether you are fixing a bug,
adding a new feature, or just improving the documentation of this project,
you can get started by just following these steps:

1. Fork this repository

1. Clone this repository on your computer

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

1. Run `uv run pre-commit install` to initialize all the pre-commit hooks.

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

## Tech Stack

### Regular Dependencies

- Python
- SQLite
- SQL (to actually write the queries)
- typer (for the CLI)
- questionary (for the CLI prompting)
- rich (for the CLI styling)

### Dev Dependencies

- uv
- ruff
- mypy
- platformdirs
- pytest
- pytest-mock
- pre-commit
- vermin
