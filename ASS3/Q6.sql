SELECT  r.authors, count( r.authors )
FROM(
SELECT d.A||','||d.B||','||d.C as authors
FROM(
SELECT k.author_name AS A ,l.author_name AS B,m.author_name AS C
FROM
(SELECT j.p_id,j.y,j.c_id FROM
(SELECT X.paper_id_1 as p_id, X.citationpaper_id_2 as y,Y.citationpaper_id_2 as c_id
FROM mydb.citation as X
INNER JOIN mydb.citation as Y
ON X.citationpaper_id_2 = Y.paper_id_1 ) as j 
INNER JOIN mydb.citation as Z
ON j.c_id = Z.paper_id_1 AND j.p_id = Z.citationpaper_id_2) as T ,mydb.authored_by as k, mydb.authored_by as l,mydb.authored_by as m
WHERE T.p_id = k.paper_id AND T.y = l.paper_id AND T.c_id = m.paper_id) AS d
WHERE d.A <> d.B AND d.B <> d.C) as r
GROUP BY r.authors