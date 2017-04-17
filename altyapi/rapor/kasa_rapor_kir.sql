SELECT date(fatura.TARIH) as tarih, tblcasabit.CARI_ISIM, fatura.ACIKLAMA,
case when (ftip='G' and kaynak in ('@kaynak@') ) then round(geneltoplam,2) else 0 end AS GIRIS,
case when (ftip='C' and kaynak in ('@kaynak@') ) then round(geneltoplam,2) else 0 end AS CIKIS,
fatura.med
FROM fatura
INNER JOIN tblcasabit ON fatura.HEDEF = tblcasabit.CARI_KOD
WHERE fatura.KAYNAK = '@kaynak@' OR fatura.HEDEF='@kaynak@'
AND fatura.TARIH BETWEEN '@bastarih@' AND '@sontarih@'
ORDER BY tarih



rapor=[]
aratop=0
tarihgc=row[0][0]
for r in row:
	tarih=r[0]
	if tarih != tarihgc:
		tarihgc=r[0]
		print "aratop",aratop
		aratop=0
	if r[3]==0:
		aratop-=r[4]
	else:
		aratop+=r[3]
	print r
print aratop