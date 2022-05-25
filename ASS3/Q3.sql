SELECT Y.citationpaper_id_2 as paper_X,X.paper_id_1 as paper_Z
FROM mydb.citation as X
INNER JOIN mydb.citation as Y
ON X.citationpaper_id_2 = Y.paper_id_1