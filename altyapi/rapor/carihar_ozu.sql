set @dbakiye := 0;
select date(t.tarih) as tarih,t.fi�no,date(t.vade_tarihi) as vade_tarihi,round(t.giris,2) as giri�,round(t.cikis,2) as ��k��,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.hareket_tipi,t.aciklama,t.fkod from(
select tarih as tarih,fno as fi�no,geneltoplam as gt,vade_tarihi,aciklama,islem_turu,inckeyno as fkod,
case when (ftip='C' and hedef in ('@iscari@')) or (ftip='G' and hedef in ('@iscari@')  )  then geneltoplam else 0 end as giris,
case when ftip='C' and kaynak in ('@iscari@')  or (ftip='G' and kaynak in ('@iscari@') )  then geneltoplam else 0 end as cikis,
(case 
when ftip='C' and kaynak in ('@iscari@') then concat((select cari_isim from tblcasabit where cari_kod=hedef),"@",hedef," ��k��")
when ftip='G' and kaynak in ('@iscari@') then concat((select cari_isim from tblcasabit where cari_kod=hedef),"@",hedef," kar�� giri�")
when ftip='G' and hedef in ('@iscari@')  then concat((select cari_isim from tblcasabit where cari_kod=kaynak),"@",kaynak," giri�")
when ftip='C' and hedef in ('@iscari@')  then concat((select cari_isim from tblcasabit where cari_kod=kaynak),"@",kaynak," kar�� ��k��")
end
) as hareket_tipi
from fatura as f inner join tblcasabit as c
on (c.cari_kod in ('@iscari@'))
where (kaynak in ('@iscari@') or hedef in ('@iscari@'))
group by f.inckeyno
order by tarih
)as t;