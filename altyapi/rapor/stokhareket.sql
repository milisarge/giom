WITH NUMARALANDIRILMIS AS
(
    SELECT REFNO,KOD,ROW_NUMBER() OVER(ORDER BY TARIH) AS 'SATIR_NO',
			TARIH,BELGENO,ACIKLAMA, 
			BORC, ALACAK
		from
		(select ENTEGREFKEY AS REFNO,NETHESKODU AS KOD,TARIH,BELGENO,ACIKLAMA,ba, 
		(case when ba='B' then tutar else 0 end)as BORC,
		(case when ba='A' then tutar else 0 end )as ALACAK
		from tblbnkhestra where netheskodu='@heskod' ) as k

)

SELECT B1.REFNO,(SELECT CONVERT(VARCHAR(10), B1.TARIH, 103) AS [DD-MM-YYYY]) as TARIH,B1.BELGENO,B1.ACIKLAMA, 
		B1.BORC,B1.ALACAK, --TB.TOP_BORC, TA.TOP_ALACAK, 
		TB.TOP_BORC-TA.TOP_ALACAK AS BAKIYE
		--BORC-ALACAK AS BAKIYE
	FROM NUMARALANDIRILMIS B1
	CROSS APPLY (
		SELECT SUM(B2.BORC) AS TOP_BORC
		FROM NUMARALANDIRILMIS B2
		WHERE B2.SATIR_NO <= B1.SATIR_NO 
			AND B2.KOD = B1.KOD ) TB
	CROSS APPLY (
		SELECT SUM(B3.ALACAK) AS TOP_ALACAK
		FROM NUMARALANDIRILMIS B3
		WHERE B3.SATIR_NO <= B1.SATIR_NO
			AND B3.KOD = B1.KOD ) TA
where B1.TARIH>=dateadd(day,-7,'@bastarih') 
	ORDER BY B1.SATIR_NO