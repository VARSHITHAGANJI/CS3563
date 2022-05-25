SELECT * 
FROM(
SELECT r.A1||','||r.A2 as co_authors, count(*) as c
FROM(
SELECT a.paper_id as p_id, a.a1 as A1, a.a2 as A2
FROM (
SELECT X.paper_id as paper_id, X.author_name as a1, Y.author_name as a2
FROM mydb.authored_by as X
INNER JOIN mydb.authored_by as Y
ON X.paper_id = Y.paper_id AND X.author_name <> Y.author_name AND X.author_number < Y.author_number
) as a
ORDER BY p_id) as r
GROUP BY r.A1,r.A2) as co_authored
WHERE co_authored.c > 1