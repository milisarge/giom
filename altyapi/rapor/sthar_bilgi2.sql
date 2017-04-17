set @dbakiye := 0;
select date(t.tarih) as tarih,t.fi�no,round(t.kdvsizbf,3) as nf,round(t.kdvlibf,3) as bf ,round(t.giris,2) as giri�,round(t.cikis,2) as ��k��,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.hareket_tipi from(
select tarih as tarih,fisno as fi�no,nf as kdvsizbf,bf as kdvlibf , miktar,
case when (ftip='C' and hedef=28) or (ftip='G' and hedef=28)  then miktar else 0 end as giris,
case when ftip='C' and kaynak=28  or (ftip='G' and kaynak=28)  then miktar else 0 end as cikis,
(case 
when ftip='C' and kaynak=28 then concat(hedef," sat��")
when ftip='G' and kaynak=28 then concat(hedef," kar�� al�m")
when ftip='G' and hedef=28 then concat(kaynak," al�m")
when ftip='C' and hedef=28 then concat(kaynak," kar�� sat��")
end
) as hareket_tipi
from sthar where  hedef=28 or kaynak=28
order by inckeyno
)as t;