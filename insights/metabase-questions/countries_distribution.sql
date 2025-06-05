SELECT origin_country,
COUNT(*) AS number_of_movies
FROM movies
GROUP BY origin_country
ORDER BY number_of_movies DESC;
