SELECT SUM( GENELTOPLAM )
FROM fatura as f inner join tblcasabit as c on c.cari_kod=f.kaynak
WHERE FTIP = 'C' AND c.grup_kodu='@kaynak@' AND HEDEF = '@hedef@' and  VADE_TARIHI<='@vade_tarihi@'
