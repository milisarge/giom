set @dbakiye := 0;
set @iscari := '@iscari@';
set @stkod := '@stkod@';
select DATE_FORMAT(t.tarih, '%d.%m.%Y')  as tarih,t.fi�no,t.hareket_tipi,round(t.kdvsizbf,3) as nf,round(t.kdvlibf,3) as bf ,round(t.giris,3) as giri�,round(t.cikis,3) as ��k��,
round((@dbakiye := @dbakiye + giris-cikis),2) as bakiye,t.aciklama as ack,t.inckeyno as sthkod from(
select tarih as tarih,fisno as fi�no,nf as kdvsizbf,bf as kdvlibf , miktar,
case when (ftip='C' and hedef=@iscari) or (ftip='G' and kaynak=@iscari)  then miktar else 0 end as giris,
case when ftip='C' and kaynak=@iscari  or (ftip='G' and hedef=@iscari)  then miktar else 0 end as cikis,
(case 
when ftip='C' and kaynak=@iscari then concat((select cari_isim from tblcasabit where cari_kod=hedef)," sat��")
when ftip='G' and hedef=@iscari then concat((select cari_isim from tblcasabit where cari_kod=kaynak)," sat��")
when ftip='G' and kaynak=@iscari then concat((select cari_isim from tblcasabit where cari_kod=hedef)," al�m")
when ftip='C' and hedef=@iscari then concat((select cari_isim from tblcasabit where cari_kod=kaynak)," al�m")
end
) as hareket_tipi,aciklama,inckeyno
from sthar where  stok_kodu=@stkod and (hedef=@iscari or kaynak=@iscari)
order by tarih
)as t;