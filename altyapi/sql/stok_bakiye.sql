set @dbakiye := 0;
set @iscari := '@merkez@';
set @stkod := '@stokod@';
select 
round(sum(giris-cikis),2) as bakiye from(
select 
case when (ftip='C' and hedef=@iscari) or (ftip='G' and kaynak=@iscari)  then miktar else 0 end as giris,
case when ftip='C' and kaynak=@iscari  or (ftip='G' and hedef=@iscari)  then miktar else 0 end as cikis
from sthar where  stok_kodu=@stkod and (hedef=@iscari or kaynak=@iscari) and tarih<='@tarih@'
)as t;