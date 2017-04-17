SELECT sum(GENELTOPLAM)
FROM `fatura` WHERE FTIP = 'G' and VADE_TARIHI<='@vade_tarihi@' AND HEDEF = '@hedef@'