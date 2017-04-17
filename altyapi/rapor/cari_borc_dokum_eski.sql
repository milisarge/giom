select t.hedefkod,t.hedefad,sum(round(t.vgiris,2)-round(t.vcikis,2)) as vgborc,sum(round(t.giris,2)-round(t.cikis,2)) as borc
from(
select f.hedef as hedefkod,(select cari_isim from tblcasabit where cari_kod=f.hedef) as hedefad,
case when (ftip='C' and hedef in (@kaynak@)) or (ftip='G' and kaynak in (@kaynak@)  )  then geneltoplam else 0 end as giris,
case when (ftip='C' and kaynak in (@kaynak@))  or (ftip='G' and hedef in (@kaynak@) )  then geneltoplam else 0 end as cikis,
case when (ftip='C' and hedef in (@kaynak@) and vade_tarihi <='@vade_tarihi@') or (ftip='G' and kaynak in (@kaynak@)) and vade_tarihi <='@vade_tarihi@' then geneltoplam else 0 end as vgiris,
case when (ftip='C' and kaynak in (@kaynak@) and vade_tarihi <='@vade_tarihi@') or (ftip='G' and hedef in (@kaynak@))  and vade_tarihi <='@vade_tarihi@' then geneltoplam else 0 end as vcikis
from fatura as f inner join tblcasabit as c
on (c.cari_kod in (@kaynak@)) 
where 
(hedef in (select cari_kod from tblcasabit ) and kaynak in (@kaynak@))
group by f.inckeyno,f.hedef
)as t
group by t.hedefkod