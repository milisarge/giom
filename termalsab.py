# -*- coding: utf-8 -*-
from genelfonks import *
import platform

arge=Arge()
makbuz1_komut="kasa_makbuz1.bat"
makbuz2_komut="kasa_makbuz2.bat"
if platform.system()=='Linux':
	makbuz1_komut="./kasa_makbuz1.sh"
	makbuz2_komut="./kasa_makbuz2.sh"

class TermalSablon:
	def __init__(self):
		self.tarih=""
		self.fisno=""
		self.saat=arge.saat_al()
		self.mnot="---"
		self.mnot2="---"
		self.mnot3="-"
		self.tutar=0
		self.fistip=""
		self.hedef=""
		self.ack=""
		
	def yazdir(self,sablon="kasa"):
		if sablon == "kasa":
			saat=arge.saat_al()
			if(self.tutar!=""):
				if(self.tutar>0 ): 
					self.fistip=("TAHSİLAT").decode('utf-8')
					self.mnot2=self.mnot
					self.mnot=self.mnot3
				else:                    
					self.fistip=("TEDİYE").decode('utf-8')
					self.tutar = self.tutar*-1
					self.mnot2=self.mnot3
			tutar=str(self.tutar)
			tyazi=arge.tyazi_cevir(tutar)	
			tarih=self.tarih
			fistip=self.fistip
			fisno=self.fisno
			hedef=self.hedef
			ack=self.ack
			mnot=self.mnot
			mnot2=self.mnot2
			with codecs.open("kasacikti.prn", "w","latin5") as out:
				for line in codecs.open("sablon.prn",'r',"latin5"):
					line=line.replace("xnushanot","İKİNCİ".decode('utf-8'))
					line=line.replace("xtarih", str(tarih))
					line=line.replace("xsaat",str(saat))
					line=line.replace("xfistip",fistip)
					line=line.replace("xfisno",fisno)
					line=line.replace("xtutar",tutar.encode('iso8859-9'))
					line=line.replace("xyaziyla1",tyazi[0].encode('iso8859-9'))
					line=line.replace("xyaziyla2",tyazi[1].encode('iso8859-9'))
					line=line.replace("xhedef",hedef.decode('iso8859-9'))
					line=line.replace("xmakbuzack",ack)
					line=line.replace("xteslimeden",mnot2)
					line=line.replace("xteslimalan",mnot)
					out.write(line)
	
			with codecs.open("kasacikti2.prn", "w","latin5") as out:
				for line in codecs.open("sablon.prn",'r',"latin5"):
					line=line.replace("xnushanot","BİRİNCİ".decode('utf-8'))
					line=line.replace("xtarih", str(tarih))
					line=line.replace("xsaat",str(saat))
					line=line.replace("xfistip",fistip)
					line=line.replace("xfisno",fisno)
					line=line.replace("xtutar",tutar.encode('iso8859-9'))
					line=line.replace("xyaziyla1",tyazi[0].encode('iso8859-9'))
					line=line.replace("xyaziyla2",tyazi[1].encode('iso8859-9'))
					line=line.replace("xhedef",hedef.decode('iso8859-9'))
					line=line.replace("xmakbuzack",ack)
					line=line.replace("xteslimeden",mnot2)
					line=line.replace("xteslimalan",mnot)
					out.write(line)
			os.system(makbuz1_komut)
			os.system(makbuz2_komut)
