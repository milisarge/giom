select t.sira,t.kod,
(case
when t.ack='' then
(select stok_adi from tblstsabit where stok_kodu=t.kod)
when t.ack<>'' then t.ack
end
)as isim,round(t.miktar,3) as miktar,t.birim,round(t.kdvsizbf,3) as nf,round(t.kdvlibf,3) as bf ,
round(t.miktar*round(t.kdvlibf,8),2) as tutar,kdvoran as kdv from(
select sira,aciklama as ack,stok_kodu as kod,olcubr as birim,fisno as fiþno,nf as kdvsizbf,bf as kdvlibf , miktar as miktar,kdvoran
from sthar where  finckeyno='@fkod@'
order by sira
)as t;