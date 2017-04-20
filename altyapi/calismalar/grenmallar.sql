SELECT A.STOK_KODU, A.STOK_ADI, SUM( B.MIKTAR ) , B.BF, ROUND( SUM( B.MIKTAR ) * B.BF, 2 )
FROM STHAR AS B
INNER JOIN TBLSTSABIT AS A ON A.STOK_KODU = B.STOK_KODU
WHERE KAYNAK = '28'
AND HEDEF = '09'
AND TARIH >= '2015-01-01'
AND TARIH <= '2015-01-31'
GROUP BY A.STOK_KODU