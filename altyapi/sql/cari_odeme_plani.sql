set @dbakiye :=0;
select * from(
SELECT t.gc,t.vtrh as vade_tarih,t.isim as cari_ismi,t.ftutar as vadeye_denk_gelen_tutar, 
round( (@dbakiye := @dbakiye + vgborc), 2 ) AS vadesi_gecen_toplam_tutar
FROM (
SELECT ftip as gc,c.cari_isim AS isim, vade_tarihi AS vtrh, geneltoplam AS ftutar, sum(
CASE WHEN vade_tarihi <= now()
AND ftip = 'G'
THEN round( geneltoplam, 2 )
ELSE CASE WHEN vade_tarihi <=now()
AND ftip = 'C'
THEN (
-1 * round( geneltoplam, 2 ) )
ELSE 0
END END
) AS vgborc
FROM fatura AS f
INNER JOIN tblcasabit AS c ON f.hedef = c.cari_kod
INNER JOIN tblcasabit AS cx ON f.kaynak = cx.cari_kod
WHERE cx.grup_kodu = 'merkez'
AND c.cari_tip = 'F'
AND c.rapor_kodu1 = 'takip'
AND f.tarih < now( )
GROUP BY inckeyno
) AS t
where t.vtrh< now() + interval 60 day )
as p
where p.gc='G' order by p.cari_ismi desc