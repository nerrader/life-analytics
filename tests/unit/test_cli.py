from life_analytics import cli


def test_validate_datetime_with_valid_datetime() -> None:
    assert cli._validate_datetime("00:00") is True
    assert cli._validate_datetime("18:20") is True


def test_validate_datetime_with_invalid_datetime() -> None:
    assert isinstance(cli._validate_datetime("25:00"), str)
    assert isinstance(cli._validate_datetime("24:60"), str)
    assert isinstance(cli._validate_datetime("7 :59 "), str)


def test_validate_rating_with_valid_rating() -> None:
    assert cli._validate_rating("10") is True
    assert cli._validate_rating("1") is True
    assert cli._validate_rating("4") is True


def test_validate_rating_with_invalid_rating() -> None:
    assert isinstance(cli._validate_rating("11"), str)
    assert isinstance(cli._validate_rating("-1"), str)
    assert isinstance(cli._validate_rating("0"), str)
