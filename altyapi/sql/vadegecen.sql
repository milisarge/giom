SELECT * FROM
(select CS.CARI_KOD,cs.cari_isim,
SUM(ch.BORC)-SUM(ch.alacak) AS BAKIYE  from tblcahar as ch inner join tblcasabit 
as cs on cs.cari_kod=ch.cari_kod 
where cs.grup_kodu like 'TAKIP' and cs.cari_kod='@carikod' AND VADE_TARIHI < '@tarih' GROUP BY CS.CARI_ISIM,CS.CARI_KOD )AS D 
WHERE D.BAKIYE<0 