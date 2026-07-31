BEGIN TRANSACTION;

DELETE FROM daily_summaries;
DELETE FROM activities;
DELETE FROM sleep;
DELETE FROM sqlite_sequence;

COMMIT;