from mysqlmak import *
import os
import sys
import datetime
import platform


yazdir_komut="yazdir.bat"
yazdir_komut2="yazdir2.bat"
dosya="lzrfis.prn"
if platform.system()=='Linux':
	yazdir_komut="./yazdir.sh "+dosya
	yazdir_komut2="./yazdir2.sh "+dosya
	
aralik=22
font="2"
printstr=""
mak=mysqlmak()
#fisno="w00000000000002"
#fattip="dat"
ftip=sys.argv[1]
fkod=sys.argv[2]
yazici=sys.argv[3]	
if ftip=='f':	
	fatura=mak.fatura_yukle(fkod)
	stharsay=len(mak.sthlar_al(fkod))
	print "stharsay:",stharsay
	stharuz=stharsay*aralik
	etkuz=stharuz+(12*aralik)
	#etkuz=600
	print "etkuz:",etkuz
	tarih=str(mak.tarih_turk(fatura.tarih))
	hedef=fatura.hedef
	fno=fatura.fno
	stharlar=mak.sthlar_al(fkod)
else:
	stharsay=len(mak.stk_al(fkod))
	print "stharsay:",stharsay
	stharuz=stharsay*aralik
	etkuz=stharuz+(12*aralik)
	print "etkuz:",etkuz
	tarih=str(datetime.datetime.now()).split()[0]
	hedef=fkod
	fno=fkod
	stharlar=mak.stk_al(fkod)
printstr+="I8,A,001"+"\n"
printstr+="D3"+"\n"
printstr+="R0,0"+"\n"
printstr+="Q"+str(etkuz)+"\n"
printstr+="q600"+"\n"
printstr+="I8,E,001"+"\n"
printstr+="N"+"\n"
inceayar=10
if mak.cari(hedef):
	cisim=mak.cari(hedef).isim
else:
	cisim=""
printstr+="A600,"+str(etkuz-aralik)+",2,"+font+",1,1,N,"+'"'+"--"+'"'+"\n"
printstr+="A600,"+str(etkuz-(aralik*2)-inceayar)+",2,"+font+",1,1,N,"+'"'+"tarih:"+'"'+"\n"
printstr+="A530,"+str(etkuz-(aralik*2)-inceayar)+",2,"+font+",1,1,N,"+'"'+tarih+'"'+"\n"
printstr+="A360,"+str(etkuz-(aralik*2)-inceayar)+",2,"+font+",1,1,N,"+'"'+hedef+'"'+"\n"
printstr+="A285,"+str(etkuz-(aralik*2)-inceayar)+",2,"+font+",1,1,N,"+'"'+" fisno:"+'"'+"\n"
printstr+="A200,"+str(etkuz-(aralik*2)-inceayar)+",2,"+font+",1,1,N,"+'"'+fno+'"'+"\n"
printstr+="A600,"+str(etkuz-(aralik*4))+",2,"+font+",1,1,N,"+'"'+cisim.decode('latin5')+'"'+"\n"
printstr+="A600,"+str(etkuz-(aralik*5))+",2,"+font+",1,1,N,"+'"'+"--------------------------------------------------"+'"'+"\n"

printstr+="A550,"+str(etkuz-(aralik*6))+",2,"+font+",1,1,N,"+'"'+"MALZEME"+'"'+"\n"
printstr+="A280,"+str(etkuz-(aralik*6))+",2,"+font+",1,1,N,"+'"'+"MIKTAR"+'"'+"\n"
printstr+="A190,"+str(etkuz-(aralik*6))+",2,"+font+",1,1,N,"+'"'+"FIYAT"+'"'+"\n"
printstr+="A100,"+str(etkuz-(aralik*6))+",2,"+font+",1,1,N,"+'"'+"TUTAR"+'"'+"\n"
printstr+="A600,"+str(etkuz-(aralik*7))+",2,"+font+",1,1,N,"+'"'+"--------------------------------------------------"+'"'+"\n"

sthara=8 #sthar aralik katsayisi
inceayar=5

meblag=0
topmik=0
for sthar in stharlar:
	if ftip=='f':
		malzeme=(sthar[2])[0:26]
		miktar=float(sthar[3])
		fiyat=round(float(sthar[6]),2)
		tutar=round(sthar[7],2)
	else:
		malzeme=(sthar[2])[0:26]
		miktar=float(sthar[3])
		fiyat=round(float(sthar[4]),2)
		tutar=round(sthar[5],2)
	tutar=float(tutar)
	topmik+=miktar
	meblag+=tutar
	
	printstr+="A600,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+malzeme+'"'+"\n"
	printstr+="A280,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+str(miktar)+'"'+"\n"
	printstr+="A190,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+str(fiyat)+'"'+"\n"
	printstr+="A100,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+str(tutar)+'"'+"\n"
	sthara+=1
	
sthara+=1
printstr+="A220,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+"TOPLAM"+'"'+"\n"

printstr+="A110,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+str(float(meblag))+'"'+"\n"
printstr+="A600,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+"TOPMIK"+'"'+"\n"

printstr+="A480,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+str(float(topmik))+'"'+"\n"
sthara+=2
font="2"
printstr+="A525,"+str(etkuz-(aralik*sthara)-inceayar)+",2,"+font+",1,1,N,"+'"'+"GIOM SISTEMI"+'"'+"\n"

	
printstr+="P1"+"\n"
codecs.open("lzrfis.prn", "w","latin5").write(printstr)
#open("lzrfis.prn","w").write(printstr)
#os.system("copy ppzbr.prn lpt2")
if yazici=="1":
	os.system(yazdir_komut)
	log=open("yazdir.log","r").read()
	print "yazdirma log-->",log
	if "failed" in str(log):
		print "tekrar deneniyor"
		os.system(yazdir_komut)	
else:
	os.system(yazdir_komut2)
