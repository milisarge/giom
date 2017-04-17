SELECT round(sum(geneltoplam),2)
FROM fatura as f
inner join tblcasabit as c
on c.cari_kod=f.kaynak
WHERE c.grup_kodu = '@mkod@'
and ftip='G'
AND hedef = '@subekod@'
AND tarih
BETWEEN '@bastarih@'
AND '@sontarih@'