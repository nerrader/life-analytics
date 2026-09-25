# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Added success messages
- Improved the guide for the "USING COMMAND OPTIONS" section.
- Fixed a bug regarding `sleep --detailed` commands not producing a record.

## [2.0.1]

- Fixed bugs regarding `--detailed`.

## [2.0.0]

- Added `start` and `stop` commands.
- Added `--detailed` flag for `activity` and `sleep` commands.
- Added configs/settings using the `config` command.
- Added schema versioning, and an automatic schema migration system, including datetime normalization.
- Added `-ap` option for activity start/stop commands time stamp text path.
- Added powershell scripts to make the building process more painless and consistent.
- Made `sleep_type` modifiable in `--edit`
- Revamped the old `stats` command to display overall stats for collected data.
- Revamped the error messages to be more rust-like and helpful.
- Rename old `stats` command to `list`
- Removed unnecessary activity category schema constraint.

## [1.0.0]

This release adds the core features of the tracker.

- Stores tracking data locally on your computer, located at `%LOCALAPPDATA%/nerrader/life-analytics/life.db`.
- Daily summaries, activities and sleep tracking, and an interactive mode
to make data entry more straightforward.
- Record editing using `--edit` for the respective commands.
- `stats` command to display your all-time tracked data.
- `clear` command to clear all your data.
- A help menu accessible with `--help`.

[Unreleased]: https://github.com/nerrader/life-analytics/compare/v2.0.1...HEAD
[2.0.1]: https://github.com/nerrader/life-analytics/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/nerrader/life-analytics/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/nerrader/life-analytics/compare/c75a5e6...v1.0.0
