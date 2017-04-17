SELECT *
FROM fatura AS a
INNER JOIN sthar AS b ON a.inckeyno = b.finckeyno
WHERE a.fno <> b.fisno
GROUP BY a.inckeyno