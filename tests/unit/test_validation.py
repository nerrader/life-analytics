from life_analytics.domain import validation


def test_valid_rating() -> None:
    assert validation.is_valid_rating(100.0) is False
    assert validation.is_valid_rating(0) is False
    assert validation.is_valid_rating(1) is True
    assert validation.is_valid_rating(4.9992) is True


def test_valid_time() -> None:
    assert validation.is_valid_time("24:01") is False
    assert validation.is_valid_time("23:60") is False
    assert validation.is_valid_time("17.32") is False
    assert validation.is_valid_time("17:32") is True
    assert validation.is_valid_time("23:59") is True
    assert validation.is_valid_time("00:00") is True


def test_valid_category() -> None:
    assert validation.is_valid_category("MAINT", {"MAINT", "IDLE", "SCHOOL"}) is True
    assert validation.is_valid_category("MAINT", None) is True
    assert validation.is_valid_category("jadksf", None) is True
    assert validation.is_valid_category("jadksf", {"MAINT", "IDLE", "SCHOOL"}) is False
    assert validation.is_valid_category("maint", {"MAINT", "IDLE", "SCHOOL"}) is False


def test_valid_datetime() -> None:
    assert validation.is_valid_datetime("2026-05-09 19:50") is True
    assert validation.is_valid_datetime("2026-05-09 00:00") is True
    assert validation.is_valid_datetime("2026-05-09 23:59") is True
    assert validation.is_valid_datetime("2024-02-29 12:30") is True
    assert validation.is_valid_datetime("2000-02-29 12:30") is True
    assert validation.is_valid_datetime("2026-05-09") is False
    assert validation.is_valid_datetime("19:50") is False
    assert validation.is_valid_datetime("") is False
