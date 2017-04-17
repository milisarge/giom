# -*- coding: utf-8 -*-

class Tblfatura:
	def __init__(self):
		self.kaynak=""
		self.ftip=""
		self.fno=""
		self.hedef=""
		self.tarih=""
		self.khtutar=0.0
		self.kdtutar=0.0
		self.sat_iskt_top=0.0
		self.mfaz_iskt_top=0.0
		self.gen_isk1t=0.0
		self.gen_isk2t=0.0
		self.gen_isk3t=0.0
		self.gen_isk1o=0.0
		self.gen_isk2o=0.0
		self.gen_isk3o=0.0
		self.kdvtoplam=0.0
		self.aciklama=""
		self.fat_altisk=0.0
		self.fat_altisk2=0.0
		self.kdvdurum=""
		self.fatkalem_adedi=0
		self.toplam_mik=0
		self.geneltoplam=0.0
		self.irs="H"
		self.takipkod=""
		self.kayityapankul=""
		self.kayittarihi=""
		self.duzeltmeyapankul=""
		self.duzeltmetarihi=""
		self.kdv1top=0.0
		self.kdv8top=0.0
		self.kdv18top=0.0
		self.vadetarihi='0000-00-00'
		self.inckeyno=0
		self.cari_tip=""
		self.islem_turu="BOS"
		self.med='H'
	def ekle(self,sql):
		sql=sql.replace('@kaynak@',self.kaynak)
		sql=sql.replace('@ftip@',self.ftip)
		sql=sql.replace('@fno@',self.fno)
		sql=sql.replace('@hedef@',self.hedef)
		sql=sql.replace('@tarih@',str(self.tarih))
		sql=sql.replace('@khtutar@',str(self.khtutar))
		sql=sql.replace('@kdtutar@',str(self.kdtutar))
		sql=sql.replace('@kdvtoplam@',str(self.kdvtoplam))
		sql=sql.replace('@sat_iskt_top@',str(self.sat_iskt_top))
		sql=sql.replace('@kdvdurum@',self.kdvdurum)
		sql=sql.replace('@fatkalem_adedi@',str(self.fatkalem_adedi))
		sql=sql.replace('@mfaz_iskt_top@',str(self.mfaz_iskt_top))
		sql=sql.replace('@toplam_mik@',str(self.toplam_mik))
		sql=sql.replace('@geneltoplam@',str(self.geneltoplam))
		sql=sql.replace('@takipkod@',self.takipkod)
		sql=sql.replace('@irs@',self.irs)
		sql=sql.replace('@gen_isk1t@',str(self.gen_isk1t))
		sql=sql.replace('@gen_isk2t@',str(self.gen_isk2t))
		sql=sql.replace('@gen_isk3t@',str(self.gen_isk3t))
		sql=sql.replace('@gen_isk1o@',str(self.gen_isk1o))
		sql=sql.replace('@gen_isk2o@',str(self.gen_isk2o))
		sql=sql.replace('@gen_isk3o@',str(self.gen_isk3o))
		sql=sql.replace('@kayityapankul@',self.kayityapankul)
		sql=sql.replace('@kayittarihi@',str(self.kayittarihi))
		sql=sql.replace('@duzeltmeyapankul@',self.duzeltmeyapankul)
		sql=sql.replace('@duzeltmetarihi@',str(self.duzeltmetarihi))
		sql=sql.replace('@kdv1top@',str(self.kdv1top))
		sql=sql.replace('@kdv8top@',str(self.kdv8top))
		sql=sql.replace('@kdv18top@',str(self.kdv18top))
		sql=sql.replace('@aciklama@',self.aciklama)
		sql=sql.replace('@fat_altisk@',str(self.fat_altisk))
		sql=sql.replace('@fat_altisk2@',str(self.fat_altisk2))
		sql=sql.replace('@vadetarihi@',str(self.vadetarihi))
		sql=sql.replace('@inckeyno@',str(self.inckeyno))
		sql=sql.replace('@cari_tip@',str(self.cari_tip))
		sql=sql.replace('@islem_turu@',str(self.islem_turu))
		sql=sql.replace('@med@',str(self.med))
		return sql
	def yukle(self,fatura):
		self.kaynak=fatura[0]
		self.ftip=fatura[1]
		self.fno=fatura[2]
		self.hedef=fatura[3]
		self.tarih=fatura[4]
		self.khtutar=fatura[5]
		self.kdtutar=fatura[20]
		self.sat_iskt_top=fatura[6]
		self.mfaz_iskt_top=fatura[7]
		self.gen_isk1t=fatura[8]
		self.gen_isk2t=fatura[9]
		self.gen_isk3t=fatura[10]
		self.gen_isk1o=fatura[11]
		self.gen_isk2o=fatura[12]
		self.gen_isk3o=fatura[13]
		self.kdvtoplam=fatura[14]
		self.aciklama=fatura[17]
		self.fat_altisk=fatura[15]
		self.fat_altisk2=fatura[16]
		self.kdvdurum=fatura[18]
		self.fatkalem_adedi=fatura[19]
		self.toplam_mik=fatura[20]
		self.geneltoplam=fatura[22]
		self.irs=fatura[23]
		self.takipkod=fatura[24]
		self.kayityapankul=fatura[25]
		self.kayittarihi=fatura[26]
		self.duzeltmeyapankul=fatura[27]
		self.duzeltmetarihi=fatura[28]
		self.kdv1top=fatura[29]
		self.kdv8top=fatura[30]
		self.kdv18top=fatura[31]
		self.vadetarihi=fatura[32]
		self.inckeyno=fatura[33]
		self.cari_tip=fatura[34]
		self.islem_turu=fatura[35]
		self.med=fatura[36]