SELECT a.stok_kodu, stok_adi, sum( b.miktar )
FROM sthar AS b
INNER JOIN tblstsabit AS a ON a.stok_kodu = b.stok_kodu
WHERE hedef = '12'
AND tarih between '2015-01-05' and '2015-01-11'
GROUP BY stok_kodu