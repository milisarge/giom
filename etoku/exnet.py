import datetime
import xlrd
from xls import *
from vt import *
from iniparse import ConfigParser
import sys
#ayarlar
ayar=ConfigParser()
ayardos='.\exnet\DATA\default.ini'
ayardosyol='.\\exnet\\DATA\\'
if len(sys.argv) > 1:
	ayardos=sys.argv[1]
ayar.read(ayardos)
dosya=ayar.get("excel","dosya")	
sayfa=ayar.get("excel","sayfa")	
fisler=ayar.get("excel","fisler")
fisler=fisler.split("@")	
form=xls()
#komut satirindan yukleme yapmak icin
#form nesnesine ilgili sayfa yukleniyor.
form.sayfa(ayardosyol+dosya,sayfa)

for fis in fisler:
	print fis
	merkezhc=ayar.get(fis,"merkez")
	merkez=form.deger(merkezhc)
	tarihhc=ayar.get(fis,"tarih")
	tarih=form.degertarih(tarihhc)
	islemhc=ayar.get(fis,"islem")
	islem=form.deger(islemhc)
	urtkodhc=ayar.get(fis,"urtkod")
	urtkod=form.deger(urtkodhc)
	alicihc=ayar.get(fis,"alici")
	alici=form.deger(alicihc)
	aktifhc=ayar.get(fis,"aktif")
	aktif=form.deger(aktifhc)
	dizi=ayar.get(fis,"stoklar")
	icerik=dizi.split("@")
	stoklar=form.degerdizi(icerik[0],int(icerik[1]),int(icerik[2]))
	dizi=ayar.get(fis,"miktarlar")
	icerik=dizi.split("@")
	miktarlar=form.degerdizi(icerik[0],int(icerik[1]),int(icerik[2]))
	dizi=ayar.get(fis,"bfler")
	icerik=dizi.split("@")
	bfler=form.degerdizi(icerik[0],int(icerik[1]),int(icerik[2]))
	
	tarihx=str(tarih).split('-')
	tarihx=tarihx[0][0:2]+tarihx[1]+tarihx[2]
	fisno=merkez+"_"+islem+"_"+urtkod+"_"+tarihx
	#print merkez,tarih,islem,urtkod,alici
	#print stoklar,miktarlar,bfler,fisno
	#kayit kapali onay menusu olacak
	form.kayit(stoklar,miktarlar,bfler,fisno)
	print "----------------------"

#stokliste kayt
#form.kayit(stoklar,miktarlar,bfler)






#print str(form.cell(0,2).value)
#hucre("aa55") 

#print form.degertarih(tarih)
#print form.deger(merkez)
#print form.deger(trans)
#print form.deger(islem)
#print form.degerfloat("c10")


	


	
