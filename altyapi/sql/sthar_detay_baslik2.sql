select DATE_FORMAT(tarih, '%d-%m-%Y') as tarih,fno as fiþno,round(kdtutar,3) as toplam_tutar,
(select cari_isim from tblcasabit where cari_kod=kaynak) as kaynak,
(select cari_isim from tblcasabit where cari_kod=hedef) as hedef
from fatura 
where inckeyno='@fkod@'