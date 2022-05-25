SELECT c.citationpaper_id_2 as paper,c.paper_id_1 as cited_by, k.t  as title,k.v as venue,k.y as year_of_pub,k.a as authors,k.ab as abstract
FROM (mydb.citation as c INNER JOIN
(SELECT s.paper_id as l,s.paper_title as t ,s.name as v, s.year_of_publication as y,b.author_list as a,s.abstract as ab 
 FROM (mydb.research_paper as s
INNER JOIN (SELECT X.paper_id as g, string_agg(X.author_name, ', ') AS author_list
FROM  mydb.authored_by as X
GROUP  BY 1) as b
ON b.g = s.paper_id
	  )) as k
ON c.paper_id_1 = k.l
	 ) 
ORDER BY paper