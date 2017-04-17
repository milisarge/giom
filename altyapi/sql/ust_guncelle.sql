UPDATE fatura SET FNO='@fno@',TARIH='@tarih@',VADE_TARIHI='@vadetarih@',ACIKLAMA='@aciklama@',GENELTOPLAM='@tutar@',IRS='@irs@',MED='@med@',HEDEF='@hedef@',DUZELTMETARIHI=NOW()
where INCKEYNO='@fkod@';
update sthar set tarih='@tarih@',FISNO='@fno@',HEDEF='@hedef@',VADE_TARIHI='@vadetarih@',DUZELTMETARIHI=NOW() where FINCKEYNO='@fkod@';
