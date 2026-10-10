# Second Phase Findings

This file will be focused on documenting my findings for the second phase, the EDA part of my life analysis.

## Category Energy Deltas

I decided to first investigate if different categories had varying energy deltas, and sure enough, while these were minor changes, there was.

| Category | Mean  | Median | Q1  | Q3 | IQR | SD   | n   |
|----------|-------|--------|-----|----|-----|------|-----|
| SPORTS   | 0.61  | 0.5    | 0   | 1  | 1   | 0.79 | 23  |
| MAINT    | 0.3   | 0.0    | 0   | 0.5| 0.5 | 0.56 | 141 |
| IDLE     | -0.03 | 0.0    | 0   | 0  | 0   | 0.5  | 108 |
| DEV      | -0.06 | 0.0    | 0   | 0  | 0   | 0.5  | 103 |
| SOCIAL   | -0.09 | 0.0    | 0   | 0  | 0   | 0.68 | 25  |
| SCHOOL   | -0.46 | 0.0    | -1  | 0  | 1   | 0.72 | 72  |

> Result produced by [sql/category-energy-deltas.sql](sql/category-energy-deltas.sql)

- `SPORTS` activities show the strongest energy delta, with `mean` = 0.61, `Q3` and `IQR` = 1.
- `MAINT` activities are mostly energy neutral, however leaning toward the positive side, as `Q3` = 0.5
- `IDLE`, `DEV`, and `SOCIAL` activities are usually energy neutral, with `IQR` = 0, though somewhat leaning towards the negative side.
- `SCHOOL` activities are usually neutral, as `Median` = 0, though sometimes it can be energy-draining, as `Q1` = -1

I find it interesting that `MAINT` activities show a stronger association of positive energy delta, while `IDLE` activities don't.

You would think that taking a break or resting would potentially increase energy later on, but apparently not?

And another observation is that the `SOCIAL` category apparently tends to decrease my energy, despite having a relatively high average enjoyability rate of 3.84/5.

> Average enjoyability rate produced by [sql/average-social-enjoyability](sql/average-social-enjoyability.sql)

These observations led to two new questions, that I will be adding in the unanswered questions list:

- Why are MAINT activities associated with a positive energy delta, while IDLE has a neutral change?
- Why are SOCIAL activities associated with a negative energy delta, despite having a high average enjoyability?

I also tried to investigate whether enjoyability and energy delta are typically associated with each other.

| Enjoyability | Mean  | Median | Q1   | Q3  | IQR | SD   | n   |
|--------------|-------|--------|------|-----|-----|------|-----|
| 5            | 0.72  | 0.5    | 0    | 1   | 1   | 0.79 | 18  |
| 4.5          | 0.28  | 0.0    | 0    | 0.5 | 0.5 | 0.89 | 23  |
| 4            | 0.25  | 0.0    | 0    | 1   | 1   | 0.77 | 97  |
| 3.5          | -0.02 | 0.0    | 0    | 0   | 0   | 0.62 | 93  |
| 3            | -0.1  | 0.0    | 0    | 0   | 0   | 0.49 | 213 |
| 2.5          | -0.23 | 0.0    | 0    | 0   | 0   | 0.42 | 13  |
| 2            | -0.36 | 0.0    | -0.5 | 0   | 0.5 | 0.46 | 25  |
| 1.5          | 0.0   | 0.0    | 0    | 0   | 0   | 0.0  | 1   |
| 1            | -1.0  | -1.0   | -2   | -1  | 1   | 0.71 | 4   |

Result produced by: [sql/enjoyability-energy-delta-association.sql](sql/enjoyability-energy-delta-association.sql)
The results show a positive association between enjoyability and energy delta.

- Activities that had an enjoyability rating of >=4 were associated with a positive energy delta, as `Q3` = 0.5 or 1.
- Activities that had an enjoyability rating of <= 2 are associated with a negative energy delta. With `Q1` = -0.5 or -2.
- However, activities in the middle were associated with a neutral energy delta, as `Median`, and `IQR` are both 0.

However, since the number of observations varies substantially between enjoyment levels, especially at the extremes, this should be considered an initial observation rather than a strong conclusion.

## Things about Sleep

First, I wanted to see if your sleep quality had anything to do with duration.

![A graph showing no correlation between sleep quality and sleep duration](assets/analysis-images/no-sleep-duration-quality-correlation.png)
Results produced by [sql/no-sleep-duration-quality-correlation.sql](sql/no-sleep-duration-quality-correlation.sql) and Tableau Public.

Yeah, no, there isn't.
At least not an obvious one, the points are pretty scattered, with no obvious trend. This doesn't prove that they aren't correlated, but there is just not enough evidence of a relationship so far.

I also decided to look at if sleep quality had anything to do with daily summary metrics (mood, productivity, stress)

| Quality | Avg Mood | Avg Productivity | Avg Stress | n |
| ---: | ---: | ---: | ---: | ---: |
| 1.5 | 2.50 | 3.00 | 1.00 | 1 |
| 2.0 | 3.50 | 2.25 | 1.00 | 2 |
| 2.5 | 3.50 | 4.25 | 1.00 | 1 |
| 3.0 | 3.25 | 3.20 | 1.60 | 10 |
| 3.5 | 2.93 | 3.64 | 1.86 | 7 |
| 4.0 | 3.31 | 4.13 | 1.81 | 8 |
| 4.5 | 4.17 | 3.50 | 1.00 | 3 |

Results produced by [sql/sleep-quality-summary-metrics-corr.sql](sql/sleep-quality-summary-metrics-corr.sql)
There are some potentially interesting patterns here, with mood and productivity somewhat increasing with the quality, except at 4.5 where productivity drops (though it only has n = 3, so take that with a grain of salt) while stress showing no pattern whatsoever.

Though this is more of an interesting observation rather than a conclusion, as the sample size (n) is way too small to draw strong conclusions.

I also wanted to take a look at sleep quality during the weekends.

| Day Type | Avg Sleep Quality | n |
| ---: | ---: | ---: |
| Weekday | 3.25 | 22 |
| Weekend | 3.70 | 10 |

Results produced by [sql/day-type-sleep-quality.sql](sql/day-type-sleep-quality.sql)
Unsurprisingly, weekends are associated with a higher sleep quality than weekdays.

| Day Type | Avg Mood | Avg Productivity | Avg Stress | n |
| --- | ---: | ---: | ---: | ---: |
| Weekday | 3.1364 | 3.3068 | 1.6591 | 22 |
| Weekend | 3.6111 | 4.0000 | 1.4444 | 9 |

And weekends are also associated with higher productivity and higher mood.

Though again, the sample size (n) is too small to draw strong conclusions, so please keep that in mind and take this with a grain of salt.

So another question I would add is:

- Are the observed differences from weekends and weekdays consistent enough to be investigated further?
- Is a higher sleep quality really associated with overall higher performance on daily summary metrics?
