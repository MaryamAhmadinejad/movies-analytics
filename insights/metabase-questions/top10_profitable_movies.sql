SELECT title,
release_year,
profit
FROM {{#72-movies-profits}}
ORDER BY profit DESC
LIMIT 10;
