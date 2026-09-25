SELECT
    category,
    AVG((energy_after - energy_before)) AS energy_delta,
    COUNT(*) AS count
FROM activities
GROUP BY category
HAVING count > 10 -- to remove the ones with low sample size
ORDER BY energy_delta DESC;
