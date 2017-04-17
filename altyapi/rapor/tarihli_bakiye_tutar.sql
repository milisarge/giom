set @iscari := '@subekod@';
select sum(btut) as devir_tutari from(
select t.kod,t.isim,
round(sum(giris-cikis),2) as bakiye,t.fiyat,round((sum(giris-cikis)*t.fiyat),2) as btut from(
select b.stok_kodu as kod,a.stok_adi as isim,bf as fiyat,
case when (ftip='C' and hedef=@iscari) or (ftip='G' and kaynak=@iscari)  then b.miktar else 0 end as giris,
case when ftip='C' and kaynak=@iscari  or (ftip='G' and hedef=@iscari)  then b.miktar else 0 end as cikis
from sthar as b
inner join tblstsabit as a on a.stok_kodu=b.stok_kodu 
where (hedef=@iscari or kaynak=@iscari) and tarih<='@bastarih@' 
)as t 
group by kod) as g