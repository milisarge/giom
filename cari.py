# -*- coding: utf-8 -*-

class Cari:
	def __init__(self, kod="", isim="",adres="", tel="", vergino="", 
	vergiyer="",sube="",muhkod="",eposta="",tip="",tel2="",iskoran="",cari_tip="",
	vadegunu=0,grupkod="",kod1="",iban=""):
		self.kod = kod
		self.isim = isim
		self.adres = adres
		self.tel=tel
		self.tel2=tel2
		self.vergino=vergino
		self.vergiyer=vergiyer
		self.sube=sube
		self.muhkod=muhkod
		self.eposta=eposta
		self.tip=tip
		self.iskoran=iskoran
		self.vadegunu=vadegunu
		self.cari_tip=cari_tip
		self.grupkod=grupkod
		self.kod1=kod1
		self.iban=iban
	def jsonla(self):
		cari={'isim':self.isim,'kod':self.kod,
		'adres':str(self.adres).decode('iso-8859_9'),'tel':self.tel,
		'tel2':self.tel2,'vergino':self.vergino,
		'vergiyer':str(self.vergiyer).decode('iso-8859_9'),'muhkod':self.muhkod,'eposta':self.eposta,
		'tip':self.tip,'iskoran':str(self.iskoran),'vadegunu':self.vadegunu,'cari_tip':self.cari_tip,'grupkod':self.grupkod,
		'kod1':self.kod1,'iban':self.iban.decode('iso-8859_9')}
		return cari
