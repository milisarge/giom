SELECT round(sum(geneltoplam),2)
FROM fatura
where ftip='C'
AND kaynak= '@subekod@'
AND tarih
BETWEEN '@bastarih@' + interval 1 day
AND '@sontarih@'