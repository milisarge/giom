#!/usr/bin/python
 # -*- coding: utf-8 -*-
import MultipartPostHandler, urllib2
import sys

#try:
	#url = enterbox(msg="servis",default='http://192.168.1.100:6060/dinamiko')
url='http://192.168.1.100:6060/dinamiko'

if len(sys.argv) > 3:
	parola=sys.argv[1]
	komut=sys.argv[2]
	param=sys.argv[3]
	params = { 'parola':parola,'komut' : komut, 'param' : param  }
	opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
	cevap=opener.open(url, params).read()
	print cevap
	#msgbox(cevap[0:24])
else:
	print "parametre eksik"
	#path=fileopenbox(msg='YUKLENECEK EXCEL DOSYA SECIMI')
	#path2=fileopenbox(msg='YUKLENECEK INI DOSYA SECIMI')
	#parola= enterbox(msg="parola",default='')
	
	
#except:
#	print "kritik hata"
#	#msgbox("HATALI DURUM")
