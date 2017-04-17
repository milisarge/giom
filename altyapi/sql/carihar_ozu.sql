set @dbakiye := 0;
select date(t.tarih) as tarih,t.fiþno,date(t.vade_tarihi) as vade_tarihi,round(t.giris,2) as giriþ,round(t.cikis,2) as çýkýþ,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.hareket_tipi,t.aciklama,t.fkod from(
select tarih as tarih,fno as fiþno,geneltoplam as gt,vade_tarihi,aciklama,islem_turu,inckeyno as fkod,
case when (ftip='C' and hedef in ('@iscari@')) or (ftip='G' and hedef in ('@iscari@')  )  then geneltoplam else 0 end as giris,
case when ftip='C' and kaynak in ('@iscari@')  or (ftip='G' and kaynak in ('@iscari@') )  then geneltoplam else 0 end as cikis,
(case 
when ftip='C' and kaynak in ('@iscari@') then concat((select cari_isim from tblcasabit where cari_kod=hedef),"@",hedef," çýkýþ")
when ftip='G' and kaynak in ('@iscari@') then concat((select cari_isim from tblcasabit where cari_kod=hedef),"@",hedef," karþý giriþ")
when ftip='G' and hedef in ('@iscari@')  then concat((select cari_isim from tblcasabit where cari_kod=kaynak),"@",kaynak," giriþ")
when ftip='C' and hedef in ('@iscari@')  then concat((select cari_isim from tblcasabit where cari_kod=kaynak),"@",kaynak," karþý çýkýþ")
end
) as hareket_tipi
from fatura as f inner join tblcasabit as c
on (c.cari_kod in ('@iscari@'))
where (kaynak in ('@iscari@') or hedef in ('@iscari@'))
group by f.inckeyno
order by tarih
)as t;