import xlrd
from vt import *
import os
#wb = xlrd.open_workbook(dosya)
#sh = wb.sheet_by_name(sayfa)

class xls():
	alfa = "abcdefghijklmnopqrstuvwxyz" 
	vt=""
	
	form=""
	def __init__(self):
		
		self.vt=vt()
	def bilgi(self):
		print "xls nesnesi"
	def sayfa(self,dosya,sayfa):
		
		wb = xlrd.open_workbook(dosya,encoding_override='cp1252')
		sh = wb.sheet_by_name(sayfa)
		self.form=sh
	
	def deger(self,konum):
		deger=""
		konum=konum.lower()
		try:
			sutun=int(self.alfa.index(konum[0]))
			satir=int(konum.strip(konum[0]))-1
			#print "konum",konum
			deger=str(self.form.cell(satir,sutun).value)
			if(deger==""):
				deger="bos deger"
			#deger=deger.split(".")[0]
			sonek=deger[(len(deger)-2):len(deger)]
			if sonek==".0":
				deger=deger[0:(len(deger)-2)]
		except IndexError:
			deger="bos deger"
		return deger
		
	def degerfloat(self,konum):
		deger=""
		konum=konum.lower()
		try:
			sutun=int(self.alfa.index(konum[0]))
			satir=int(konum.strip(konum[0]))-1
			deger=str(self.form.cell(satir,sutun).value)
			if(deger=="0.0"):
				deger="bos float"
			if(deger==""):
				deger="bos float"
			#deger=deger.split(".")[0]
		except IndexError:
			deger="bos deger"
		return deger
		
	def degertarih(self,konum):
		tarihson=""
		konum=konum.lower()
		try:
			sutun=int(self.alfa.index(konum[0]))
			satir=int(konum.strip(konum[0]))-1
			tarih=xlrd.xldate_as_tuple((self.form.cell(satir,sutun).value),0)
			tarihson=str(tarih[0])+"-"+str(tarih[1])+"-"+str(tarih[2])	
		except ValueError:
			tarihson="tarih yok"
		return tarihson
	def dikey_konumlar(self,harf,bas,son):
		konumlar=[]
		for sayi in range(bas,son+1):
			konumlar.append(harf+str(sayi))
		return konumlar
	def yatay_konumlar(self,sayi,hbas,hson):
		konumlar=[]
		alfabe=self.alfa
		for harf in alfabe:
			if alfabe.index(harf)>=alfabe.index(hbas) and alfabe.index(harf)<=alfabe.index(hson):
				konumlar.append(harf+str(sayi))
		return konumlar
		
	def kayit(self,stoklar,miktarlar,bfler,fisno,stotip="kod"):
		self.vt.yenihareket(fisno)
		for stokx in stoklar:
			indeks=stoklar.index(stokx)
			stok=self.deger(stokx)
			if(stok!="bos deger"):   #bu kosul olursa bos degerler alinmaz
				miktar=self.degerfloat(miktarlar[indeks])
				if(miktar!="bos float"):
					miktar=float(miktar)
					bf=self.degerfloat(bfler[indeks])
					if(bf!="bos float"):
						bf=float(bf)
						if(stotip!="kod"):
							hata=self.vt.kaydet2(stok,miktar,bf)
						else:	
							hata=self.vt.kaydet(stok,miktar,bf)
						if(hata!="yok"):
							print hata
		#print self.vt.tablo_adi
		#self.vt.yazdir(self.vt.tablo_adi)
	def goster(self,stoklar,miktarlar,bfler):
		for stokx in stoklar:
			indeks=stoklar.index(stokx)
			#print indeks
			stok=self.deger(stokx)
			if(stok!="bos deger"):   #bu kosul olursa bos degerler alinmaz
				miktar=self.degerfloat(miktarlar[indeks])
				if(miktar!="bos float"):
					miktar=float(miktar)
					bf=self.degerfloat(bfler[indeks])
					if(bf!="bos float"):
						bf=float(bf)
						print stok,miktar,bf	
