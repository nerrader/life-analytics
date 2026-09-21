GUIDE = """\n
# Life Tracker Guide

## USING COMMAND OPTIONS

Command options let you provide values directly instead of entering them
through interactive prompts. This can make data entry faster and allows
commands to be used in scripts or automation.

The easiest way to see the available options for a command is with `--help`:

```bash
life activity --help
```

## EDITING RECORDS

The `--edit` option lets you modify an existing record.

Editing does not currently have an interactive mode. You must provide the
values you want to change using command options.

For example, to change the mood of a daily summary:

```bash
life summary --edit 2026-08-23 --mood 3
```

For activity and sleep records, use the record's ID instead:

```bash
life sleep --edit 3 -s 21:00
```

You can also update multiple values at once:

```bash
life activity --edit 5 --category SOCIAL -eb 2 --energy-after 5
```

Only the values you provide will be updated.

## CONFIGURATION

Use `life config list` to view your current configuration:

```bash
life config list
```

database_path:         Location of the database file.\n
activity_start_path:   Location of the file used to track activity.\n
force_detailed_mode:   Enabled --detailed on every activity or sleep command.\n
valid_categories:      Categories available when recording actvities. Manage these with `life config category`.

Configuration values can be changed with:

```bash
life config set <name> <value>
```

For example:

```bash
life config set force_detailed_mode true
```

Use `life config --help` for more information about configuration commands.

## THE --detailed FLAG

Most of the time, you don't need `--detailed`.

- The activity command normally assumes that the start and end times are on
the same date.
- The sleep command normally assumes that the start time was
yesterday and the end time is today.

This works most times, but sometimes you need to specify different
dates. That's where `--detailed` comes in.

It requires you to provide the full datetime for both the start and end times:

    YYYY-MM-DD HH:MM

This is a little more inconvenient, but gives you full control over the
datetimes when dealing with those weird edge cases.

## FOR MORE HELP

Every command has its own help menu:

```bash
life activity --help
life sleep --help
life summary --help
life config --help
```

Use it, its incredibly helpful for knowing more about the specifics.\n
"""
