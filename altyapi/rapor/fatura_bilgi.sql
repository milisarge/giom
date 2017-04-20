set @kimlik:=@kimlik@;
SELECT A.STOK_ADI AS MALZEME,
round(B.MIKTAR,3) AS MIKTAR,
round(B.BF,3) AS FIAT,
round((B.BF*B.MIKTAR),3) AS TUTAR FROM TBLSTSABIT AS A 
INNER JOIN STHAR AS B ON A.STOK_KODU=B.STOK_KODU 
WHERE B.FINCKEYNO=@kimlik
GROUP BY B.SIRA,A.STOK_ADI,B.MIKTAR,B.BF order by B.SIRA;