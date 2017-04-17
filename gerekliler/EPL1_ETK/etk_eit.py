import urllib2
import time
import os

while(1>0):
	try:
		time.sleep(2)
		cevab=urllib2.urlopen('http://X.X.X.:yyyy/etk_yazdir?kontrol')
		print "sunucu aktif	etiket bekleniyor....."
		etkbilgi=cevab.read()
		if(etkbilgi!="yok"):
			etiket=etkbilgi.split('@')
			isim=etiket[0]
			sf=etiket[1]
			sablon=open('etk_sablon.dos', 'r').read()
			yetiket=sablon.replace('@stok_adi@',isim)
			yetiket=yetiket.replace('@sf@',sf)
			open('yetiket.dos', 'w').write(yetiket)
			print yetiket
			#os.system("webyazdir.bat")
			os.system("webyazdir.sh")
	except:
		time.sleep(4)
		print "sunucu bekleniyor....."
