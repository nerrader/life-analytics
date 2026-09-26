SELECT
    sleep.quality,
    AVG(summary.mood),
    AVG(summary.productivity),
    AVG(summary.stress),
    COUNT(*) as n
FROM
    sleep
    JOIN daily_summaries as summary
    ON DATE(sleep.end_at) = summary.summary_date
GROUP BY sleep.quality
ORDER BY sleep.quality ASC;
