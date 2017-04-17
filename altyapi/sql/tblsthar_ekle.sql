INSERT INTO sthar (
STOK_KODU,FISNO,MIKTAR,TARIH,NF,BF,KDVORAN,ACIKLAMA,SATISK,MALFISK,FTIP,SATISK2,SATISK3,HEDEF,PLASIYER_KODU,TAKIPKOD,
TAKIPKOD2,SIRA,IRSALIYE_NO,IRSALIYE_TARIH,OLCUBR,VADE_TARIHI,KAYNAK,DUZELTMETARIHI,KAYITTARIHI,FINCKEYNO)
VALUES
('@stok_kodu@', '@fisno@', '@miktar@', '@tarih@', '@nf@', '@bf@', '@kdvoran@','@aciklama@' , '@satisk@', '@malfisk@', '@ftip@',
'@satisk2@', '@satisk3@', '@hedef@','@plasiyer_kodu@' , '@takipkod@' , '@takipkod2@' , '@sira@', '@irsaliye_no@' ,
'@irsaliye_tarih@' , '@olcubr@','@vadetarihi@' , '@kaynak@', 
'@duzeltmetarihi@','@kayittarihi@', '@finckeyno@');