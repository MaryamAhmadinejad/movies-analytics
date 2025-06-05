SELECT genres.title,
AVG(movies.vote_average) AS score
FROM genre_movie
INNER JOIN genres ON genres.id = genre_movie.genre_id
INNER JOIN movies ON movies.id = genre_movie.movie_id
GROUP BY genres.title
ORDER BY score DESC
LIMIT 10;
