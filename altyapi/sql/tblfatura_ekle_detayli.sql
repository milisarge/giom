insert into fatura
(kaynak,ftip,fno,hedef,tarih,khtutar,kdtutar,sat_iskt_top,mfaz_iskt_top,gen_isk1t,gen_isk2t,gen_isk3t,gen_isk1o,gen_isk2o,gen_isk3o,
kdvtoplam,aciklama,fat_altisk,fat_altisk2,kdvdurum,fatkalem_adedi,toplam_mik,geneltoplam,irs,takipkod,kayityapankul,kayittarihi,
duzeltmetarihi,duzeltmeyapankul,kdv1top,kdv8top,kdv18top,vade_tarihi,inckeyno,cari_tip,islem_turu,med)
values
('@kaynak@','@ftip@','@fno@','@hedef@','@tarih@','0.00','0.00','0.00','0.00',
'0.00','0.00','0.00','0.00','0.00','0.00','0.00','@aciklama@',
'@fat_altisk@','@fat_altisk2@','E','0','0','@geneltoplam@','H','x',
'giom14','@duzeltmetarihi@','@duzeltmetarihi@','giom14','0','0','0',
'@vadetarihi@','@inckeyno@','@cari_tip@','@islem_turu@','H')	
