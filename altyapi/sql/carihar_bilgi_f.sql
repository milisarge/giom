set @dbakiye := 0;
select date(t.tarih) as tarih,t.fiþno,t.hareket_tipi,t.aciklama,round(t.giris,2) as giriþ,round(t.cikis,2) as çýkýþ,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.fkod from(
select tarih as tarih,fno as fiþno,geneltoplam as gt,vade_tarihi,aciklama,inckeyno as fkod,
case when (ftip='C' and hedef in ('@iscari@')) or (ftip='G' and kaynak in ('@iscari@')  )  then geneltoplam else 0 end as giris,
case when ftip='C' and kaynak in ('@iscari@')  or (ftip='G' and hedef in ('@iscari@') )  then geneltoplam else 0 end as cikis,
concat(b.tur,"(",cx.cari_isim,")") as hareket_tipi
from fatura as f inner join islem_turleri as b
on (f.ftip=b.gcmod and f.cari_tip=b.kcari and f.islem_turu=b.mcari) 
inner join tblcasabit as c
on c.cari_kod = f.kaynak
inner join tblcasabit as cx
on cx.cari_kod = f.hedef
where 
@fisno_kriter@
@tarih_kriter@
@islem_kriter@
@hartip_kriter@
@irs_kriter@
( (hedef in (@karsicari@) or kaynak in (@karsicari@)) and (kaynak in ('@iscari@') or hedef in ('@iscari@')) )
group by f.inckeyno,f.tarih,f.fno,f.geneltoplam,f.vade_tarihi,f.aciklama,f.ftip,f.hedef,f.kaynak,b.tur,c.cari_isim,cx.CARI_ISIM
order by tarih
)as t;

