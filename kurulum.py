#!/usr/bin/python2

import sys
moduller=["pymysql","flask","iniparse","xlwt","xlrd"]
modul="s"
onay="yok"
while onay=="yok":
	try:
		moduller=map(__import__, moduller)
		onay="var"
	except ImportError as hata:
		modul=str(hata).split()[3]
		sys.stderr.write("{} modulu bulunamadi \n".format(modul))
		secim= raw_input( modul+" modulu kurulsun mu?(e/h)" )
		if(secim=="e"):
			os.system("pip install "+modul)
		else:
			print modul+" modulu kurulamadi!!!"

print "kurulum tamamlandi"
