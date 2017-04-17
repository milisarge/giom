SELECT sum (ROUND( SUM( B.MIKTAR ) * B.BF, 2 ))
FROM sthar AS B
INNER JOIN tblstsabit AS A ON A.STOK_KODU = B.STOK_KODU
WHERE KAYNAK = '@subekod@'
 ftip='C'
AND TARIH >= '@bastarih@' + interval 1 day
AND TARIH <= '@sontarih@'
GROUP BY A.STOK_KODU
