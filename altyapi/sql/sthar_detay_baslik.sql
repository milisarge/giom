select DATE_FORMAT(tarih, '%d-%m-%Y') as tarih,fno as fiþno,round(khtutar,2) as kdvsiz_tutar,round(kdvtoplam,2) as kdv,
round(kdv1top,2) as kdv1,
round(kdv8top,3) as kdv8,
round(kdv18top,2) as kdv18,
round(geneltoplam,2) as tutar,round(kdtutar,2) as kdvli_tutar,date(vade_tarihi) as vade_tarihi,aciklama,
kaynak,(select cari_isim from tblcasabit where cari_kod=kaynak) as kaynak,
hedef,(select cari_isim from tblcasabit where cari_kod=hedef) as hedef,inckeyno as fkodstk
from fatura 
where inckeyno='@fkod@'