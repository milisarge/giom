import sqlite3 as lite
import random
import sys
import platform
import os

yol=''

if platform.system()=='Linux':
	yol='/opt//giom/'
sys.path.append(yol)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               


from mysqlmak import *


class vt():
	vt_adi = "" 
	tablo_adi=""
	mak=mysqlmak()
	def __init__(self):
		self.vt_adi=yol+"stoklist.db" 
	
	def reset(self):
		con = lite.connect('stoklist.db')
		cur = con.cursor()   
		cur.execute("DROP TABLE IF EXISTS stoklist")
		cur.execute("CREATE TABLE stoklist(sira INTEGER PRIMARY KEY AUTOINCREMENT,stkod TEXT,stkad TEXT,miktar REAL,bf REAL,tutar REAL,stoklistno INT)")
	def hareketsil(self,stoklistno):
		con = lite.connect('stoklist.db')
		with con:    
			cur = con.cursor()    
			cur.execute("delete from stoklist where stoklistno='"+stoklistno+"'")
	def yenihareket(self):
		self.tablo_adi=str(random.randrange(1,1000))+".stk"
	def yenihareket(self,fisno):
		self.tablo_adi=str(fisno)+".stk"	
	def kaydet2(self,stkad,miktar,bf):
		con = lite.connect(self.vt_adi)
		cur = con.cursor()
		tutar=round(bf*miktar,2)
		if(self.mak.stok2(stkad)):
			stkod=self.mak.stok2(stkad).kod
		else:
			return ("\n"+"--------------HATA:STOK ADI BULUNAMADI -->"+stkad+"\n")
		if(bf==-1):
			bf=round(float(self.mak.stok2(stkad).satis_fiat3),3)
			tutar=miktar*bf
		stokhar=(stkod,stkad,miktar,bf,tutar,self.tablo_adi)
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar)  			
			print "+",stkod,stkad[0:15],miktar,bf,tutar,self.tablo_adi
			return "yok"
		print "excel stk kayitda sorun olustu."
	def kaydet(self,stkod,miktar,bf):
		con = lite.connect(self.vt_adi)
		cur = con.cursor()
		tutar=round(bf*miktar,2)
		if(self.mak.stok(stkod)):
			stkad=self.mak.stok(stkod).isim
		else:
			return ("--------------------HATA:STOK KODU BULUNAMADI -->"+stkod)
		if(bf==-1):
			bf=round(float(self.mak.stok(stkod).satis_fiat3),3)
			tutar=miktar*bf
		stokhar=(stkod,stkad,miktar,bf,tutar,self.tablo_adi)
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar)  			
			print "+",stkod,stkad[0:15],miktar,bf,tutar,self.tablo_adi
			return "yok"
		print "excel stk kayitda sorun olustu."
	
	def kasa_kaydet(self,tarih,kaynak,hedef,tutar):
		tarih=self.mak.tarih_format(tarih)
		tutar=float(tutar)*-1
		tutar=str(tutar)
		sonuc=self.mak.kasakayit(tarih,'HAL_NAKIT','CARI',tutar,kaynak,hedef,'')
		print "vt islem sonuc:",sonuc
		
	def yazdir(self,stoklistno):
		con = lite.connect(self.vt_adi)
		cur = con.cursor() 
		cur.execute("select * from stoklist where stoklistno='"+stoklistno+"'")  
		data = cur.fetchall()	
		print data
							
				
							
