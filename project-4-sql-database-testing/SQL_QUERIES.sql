-- Project 4 — SQL & Database Testing

-- TC-SQL-001
SELECT * FROM movies;

-- TC-SQL-002 (result not independently verified)
SELECT title, year FROM movies;

-- TC-SQL-003
SELECT * FROM movies WHERE title = 'Toy Story';

-- TC-SQL-004
SELECT * FROM movies WHERE year > 2010;

-- TC-SQL-005
SELECT * FROM movies WHERE director = 'John Lasseter';

-- TC-SQL-006
SELECT * FROM movies WHERE length_minutes > 100;

-- TC-SQL-007
SELECT * FROM movies
WHERE year > 2005 AND length_minutes > 110;

-- TC-SQL-008
SELECT * FROM movies
WHERE director = 'John Lasseter' OR director = 'Brad Bird';

-- TC-SQL-009
SELECT * FROM movies WHERE year BETWEEN 2000 AND 2010;

-- TC-SQL-010
SELECT * FROM movies ORDER BY year DESC;

-- TC-SQL-011
SELECT COUNT(*) FROM movies;

-- TC-SQL-012
SELECT director, COUNT(*) FROM movies GROUP BY director;

-- TC-SQL-013
SELECT movies.title, boxoffice.rating
FROM movies
JOIN boxoffice ON movies.id = boxoffice.movie_id;

-- TC-SQL-014
SELECT movies.title, boxoffice.domestic_sales
FROM movies
JOIN boxoffice ON movies.id = boxoffice.movie_id;

-- TC-SQL-015
SELECT * FROM employees WHERE building IS NULL;

-- TC-SQL-016
SELECT * FROM employees WHERE building IS NOT NULL;
