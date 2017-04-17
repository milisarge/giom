select fno as fiþno,ftip,islem_turu,DATE_FORMAT(tarih, '%d-%m-%Y') as tarih,DATE_FORMAT(vade_tarihi, '%d-%m-%Y') as vade_tarih,
aciklama,kaynak,hedef,takipkod,geneltoplam,med,irs,khtutar,kdtutar,
kdv1top,kdv8top,kdv18top,kdvtoplam,fatkalem_adedi,cari_tip,islem_turu,kdvdurum,toplam_mik,kdvdurum,inckeyno
from fatura 
where inckeyno='@fkod@'