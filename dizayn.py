# -*- coding: utf-8 -*-
import math

class kalemyapi():
	kdv=""
	ad=""
	miktar=""
	birim=""
	brfiyat=""
	tutar=""

class faturayapi():
	hedef=""
	adres=""
	vdaire=""
	vergino=""
	tarih=""
	tarih2=""
	saat=""
	kalemler=[]
	tutaryaziyla=""
	kdvsiztutar=""
	kdv1=""
	kdv8=""
	kdv18=""
	gtoplam=""
	merkezsicilno=""
	subesicilno=""
	mersisno=""
	kaynakwebadresi=""
	sayfayaz=[]
	
class dizaynyapi():
	
	def sayfala(self,fatura="", kalemadedi=0):
		if not fatura :
			return "Fatura Nesnesi Bos Geldiginden Sayfalara Bolunemedi"

		#if (len(fatura.kalemler)>kalemadedi) : #kalem sayýsý faturanýn max kalem adedinden fazlaysa 1den fazla sayfa olacak
		sayfalar = []
		
		# ilk sayfa #########################################
		# ilk sayfa icin max kalem adedinden bir eksik yazilacak, son satira ise devir yazilacak
		# sonraki sayfalarda devir hem sayfa baþýna hem de sayfa sonuna yazýlacaðý için ilk sayfa ayrý deðerlendiriliyor
		sayfa = []
		sayfadevir = 0.0
		for i in range(kalemadedi-1) :		
			if(len(fatura.kalemler)==i):
				break
			sayfa.append( fatura.kalemler[i] )
			sayfadevir = sayfadevir + float(fatura.kalemler[i].tutar)
		
		# ilk sayfanýn sonuna devir toplamý ekle
		# devir eklenirken kalem nesnesi oluþturuluyor çünkü html de yazdýrýrken kolay olsun! 
		# faturada "DEVÝR" kelimesini yazdýrmak için, kalemin "ad" kýsmýna bu kelimeyi ekliyoruz.
		# NOT: herhangi bir kýsma da eklenebilirdi. mesela brfiyat
		
		
		kalem=kalemyapi()
		kalem.kdv=""
		kalem.ad=""
		kalem.miktar=""
		kalem.birim=""
		kalem.brfiyat="DEVIR"
		kalem.tutar= "{:.2f}".format( sayfadevir )
		
		# ilk sayfa sonuna devir eden kalemi ekliyoruz
		sayfa.append( kalem )
		
		# oluþan ilk sayfa faturanýn sayfalar nesnesine eklenicek
		sayfalar.append(sayfa) 
		
		
		#for kalem in sayfa:
			#print "--",kalem.brfiyat,kalem.tutar
		# kalan kalemleri sayfalara paylaþtýracaz
		kalan_kalem = len(fatura.kalemler) - (kalemadedi-1) # ilk sayfaya yazilan kalemlerin sayýsýný toplamdan cikart
		sayfa_basi_kalem = kalemadedi - 2					# sonraki sayfalarda ilk satýr önceki devire ait,  son satir sonraki sayfaya devire ait.
		sayfa_sayisi = float(kalan_kalem) / float(sayfa_basi_kalem) # ilk sayfa hariç kaç sayfa daha yazdýracaðýmýzý buluyoruz.
		sayfa_sayisi = math.ceil(sayfa_sayisi) # bölüm sonucunu yukarý yuvarlýyoruz çünkü bir kalem dahi kalsa, yeni bir sayfa gerekecek
		sayfa_sayisi = int(sayfa_sayisi) 
		
		
		for sayfaindex in range(sayfa_sayisi) :
			
			sayfa = []
			
			# ilk sayfa haricindeki sayfalarýn baþýna da devir toplamý ekle
			# NOT: sayfanýn üstünde kalan kalemlerin toplamýndan gelen devir
			
			# devir eklenirken kalem nesnesi oluþturuluyor çünkü html de yazdýrýrken kolay olsun! 
			# faturada "DEVÝR" kelimesini yazdýrmak için, kalemin "ad" kýsmýna bu kelimeyi ekliyoruz.
			# NOT: herhangi bir kýsma da eklenebilirdi. mesela brfiyat
			kalem=kalemyapi()
			kalem.kdv=""
			kalem.ad=""
			kalem.miktar=""
			kalem.birim=""
			kalem.brfiyat="DEVIR"
			kalem.tutar="{:.2f}".format( sayfadevir )
			sayfa.append( kalem )
			
			# Sayfalardaki devir toplamlarýný hesaplamak için kullanýlýyor.
			for kalemindex in range(sayfa_basi_kalem) :
				index = sayfa_basi_kalem * sayfaindex + kalemadedi-1 + kalemindex
				if(index<len(fatura.kalemler)) :
					sayfa.append( fatura.kalemler[index] )
					sayfadevir += float(fatura.kalemler[index].tutar)
			
			
			# ilk sayfa haricindeki sayfaların sonuna da devir toplamý ekle
			# NOT: sayfanýn üstünde kalan kalemlerin toplamýndan gelen devir
			
			# devir eklenirken kalem nesnesi oluşturuluyor çünkü html de yazdýrýrken kolay olsun! 
			# faturada "DEVÝR" kelimesini yazdýrmak için, kalemin "ad" kýsmýna bu kelimeyi ekliyoruz.
			# NOT: herhangi bir kýsma da eklenebilirdi. mesela brfiyat
			kalem=kalemyapi()
			kalem.kdv=""
			kalem.ad=""
			kalem.miktar=""
			kalem.birim=""
			kalem.brfiyat="DEVIR"
			kalem.tutar="{:.2f}".format( sayfadevir )
			sayfa.append( kalem )
			
			sayfalar.append(sayfa)
		'''for sayfa in sayfalar:
			for kalem in sayfa:
				print kalem.brfiyat,kalem.tutar
		'''
		return sayfalar
