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

- `undo` and `redo` commands to reverse mistakes
- Make listing UX better, by adding extra commands like `recent`, and `today`
- Add `--detailed` flag for sleep command to pass in your own sleep
start/end datetime, and sleep type.
- GUI version of this tool.

## How to Install

You must have Windows 10 or 11 to install this CLI tool:

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
