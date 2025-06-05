SELECT title,
release_year,
profit
FROM {{#72-movies-profits}}
ORDER BY profit
LIMIT 10;
