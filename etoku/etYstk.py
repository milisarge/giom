import datetime
import xlrd
from xls import *
from vt import *
from iniparse import ConfigParser
import sys
import platform

#ayarlarin yuklenmesi
ayar=ConfigParser()
yol='.\etoku\DATA\\'
if platform.system()=='Linux':
	yol="etoku/DATA/"

ayardos='bal.ini'
if len(sys.argv) > 1:
	ayardos=sys.argv[1]
	
ayar.read(yol+ayardos)
print "-->",yol+ayardos
dosya=yol+ayar.get("excel","dosya")	
sayfa=ayar.get("excel","sayfa")	
yon=ayar.get("excel","yon")	
if len(sys.argv) > 2:
	sayfa=sys.argv[2]
if len(sys.argv) > 3:
	konsdos=sys.argv[3]
	dosya=yol+konsdos
form=xls()
#sayfanin yuklenmesi
form.sayfa(dosya,sayfa)
fisler=ayar.get("excel","fisler")
fisler=fisler.split("@")	

for fis in fisler:
	print fis
	#
	islem=ayar.get(fis,"islem")
	islemdeger=form.deger(islem)
	aktifhc=ayar.get(fis,"aktif")
	aktif=form.deger(aktifhc)
	merkezhc=ayar.get(fis,"merkez")
	merkez=form.deger(merkezhc)
	hedefhc=ayar.get(fis,"hedef")
	hedef=form.deger(hedefhc)
	#fatura islemlerine dayali
	if islemdeger in ['DAT','ACIKIS','AGIRIS','SATIS','ALIS','ALISIRS']:
		urtkodhc=ayar.get(fis,"urtkod")
		urtkod=form.deger(urtkodhc)	
		stotip=ayar.get(fis,"stotip")
		if(yon=="dikey"):
			tarihhc=ayar.get(fis,"tarih")
			tarih=form.degertarih(tarihhc)
			islemhc=ayar.get(fis,"islem")
			islem=form.deger(islemhc)
			dizi=ayar.get(fis,"stoklar")
			icerik=dizi.split("@")
			stoklar=form.dikey_konumlar(icerik[0],int(icerik[1]),int(icerik[2]))
			dizi=ayar.get(fis,"miktarlar")
			icerik=dizi.split("@")
			miktarlar=form.dikey_konumlar(icerik[0],int(icerik[1]),int(icerik[2]))
			dizi=ayar.get(fis,"bfler")
			icerik=dizi.split("@")
			bfler=form.dikey_konumlar(icerik[0],int(icerik[1]),int(icerik[2]))
			#tarihx=str(tarih).split('-')
			#tarihx=tarihx[0][0:2]+tarihx[1]+tarihx[2]
			#fisno=merkez+"_"+islem+"_"+urtkod+"_"+tarihx
			fisno=merkez+'@'+hedef+'@'+urtkod+'@'+islem+"@"+tarih
			form.kayit(stoklar,miktarlar,bfler,fisno,stotip)
			
		if(yon=="yatay"):
		
			icerikbf=ayar.get(fis,"bfler").split('@')
			bfkonum=form.yatay_konumlar(icerikbf[0],icerikbf[1],icerikbf[2])
			icerik=ayar.get(fis,"stoklar").split('@')
			stokkonum=form.yatay_konumlar(icerik[0],icerik[1],icerik[2])
			iceriktar=ayar.get(fis,"tarihler").split('@')
			tarihsutun=iceriktar[0]
			kayitbas=int(iceriktar[1])
			kayitson=int(iceriktar[2])
			for kayitsira in range(kayitbas,kayitson+1):
				
				tarihkonum=tarihsutun+str(kayitsira)
				tarih=form.degertarih(tarihkonum)
				miktarkonum=form.yatay_konumlar(kayitsira,icerik[1],icerik[2])
				tarihx=str(tarih).split('-')
				tarihx=tarihx[1]+tarihx[2]
				fisno=merkez+'@'+hedef+'@'+urtkod+'@'+islem+"@"+tarih
				form.goster(stokkonum,miktarkonum,bfkonum)
				form.kayit(stokkonum,miktarkonum,bfkonum,fisno,stotip)
	'''if islemdeger in ['KASA']:
		secal=0
		while(secal==0):
			secim= raw_input( "KASA HAREKET ISLENSIN MI? (e/h)" )
			if(secim=="e"):
				vt=vt()
				tutarhc=ayar.get(fis,"tutar")
				tutar=form.degerfloat(tutarhc)
				print tutar
				vt.kasa_kaydet(tarih,merkez,hedef,str(tutar))
				secal=1
			elif(secim=="h"):
				secal=1
			else:
				print "gecersiz secim"
	'''	
		#print islemdeger,tarih,merkez,hedef,tutar
		
