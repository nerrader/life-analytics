SELECT
    sleep.quality AS sleep_quality,
    AVG(summary.mood) AS mood,
    AVG(summary.productivity) AS productivity,
    AVG(summary.stress) AS stress,
    COUNT(*) AS n
FROM
    sleep
INNER JOIN daily_summaries AS summary
    ON DATE(sleep.end_at) = summary.summary_date
GROUP BY sleep.quality
ORDER BY sleep.quality ASC;
