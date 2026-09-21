from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from life_analytics import config
from life_analytics.cli.app import app
from life_analytics.domain import constants as const

runner = CliRunner()


def setup_config(tmp_path: Path, mocker: MockerFixture) -> Path:
    config_path = tmp_path / "config.json"
    mocker.patch.object(const, "CONFIG_PATH", config_path)

    config.save_configs(config_path, config.Config())
    return config_path


def test_config_set_database_path(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)
    database_path = tmp_path / "test.db"

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "database_path",
            str(database_path),
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.database_path == database_path


def test_config_set_activity_start_path(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)
    activity_start_path = tmp_path / "activity.txt"

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "activity_start_path",
            str(activity_start_path),
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.activity_start_path == activity_start_path


def test_config_set_force_detailed_mode_valid_boolean_values(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "force_detailed_mode",
            "true",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.force_detailed_mode is True

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "force_detailed_mode",
            "false",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.force_detailed_mode is False


def test_config_set_force_detailed_mode_invalid_value(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    setup_config(tmp_path, mocker)

    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "force_detailed_mode",
            "maybe",
        ],
    )

    assert result.exit_code == 0
    display_error_mock.assert_called_once()


def test_config_set_invalid_config_name(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    setup_config(tmp_path, mocker)
    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "does_not_exist",
            "value",
        ],
    )

    assert result.exit_code == 0
    display_error_mock.assert_called_once()


def test_config_set_valid_categories_is_not_allowed(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    setup_config(tmp_path, mocker)
    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    result = runner.invoke(
        app,
        [
            "config",
            "set",
            "valid_categories",
            "programming",
        ],
    )

    assert result.exit_code == 0
    display_error_mock.assert_called_once()


def test_config_list_alias_ls(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    setup_config(tmp_path, mocker)

    result = runner.invoke(
        app,
        ["config", "ls"],
    )

    assert result.exit_code == 0
    assert "database_path" in result.stdout


def test_config_defaults_with_confirmation(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)
    confirmation_mock = mocker.patch("life_analytics.cli.prompts.ask_for_confirmation")

    configuration = config.Config(
        database_path=tmp_path / "custom.db",
        activity_start_path=tmp_path / "custom.txt",
        force_detailed_mode=True,
        _valid_categories={"programming", "exercise"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        ["config", "defaults"],
    )

    assert result.exit_code == 0
    confirmation_mock.assert_called_once()

    saved_config = config.load_configs(config_path)

    assert saved_config == config.Config()


def test_config_defaults_with_skip(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    configuration = config.Config(
        database_path=tmp_path / "custom.db",
        force_detailed_mode=True,
        _valid_categories={"programming"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        [
            "config",
            "defaults",
            "--skip",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config == config.Config()


def test_category_add_multiple(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "add",
            "programming",
        ],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "add",
            "exercise",
        ],
    )
    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories == {
        "programming",
        "exercise",
    }


def test_category_add_duplicate(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    runner.invoke(
        app,
        [
            "config",
            "category",
            "add",
            "programming",
        ],
    )

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "add",
            "programming",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories == {"programming"}


def test_category_delete(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    configuration = config.Config(
        _valid_categories={"programming", "exercise"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "delete",
            "programming",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories == {"exercise"}


def test_category_delete_last_category(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    configuration = config.Config(
        _valid_categories={"programming"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "delete",
            "programming",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories == set()


def test_category_delete_when_no_categories(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)
    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "delete",
            "programming",
        ],
    )

    assert result.exit_code == 0
    display_error_mock.assert_called_once()

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories is None


def test_category_delete_missing_category(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)
    display_error_mock = mocker.patch("life_analytics.cli.display.display_error")

    configuration = config.Config(
        _valid_categories={"programming"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "delete",
            "exercise",
        ],
    )

    assert result.exit_code == 0
    display_error_mock.assert_called_once()

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories == {"programming"}


def test_category_delete_aliases(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    for alias in ("remove", "delete", "del", "rm"):
        configuration = config.Config(
            _valid_categories={"programming"},
        )
        config.save_configs(config_path, configuration)

        result = runner.invoke(
            app,
            [
                "config",
                "category",
                alias,
                "programming",
            ],
        )

        assert result.exit_code == 0

        saved_config = config.load_configs(config_path)

        assert saved_config.valid_categories == set()


def test_category_clear_with_confirmation(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    confirmation_mock = mocker.patch("life_analytics.cli.prompts.ask_for_confirmation")
    configuration = config.Config(
        _valid_categories={"programming", "exercise"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "clear",
        ],
    )

    assert result.exit_code == 0
    confirmation_mock.assert_called_once()

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories is None


def test_category_clear_with_skip(
    tmp_path: Path,
    mocker: MockerFixture,
) -> None:
    config_path = setup_config(tmp_path, mocker)

    configuration = config.Config(
        _valid_categories={"programming", "exercise"},
    )
    config.save_configs(config_path, configuration)

    result = runner.invoke(
        app,
        [
            "config",
            "category",
            "clear",
            "--skip",
        ],
    )

    assert result.exit_code == 0

    saved_config = config.load_configs(config_path)

    assert saved_config.valid_categories is None
