set @iscari := '@iscari@';
set @stkod := '@stkod@';
select sum(round(t.giris,3)) as giriş,sum(round(t.cikis,3)) as çıkış,round((sum(giris)-sum(cikis)),2) as bakiye,
sum(round(t.giristut,3)) as giriş_tutar,sum(round(t.cikistut,3)) as çıkış_tutar,round((sum(giristut)-sum(cikistut)),2) as bakiye_tutar
from(
select 
stok_kodu,
case when (ftip='C' and hedef=@iscari) or (ftip='G' and kaynak=@iscari)  then miktar else 0 end as giris,
case when ftip='C' and kaynak=@iscari  or (ftip='G' and hedef=@iscari)  then miktar else 0 end as cikis,
case when (ftip='C' and hedef=@iscari) or (ftip='G' and kaynak=@iscari)  then miktar*bf else 0 end as giristut,
case when ftip='C' and kaynak=@iscari  or (ftip='G' and hedef=@iscari)  then miktar*bf else 0 end as cikistut
from sthar where  stok_kodu=@stkod and (hedef=@iscari or kaynak=@iscari)
)as t
group by t.stok_kodu