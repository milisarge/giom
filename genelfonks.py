# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
import datetime
import os
import decimal
import time
import codecs
from logcu import *
import random
import re
import sqlite3 as lite
import sys
import urllib2, urllib
import MultipartPostHandler
from random import randint
import datetime
from mysqlmak import *
from cari import *
from stok import *
from fatura import *
from htmlrapor import *
from stdnum import ean
import ctypes

class Arge:
	def coklu_topla(self,miktar):
		if '+' in str(miktar):
			miktarlar=miktar.split('+')
			topmik=0
			for mik in miktarlar:
				if mik.find(",") > 0 :
					mik=mik.replace(',','.')
				mik=float(mik)
				topmik+=mik
			miktar=topmik
			miktar=str(miktar)
		if '*' in str(miktar):
			miktarlar=miktar.split('*')
			topmik=1
			for mik in miktarlar:
				if mik.find(",") > 0 :
					mik=mik.replace(',','.')
				mik=float(mik)
				topmik*=mik
			miktar=topmik
			miktar=str(miktar)
		if '/' in str(miktar):
			miktarlar=miktar.split('/')
			bolnn=miktarlar[0]
			bol=miktarlar[1]
			if bolnn.find(",") > 0 :
				bolnn=bolnn.replace(',','.')
			if bol.find(",") > 0 :
				bol=bol.replace(',','.')
			miktar=float(bolnn)/float(bol)
		else:
			return miktar
		return str(round(float(miktar),3))
		
	def saat_al(self):	
		saatstr=""
		now = datetime.datetime.now()
		saatstr=now.strftime("%H:%M:%S")
		return saatstr
	
	def tyazi_cevir(self,tutar):
		yaziyla1=""
		yaziyla2=""
		if(tutar.find(",") != -1):
			tumtutar = tutar.split(",")
			yaziyla1 = cevir(tumtutar[0]) + "TL"
			yaziyla2 = cevir(tumtutar[1]) + "KRStur"
		elif(tutar.find(".") != -1):
			tumtutar = tutar.split(".")
			yaziyla1 = cevir(tumtutar[0]) + "TL."
			yaziyla2 = cevir(tumtutar[1]) + "KRStur"
		else:
			yaziyla1 = cevir(tutar) + "TLdir"
			yaziyla2 = ""
		return [yaziyla1,yaziyla2]
	
	def barkod_tamamla(self,barkode):
		ek=ean.calc_check_digit(str(barkode))
		return str(barkode)+ek
		
	def dosyaYdizi(self,dosya):
		icerik=codecs.open(dosya, "r","latin5")
		stoklar=[]
		for satir in icerik:
			sat=satir.split("\n")[0]
			sat=sat.split("\r")[0]
			stoklar.append([sat])
		return stoklar
	
	
		
	def servisler_al(self,dosya="servisler.ayar"):
		icerik=codecs.open(dosya, "r","latin5")
		servisler=[]
		for satir in icerik:
			sat=satir.split("\n")[0]
			sat=sat.split("\r")[0]
			servisler.append(sat)
		return servisler
	def z_rapor_analiz(self,dosya):
		anahtar="SIGNATURE=GNDZDETAILS.GDF"
		zrap=[]
		with open(dosya,'r') as f:
			for satir in f:
				rap=[]
				satlar=satir.split()
				if satlar[0]==anahtar or anahtar=="tm":
					if anahtar=="tm":
						fisno=satlar[1]
						tarih=satlar[4]
						rap.append(tarih)
						rap.append(fisno)
						for x in range(0,10): 
							rap.append(satlar[24+x])
						gentop=satlar[8]
						rap.append(gentop)
				anahtar="tm"
				if len(rap)>0:
					zrap.append(rap)	
		#print zrap		
		rapor=statikrapor()
		sutunlar=["TARIH","FISNO","KONTOR","TEMEL GIDA","MUHTELIF","UN-EKMEK","TEMIZLIK","GAZETE","SIGARA","MANAV","ET","OZ URETIM","TOPLAM"]
		return rapor.diziYhtml(zrap,sutunlar)
		open("zrapo.html","w").write(rapor.diziYhtml(zrap,sutunlar))
	def termal_yazdir(self,sablon="kasa"):
		if sablon == "kasa":
			saat=self.saat_al()
			
			if('makbuznot' in request.form and 'makbuznot3' in request.form):
				makbuznot=request.form["makbuznot"]
				makbuznot2=request.form["makbuznot"]
				makbuznot3=request.form["makbuznot3"]
			else:
				makbuznot="---"
				makbuznot2="---"
				makbuznot3="-"
			fistip=""
			
			tutarf=tutar
			if(tutar!=""):
				if(tutar[0] != "-" ):  ## sayi negatif degilse , yani para girisi oluyorsa
					fistip=("TAHSILAT").decode('utf-8')
					makbuznot2=makbuznot
					makbuznot=makbuznot3
				else:                     ## sayi negatif ise , yani para ciktisi oluyorsa
					fistip=("TEDİYE").decode('utf-8')
					tutarf=tutar
					tutar = tutar[1:]
					makbuznot2=makbuznot3
			tyazi=self.tyazi_cevir(tutar)	
			
			if(guncislem=="CARI" and secim!=""):
				fishedef=secim.split('@')[0]
				fishedef=fishedef[0:31]
			else:
				fishedef=secim.split('@')[1]
				fishedef=fishedef[0:31]
				
			with codecs.open("kasacikti.prn", "w","latin5") as out:
				for line in codecs.open("sablon.prn",'r',"latin5"):
					line=line.replace("xnushanot","ikinci".decode('utf-8'))
					line=line.replace("xtarih", str(tarih))
					line=line.replace("xsaat",str(saat))
					line=line.replace("xfistip",fistip)
					line=line.replace("xfisno",str(session['ksira']))
					line=line.replace("xtutar",tutar.encode('iso8859-9'))
					line=line.replace("xyaziyla1",tyazi[0].encode('iso8859-9'))
					line=line.replace("xyaziyla2",tyazi[1].encode('iso8859-9'))
					line=line.replace("xhedef",fishedef)
					line=line.replace("xmakbuzack",kasaack)
					line=line.replace("xteslimeden",makbuznot2)
					line=line.replace("xteslimalan",makbuznot)
					out.write(line)
	
			with codecs.open("kasacikti2.prn", "w","latin5") as out:
				for line in codecs.open("sablon.prn",'r',"latin5"):
					line=line.replace("xnushanot","birinci".decode('utf-8'))
					line=line.replace("xtarih", str(tarih))
					line=line.replace("xsaat",str(saat))
					line=line.replace("xfistip",fistip)
					line=line.replace("xfisno",str(session['ksira']))
					line=line.replace("xtutar",tutar.encode('iso8859-9'))
					line=line.replace("xyaziyla1",tyazi[0].encode('iso8859-9'))
					line=line.replace("xyaziyla2",tyazi[1].encode('iso8859-9'))
					line=line.replace("xhedef",fishedef)
					line=line.replace("xmakbuzack",kasaack)
					line=line.replace("xteslimeden",makbuznot2)
					line=line.replace("xteslimalan",makbuznot)
					out.write(line)
			os.system("yazdir1.bat")
			os.system("yazdir2.bat")

		
