SELECT citationpaper_id_2 AS cited_paper, COUNT(citationpaper_id_2) AS count_citation
FROM mydb.citation
GROUP BY citationpaper_id_2
ORDER BY COUNT(citationpaper_id_2) DESC
LIMIT 20