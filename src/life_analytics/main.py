from life_analytics import constants as const
from life_analytics.cli import app
from life_analytics.database import create_database


def main() -> None:
    if not const.LIFE_DATABASE_FILEPATH.exists():
        const.LIFE_DATABASE_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
        create_database(const.LIFE_DATABASE_FILEPATH)

    app()


if __name__ == "__main__":
    main()
