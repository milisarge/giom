SELECT vade_tarihi AS vtrh, geneltoplam AS ftutar,aciklama
FROM fatura AS f
INNER JOIN tblcasabit AS c ON f.hedef = c.cari_kod
INNER JOIN tblcasabit AS cx ON f.kaynak = cx.cari_kod
WHERE cx.grup_kodu = 'merkez'
AND c.cari_tip = 'F'
AND c.rapor_kodu1 = 'takip'
AND f.tarih < now( )
and c.cari_kod='@carikod@'
and f.ftip='g'
and vade_tarihi between ('2015-01-01' ) and   (now() + interval 60 day )
GROUP BY inckeyno order by vade_tarihi