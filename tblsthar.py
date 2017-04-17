# -*- coding: utf-8 -*-

class Tblsthar:
	def __init__(self):
		self.stok_kodu=""
		self.fisno=""
		self.miktar=0.0
		self.tarih='0000-00-00'
		self.vadetarihi='0000-00-00'
		self.nf=0.0
		self.bf=0.0
		self.kdvoran=0.0
		self.aciklama=""
		self.ftip=""
		self.satisk=0.0
		self.malfisk=0.0
		self.hedef=""
		self.satisk2=0.0
		self.satisk3=0.0
		self.sira=-1
		self.olcubr="AD"
		self.takipkod=""
		self.takipkod2=""
		self.kaynak=""
		self.irsaliye_no=""
		self.irsaliye_tarih='0000-00-00'
		self.duzeltmetarihi='0000-00-00'
		self.kayittarihi='0000-00-00'
		self.finckeyno=""
		self.plasiyer_kodu=""
		self.incno=-1
	def ekle(self,sql):
		sql=sql.replace('@stok_kodu@',self.stok_kodu)
		sql=sql.replace('@fisno@',self.fisno)
		sql=sql.replace('@miktar@',str(self.miktar))
		sql=sql.replace('@tarih@',str(self.tarih))
		sql=sql.replace('@nf@',str(self.nf))
		sql=sql.replace('@bf@',str(self.bf))
		sql=sql.replace('@kdvoran@',str(self.kdvoran))
		sql=sql.replace('@aciklama@',self.aciklama)
		sql=sql.replace('@ftip@',self.ftip)
		sql=sql.replace('@hedef@',self.hedef)
		sql=sql.replace('@takipkod@',self.takipkod)
		sql=sql.replace('@takipkod2@',self.takipkod2)
		sql=sql.replace('@sira@',str(self.sira))
		sql=sql.replace('@olcubr@',str(self.olcubr))
		sql=sql.replace('@vadetarihi@',str(self.vadetarihi))
		sql=sql.replace('@kaynak@',self.kaynak)
		sql=sql.replace('@irsaliye_no@',self.irsaliye_no)
		sql=sql.replace('@irsaliye_tarih@',str(self.irsaliye_tarih))
		sql=sql.replace('@malfisk@',str(self.malfisk))
		sql=sql.replace('@satisk@',str(self.satisk))
		sql=sql.replace('@satisk2@',str(self.satisk2))
		sql=sql.replace('@satisk3@',str(self.satisk3))
		sql=sql.replace('@finckeyno@',str(self.finckeyno))
		sql=sql.replace('@plasiyer_kodu@',self.plasiyer_kodu)
		sql=sql.replace('@kayittarihi@',str(self.kayittarihi))
		sql=sql.replace('@duzeltmetarihi@',str(self.duzeltmetarihi))
		return sql
	def yukle(self,sthar):
		self.stok_kodu=sthar[0]
		self.fisno=sthar[1]
		self.miktar=sthar[2]
		self.tarih=sthar[3]
		self.vadetarihi=sthar[22]
		self.nf=sthar[4]
		self.bf=sthar[5]
		self.kdvoran=sthar[6]
		self.aciklama=sthar[7]
		self.ftip=sthar[10]
		self.satisk=sthar[8]
		self.malfisk=sthar[9]
		self.hedef=sthar[13]
		self.satisk2=sthar[11]
		self.satisk3=sthar[12]
		self.sira=sthar[17]
		self.olcubr=sthar[20]
		self.takipkod=sthar[15]
		self.takipkod2=sthar[16]
		self.kaynak=sthar[23]
		self.irsaliye_no=sthar[18]
		self.irsaliye_tarih=sthar[19]
		self.incno=sthar[21]
		self.duzeltmetarihi=sthar[24]
		self.kayittarihi=sthar[25]
		self.finckeyno=sthar[26]
		self.plasiyer_kodu=sthar[14]
		 