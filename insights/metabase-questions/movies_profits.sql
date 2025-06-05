SELECT *,
(revenue - budget) AS profit
FROM movies
WHERE budget > 0
AND revenue > 0;
