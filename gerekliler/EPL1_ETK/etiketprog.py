# -*- coding: utf-8 -*-
import os
import sys
from easygui import *

while (1==1):
	stokkod = enterbox(msg="stok kodunu giriniz.",default="")
	stok_kodu=stokkod
	stok_adi=""
	sf=""
	bulundu="hayir"
	with open('GNCPLUF.GTF', 'r') as inF:
		for line in inF:
			if stok_kodu in line and stok_kodu!="":
			
				if(line[29:53]==line[5:29]):
					print "yazdirilan stok"+"\n"
					print "stokadi",line[53:78]
					stok_adi=line[53:78]
					print "satis fiat",line[355:360]
					sf=line[355:360]
					bulundu="evet"
	if bulundu=="hayir":
		msgbox(msg="STOK KODU BULUNAMADI !!!")
	else:
		printstr=""
		printstr+="^XA"+"\n"
		printstr+="^FO21,93^A0N,34,48^FD"+stok_adi+"^FS"+"\n"
		printstr+="^FO304,180^A0N,45,64^FD"+sf+" TL^FS"+"\n"
		printstr+="^FT262,250^A0N,14,19^FH\^FDGIOM SISTEM^FS"+"\n"
		printstr+="^XZ"
		open("rafetiket.dos","w").write(printstr)
		#sistem win ise
		#os.system("yazdir.bat")
		os.system("yazdir.sh")
