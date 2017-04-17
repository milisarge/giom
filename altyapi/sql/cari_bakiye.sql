select * from (
select hedef as kod,c.cari_isim as cari_isim,
sum(case when ftip='G' then round(geneltoplam,2) else (-1*round(geneltoplam,2)) end) as topborc
from fatura as f 
inner join tblcasabit as c on f.hedef=c.cari_kod
inner join tblcasabit as cx on f.kaynak=cx.cari_kod
where cx.grup_kodu='@kaynak@' AND c.cari_kod='@hedef@'
group by hedef ORDER BY vgborc DESC,topborc desc ) as t