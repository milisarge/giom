set @dbakiye := 0;
select * from(
select date(t.tarih) as tarih,t.fiþno,t.hareket_tipi,t.aciklama,date(t.vade_tarihi) as vade_tarihi,round(t.giris,2) as borç,round(t.cikis,2) as alacak,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.fkod from(
select tarih as tarih,fno as fiþno,geneltoplam as gt,vade_tarihi,aciklama,inckeyno as fkod,
case when (ftip='C' and hedef in ('@iscari@')) or (ftip='G' and kaynak in ('@iscari@')  )  then geneltoplam else 0 end as giris,
case when ftip='C' and kaynak in ('@iscari@')  or (ftip='G' and hedef in ('@iscari@') )  then geneltoplam else 0 end as cikis,
concat(b.tur,"(",c.cari_isim,")") as hareket_tipi 
from fatura as f inner join islem_turleri as b
on (f.ftip=b.gcmod and f.cari_tip=b.kcari and f.islem_turu=b.mcari) 
inner join tblcasabit as c
on c.cari_kod = f.kaynak
inner join tblcasabit as cx
on cx.cari_kod = f.hedef
where 
@fisno_kriter@
@islem_kriter@
@hartip_kriter@
@irs_kriter@
( c.grup_kodu=@karsicari@ and (kaynak in ('@iscari@') or hedef in ('@iscari@')) )
group by f.inckeyno
order by tarih
)as t)as u
where
u.tarih between date_add((DATE_FORMAT(NOW() ,'%Y-%m-%d')),interval -(1+@chgun@) day) and now()

