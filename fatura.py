# -*- coding: utf-8 -*-

class Fatura:
	def __init__(self):
		
		self.tarih=""
		self.vadetarih=""
		self.fisno=""
		self.kaynak=""
		self.hedef=""
		self.stharlistno=""
		self.stharlist=[]
		self.kdvdurum=""
		self.fattip=""
		self.takipkod=""
		self.aciklama=""
		self.islem=""
		self.tutar=0
		self.med='H'
		self.irs='H'
		self.fkod=""
		self.toplam_mik=0
		self.vadesay=1
		self.caritip=""
		ntop=""
		gtop=""
		kalemsay=""
		kdv1top=""
		kdv8top=""
		kdv18top=""
		fincno=""
		islem_turu=""
		kdvtop=0
		kaydeden=""
		duzelten=""
	def goster(self):
		print self.tarih,self.vadetarih,self.fisno,self.kaynak,self.hedef,self.stharlistno,self.kdvdurum,
		self.fattip,self.takipkod,self.aciklama,self.islem,self.tutar,self.med,self.fkod,self.caritip
	