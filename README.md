# Life Analytics Project

This is a simple personal data analytics project, using the CLI I made to observe
and track my own daily life, which includes:

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

- Make `stats` command have a `--today` flag to analyze today's data.
- Add logging and `verbose_mode`
- GUI version of this tool.

## How to Install

You must have Windows 10 or 11 to install this CLI tool, any other OSes are not officially supported.

1. Find the latest release in the releases page of this GitHub repository
1. Download the .exe file.

## Adding the CLI to Path

This step is optional, but also **highly recommended**

If you want to run the CLI from any folder without having to navigate to the
directory containing the .exe, you should add its folder to your system's PATH.

> [!IMPORTANT]
> If you do not add the .exe location to your PATH, you will need to navigate to
> its folder before running the CLI, or provide the full path to the executable.

## Usage

For more information about the life tracker's CLI commands, use the `guide` command and the `--help` menu.

```bash
life guide
```

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
