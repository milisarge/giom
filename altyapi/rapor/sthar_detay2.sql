select 
t.sira,
(case
when t.ack='' then
(select stok_adi from tblstsabit where stok_kodu=t.kod)
when t.ack<>'' then t.ack
end
)as isim,
round(t.miktar,3) as miktar,t.birim,round(t.kdvlibf,3) as fiyat ,
round(t.miktar*round(t.kdvlibf,8),3) as tutar,kdvoran as kdv from(
select aciklama as ack,stok_kodu as kod,sira as sira,olcubr as birim,fisno as fiþno,nf as kdvsizbf,bf as kdvlibf , miktar as miktar,kdvoran
from sthar where  finckeyno='@fkod@'
order by inckeyno
)as t;