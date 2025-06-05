SELECT release_year,
SUM(budget) AS total_budget
FROM movies
GROUP BY release_year;
