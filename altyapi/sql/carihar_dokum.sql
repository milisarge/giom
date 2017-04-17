set @dbakiye := 0;
select date(t.tarih) as tarih,t.fiþno,DATE_FORMAT(t.vade_tarihi, '%d.%m.%Y') as vade_tarihi,round(t.giris,2) as borç,round(t.cikis,2) as alacak,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.hareket_tipi,t.aciklama,t.fkod from(
select tarih as tarih,fno as fiþno,geneltoplam as gt,vade_tarihi,aciklama,inckeyno as fkod,
case when (ftip='C' and hedef in ('@iscari@')) or (ftip='G' and kaynak in ('@iscari@')  )  then geneltoplam else 0 end as giris,
case when ftip='C' and kaynak in ('@iscari@')  or (ftip='G' and hedef in ('@iscari@') )  then geneltoplam else 0 end as cikis,
concat(b.tur,"(",kaynak,")") as hareket_tipi 
from fatura as f inner join islem_turleri as b
on (f.ftip=b.gcmod and f.cari_tip=b.kcari and f.islem_turu=b.mcari) 
inner join tblcasabit as c
on c.cari_kod = f.kaynak
where 
(tarih BETWEEN '@bastarih@' AND '@sontarih@')  and
( c.grup_kodu='@kaynak@' and (kaynak in ('@iscari@') or hedef in ('@iscari@')) )
group by f.inckeyno
order by tarih
)as t;

