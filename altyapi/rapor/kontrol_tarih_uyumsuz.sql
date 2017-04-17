SELECT *
FROM fatura AS a
INNER JOIN sthar AS b ON a.inckeyno = b.finckeyno
WHERE a.tarih <> b.tarih
GROUP BY a.inckeyno