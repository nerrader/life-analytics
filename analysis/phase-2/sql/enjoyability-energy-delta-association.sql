WITH energy_differences AS (
    SELECT
        enjoyability,
        (energy_after - energy_before) AS energy_delta,
        AVG(energy_after - energy_before)
            OVER (PARTITION BY enjoyability)
            AS avg_energy_delta,
        COUNT(*) OVER (PARTITION BY enjoyability) AS total_enjoyability_rows,
        ROW_NUMBER() OVER (
            PARTITION BY enjoyability
            ORDER BY (energy_after - energy_before)
        ) AS row_number
    FROM activities
)

SELECT
    enjoyability,
    ROUND(avg_energy_delta, 2) AS mean,
    MEDIAN(energy_delta) AS 'Median',
    MAX(
        CASE
            WHEN
                row_number = CEIL(total_enjoyability_rows * 0.25)
                THEN energy_delta
        END
    ) AS q1,
    MAX(
        CASE
            WHEN
                row_number = CEIL(total_enjoyability_rows * 0.75)
                THEN energy_delta
        END
    ) AS q3,
    (
        MAX(
            CASE
                WHEN
                    row_number = CEIL(total_enjoyability_rows * 0.75)
                    THEN energy_delta
            END
        )
        - MAX(
            CASE
                WHEN
                    row_number = CEIL(total_enjoyability_rows * 0.25)
                    THEN energy_delta
            END
        )
    ) AS iqr,
    ROUND(SQRT(AVG(POWER(energy_delta - avg_energy_delta, 2))), 2) AS sd,
    COUNT(*) AS n
FROM energy_differences
GROUP BY enjoyability
ORDER BY enjoyability DESC;
