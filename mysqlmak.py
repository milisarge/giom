#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pymysql
import sqlite3 as lite
import sys
import decimal
import datetime
import copy
import codecs
import os
import json
from random  import *
from subprocess import Popen, PIPE
from logcu import *
from cari import *
from stok import *
from fatura import *
from stokhareket import *
from tblsthar import *
from tblfatura import *
from htmlrapor import *
from sayidan_yaziya import cevir
from copy import deepcopy
import xlwt
from mysql_ayar import *

class mysqlmak:
	
	global baglanti
	baglanti=MysqlBaglanti()
	
	global cursor
	global conn
	global stoklistvt
	global l
	l=Logcu()
	
	def __init__(self):
		self.test='nesne olustu'
		self.stoklistvt=self.ayar_al('999','stoklist_db')
		
	def test(self):
		sql="select * from tblstsabit where stok_kodu='5555' "
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
	
	def stok(self,stkod):
		sql=open('./altyapi/sql/stok.sql','r').read()
		sql=sql.replace('@stkod',stkod)
		return self.stok_format(sql)
	
	def stok2(self,stkad):
		sql=open('./altyapi/sql/stok2.sql','r').read()
		sql=sql.replace('@stkad',str(stkad))
		return self.stok_format(sql)
	
	def stok_format(self,sql):	
		stok=Stok()
		#self.cursor.execute(sql)
		#rows = self.cursor.fetchall()
		rows=self.calistir(sql)
		if(rows != None):
			for rowx in rows:
				rowx=list(rowx)
				if(len(rowx)>0):
					'''j=0
					for r in rowx:
						print j,r
						j+=1'''
					stok.sube_kodu=rowx[0]
					stok.kod=rowx[2]
					stok.isim=rowx[4]
					stok.grup_kodu=rowx[5]
					stok.kod_1=rowx[6]
					stok.kod_2=rowx[7]
					stok.kod_3=rowx[8]
					stok.kod_4=rowx[9]
					stok.kod_5=rowx[10]
					stok.barkod1=rowx[54]
					stok.barkod2=rowx[55]
					stok.barkod3=rowx[56]
					stok.barkod4=rowx[127]
					stok.barkod5=rowx[128]
					stok.barkod6=rowx[129]
					stok.satici_kodu=rowx[11]
					stok.olcu_br1=rowx[12]
					stok.olcu_br2=rowx[13]
					stok.birim_agirlik=round(float(rowx[35]),3)
					stok.payda=round(float(rowx[15]),3)
					stok.kdv_orani=rowx[37]
					stok.alis_kdv_kodu=rowx[57]
					if(rowx[26]):stok.satis_fiat1=round(float(rowx[26]),3)
					else:stok.satis_fiat1=0.0
					if(rowx[27]):stok.satis_fiat2=round(float(rowx[27]),3)
					else:stok.satis_fiat2=0.0
					if(rowx[28]):stok.satis_fiat3=round(float(rowx[28]),3)
					else:stok.satis_fiat3=0.0
					if(rowx[58]):stok.alis_fiat1=round(float(rowx[58]),3)				
					else:stok.alis_fiat1=0.0
					if(rowx[59]):stok.alis_fiat2=round(float(rowx[59]),3)				
					else:stok.alis_fiat2=0.0
					if(rowx[60]):stok.alis_fiat3=round(float(rowx[60]),3)				
					else:stok.alis_fiat3=0.0
					#print "stok olustu"
				return stok
		else:
			return None		
	
	def barkod_kontrol(self,kod,barkod):
		sql=open('./altyapi/sql/barkod_kontrol.sql','r').read()
		sql=sql.replace('@kod@',kod)	
		sql=sql.replace('@barkod@',barkod)	
		sonuc=self.calistir(sql)
		#print "bkon",kod,barkod
		if(sonuc):
			return sonuc[0][0]
		else:
			return sonuc
	
	def stoklar_al(self,kriter,aranan):
		sqldosya='./altyapi/sql/stok_sorgu.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kriter@',kriter)
		sql=sql.replace('@aranan@',aranan)
		sonuc=self.calistir(sql)
		stokodlar=[]
		for stok in sonuc:
			stokodlar.append(stok[0])
		return stokodlar
	
	def stoklar_ads(self):
		sqldosya='./altyapi/sql/stok_ads.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sonuc=self.calistir(sql)
		stokads={}
		for stok in sonuc:
			ads={stok[0]:stok[1]}
			stokads.update(ads)
		return stokads
	'''
	def stoklar_kdv(self):
		sqldosya='./altyapi/sql/stok_kdv.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sonuc=self.calistir(sql)
		stokkdv={}
		for stok in sonuc:
			kdv={stok[0]:stok[1]}
			stokkdv.update(kdv)
		return stokkdv
	'''
	def stoklar_pos(self,kriter,aranan):
		sqldosya='./altyapi/sql/stok_pos.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kriter@',kriter)
		sql=sql.replace('@aranan@',aranan)
		sonuc=self.calistir(sql)
		return sonuc
	
	def stok_harkont(self,stok):
		sql=open('./altyapi/sql/stok_harkont.sql','r').read()
		sql=sql.replace('@kod@',stok.kod)
		if self.calistir(sql) is None:
			return "yok"
		else:
			return "var"
	def stok_guncelle(self,stok,mod):
		if(mod=='s'):
			sql=open('./altyapi/sql/stok_sil.sql','r').read()
		if(mod=='g'):
			sql=open('./altyapi/sql/stok_guncelle.sql','r').read()
		if(mod=='y'):
			sql=open('./altyapi/sql/stok_ekle.sql','r').read()
		sql=sql.replace('@kod@',stok.kod)
		if(mod=='s'):
			return self.calis(sql)
		stok.satis_fiat1=stok.satis_fiat1.replace(',','.')
		stok.satis_fiat2=stok.satis_fiat2.replace(',','.')
		stok.satis_fiat3=stok.satis_fiat3.replace(',','.')
		stok.alis_fiat1=stok.alis_fiat1.replace(',','.')
		stok.alis_fiat2=stok.alis_fiat2.replace(',','.')
		stok.alis_fiat3=stok.alis_fiat3.replace(',','.')
		stok.birim_agirlik=stok.birim_agirlik.replace(',','.')
		sql=sql.replace('@isim@',stok.isim)	
		sql=sql.replace('@barkod1@',stok.barkod1)	
		sql=sql.replace('@barkod2@',stok.barkod2)
		sql=sql.replace('@barkod3@',stok.barkod3)	
		sql=sql.replace('@barkod4@',stok.barkod4)	
		sql=sql.replace('@barkod5@',stok.barkod5)	
		sql=sql.replace('@barkod6@',stok.barkod6)	
		sql=sql.replace('@alkdv@',str(stok.alis_kdv_kodu))	
		sql=sql.replace('@satkdv@',str(stok.kdv_orani))
		sql=sql.replace('@satis_fiat3@',str(stok.satis_fiat3))	
		sql=sql.replace('@satis_fiat2@',str(stok.satis_fiat2))	
		sql=sql.replace('@satis_fiat1@',str(stok.satis_fiat1))
		sql=sql.replace('@alis_fiat1@',str(stok.alis_fiat1))
		sql=sql.replace('@alis_fiat2@',str(stok.alis_fiat2))
		sql=sql.replace('@alis_fiat3@',str(stok.alis_fiat3))
		sql=sql.replace('@grupkod@',str(stok.grup_kodu))	
		sql=sql.replace('@kod_1@',str(stok.kod_1))	
		sql=sql.replace('@kod_2@',str(stok.kod_2))	
		sql=sql.replace('@kod_3@',str(stok.kod_3))	
		sql=sql.replace('@kod_4@',str(stok.kod_4))	
		sql=sql.replace('@kod_5@',str(stok.kod_5))	
		sql=sql.replace('@olcu_br1@',stok.olcu_br1)
		sql=sql.replace('@olcu_br2@',stok.olcu_br2)
		sql=sql.replace('@payda@',str(stok.payda))
		sql=sql.replace('@birim_agirlik@',stok.birim_agirlik)
		sql=sql.replace('@satici_kodu@',stok.satici_kodu)
		return self.calis(sql)
	
	def stok_bakiye(self,stokod,merkez,tarih='getdate()'):
		sql=open('./altyapi/sql/stok_bakiye.sql','r').read()
		sql=sql.replace('@stokod@',stokod)	
		sql=sql.replace('@merkez@',merkez)	
		sql=sql.replace('@tarih@',tarih)	
		rows=self.calistir(sql)
		if(rows):
			for r in rows:
				bakiye=r[0]
				if(bakiye!=None):
					return float(bakiye)
				else:
					return 0
		else: 
			return 0
	def stok_satis(self,stokod,merkez,gerigun):
		sql=open('./altyapi/sql/stok_satis.sql','r').read()
		sql=sql.replace('@stokod@',stokod)	
		sql=sql.replace('@merkez@',merkez)	
		sql=sql.replace('@gerigun@',gerigun)
		rows=self.calistir(sql)
		if(rows):
			for r in rows:
				satis=r[0]
				if(satis!=None):
					return float(satis)
				else:
					return 0
		else: 
			return 0
		
	def son_satis(self,stokod,merkez):
		sql=open('./altyapi/sql/son_satis.sql','r').read()
		sql=sql.replace('@stokod@',stokod)	
		sql=sql.replace('@merkez@',merkez)
		rows=self.calistir(sql)
		if rows[0][0]:
			return self.tarih_turk(str(rows[0][0]))#.split()[0]
		else:
			return "yok"
			
	def son_giris(self,stokod,merkez):
		sql=open('./altyapi/sql/son_alis.sql','r').read()
		sql=sql.replace('@stokod@',stokod)	
		sql=sql.replace('@merkez@',merkez)
		rows=self.calistir(sql)
		if rows[0][0]:
			return self.tarih_turk(str(rows[0][0]))#.split()[0]
		else:
			return "yok"
			
	def son_sayim(self,stokod,merkez):
		sql=open('./altyapi/sql/son_sayim.sql','r').read()
		sql=sql.replace('@stokod@',stokod)	
		sql=sql.replace('@merkez@',merkez)
		rows=self.calistir(sql)
		if rows[0][0]:
			return self.tarih_turk(str(rows[0][0]))#.split()[0]
		else:
			return "yok"
			
	def stokadlar_getir(self,stkad):
		sql=open('./altyapi/sql/stokadlar_getir.sql','r').read()
		sql=sql.replace('@stkad@',stkad)		
		rows=self.calistir(sql)
		stokadlar=[]
		if(rows):
			for r in rows:
				#r=str(r[0])
				stokadlar.append(r[0])
			return stokadlar
		else: 
			return None
	
	def sthar_al(self,harkod):
		sqldosya='./altyapi/sql/sthar_al.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@harkod@',str(harkod))
		rows=self.calistir(sql)
		stharnes=Tblsthar()
		stharnes=rows[0]
		return stharnes
	
	def sthar_sil(self,harkod):
 		stharo=self.sthar_al(harkod)
		if(stharo[1][0:2]=='s_' or stharo[13]=="sth_servis"):
			sqldosya='./altyapi/sql/sthar_sil.sql'
			sql=codecs.open(sqldosya,'r','iso-8859_9').read()
			sql=sql.replace('@harkod@',harkod)
			sonuc=self.calis(sql)
			return sonuc
		return "sayim harici hareketler silinemez."
	def sthar_bilgi(self,stkod,iscari,gun="-1"):
		sqldosya='./altyapi/sql/sthar_bilgi.sql'
		if gun != "-1":
			sqldosya='./altyapi/sql/sthar_bilgi_gunlu.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@iscari@',iscari)
		sql=sql.replace('@stkod@',stkod)
		if gun != "-1":
			sql=sql.replace('@gun@',str(gun))
		#salt sql data icin
		#sqldosyadata='./sql_cikti/sthar_bilgi_data.sql'
		#codecs.open(sqldosyadata,'w','iso-8859_9').write(sql)
		rapor=statikrapor()
		topsut=[5,6,9,9,9,9,9,9,9,9]
		rapor.sql(sql,alt=2,link='?sthkod',yukle="sth_yukle",sil="sth_sil",topsut=topsut)		
		raporhar=rapor.getHtml()
		
		sqldosya='./altyapi/sql/sthar_altbilgi.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@iscari@',iscari)
		sql=sql.replace('@stkod@',stkod)
		#salt sql data icin
		
		raporalt=statikrapor()
		topsutalt=[-1,-1,-1,-1,-1,-1]
		raporalt.sql(sql,alt=0,topsut=topsutalt)		
		raporalt=raporalt.getHtml()
		
		return raporhar+"<br>"+raporalt
		
		'''
		sth=[]
		rows=self.calistir(sql)
		rowx=rows[0]
		for row in rowx:
			print ".....",row
			sth.append(str(row).decode('latin5'))
		return sth
		'''
	def sthar_altbilgi(self,stkod,iscari):
		sqldosya='./altyapi/sql/sthar_altbilgi.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@iscari@',iscari)
		sql=sql.replace('@stkod@',stkod)
		#salt sql data icin
		#sqldosyadata='./altyapi/sql/sthar_bilgi_data.sql'
		#codecs.open(sqldosyadata,'w','iso-8859_9').write(sql)
		rapor=statikrapor()
		topsut=[0,0,0,0,0,0]
		rapor.sql(sql,alt=2,topsut=topsut)		
		return rapor.getHtml()
	
	def stok_sorgu(self,kriter,aranan):
		sqldosya='./altyapi/sql/stok_sorgu.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kriter@',kriter)
		sql=sql.replace('@aranan@',aranan)
		#salt sql data icin
		#sqldosyadata='./altyapi/sql/sthar_bilgi_data.sql'
		#codecs.open(sqldosyadata,'w','iso-8859_9').write(sql)
		rapor=statikrapor()
		rapor.sql(sql,alt=2)	
		return rapor.getHtml()
	
	def stok_sorgu2(self,kriter,aranan):
		sqldosya='./altyapi/sql/stok_sorgu.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kriter@',kriter)
		sql=sql.replace('@aranan@',aranan)
		rows=self.calistir(sql)
		sorg=[]
		for row in rows:
			sorg.append(row)
		return sorg
	
	def stok_sorgu_perfo(self,kriter,aranan,sira):
		sira=int(sira)
		if kriter=="FKOD":
			rows=self.sthar_detay(aranan,sonuc='dizi')
			stoko=1
		else:
			sqldosya='./altyapi/sql/stok_sorgu.sql'
			sql=codecs.open(sqldosya,'r','iso-8859_9').read()
			sql=sql.replace('@kriter@',kriter)
			sql=sql.replace('@aranan@',aranan)
			rows=self.calistir(sql)
			stoko=0
		if rows and sira<len(rows):
			if rows[sira]:
				return rows[sira][stoko]
		return 0
	
	def stkno_kontrol(self,stoklistno):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			cur = con.cursor()    
			#eskisi
			cur.execute("SELECT * FROM stoklist where stoklistno='"+stoklistno+"'")
			#cur.execute("select sira,stkod,stkad,sum(miktar),bf,tutar,stoklistno from stoklist where stoklistno='"+stoklistno+"' group by stkad,bf order by stkad")
			rows = cur.fetchall()
		return rows
	
		
	def stk_bilgi(self,stoklistno=""):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		#con = lite.connect('stoklist.db')
		with con:    
			cur = con.cursor()    
			#eskisi
			cur.execute("SELECT stkod,stkad,miktar,bf,tutar,stoklistno,sira FROM stoklist where stoklistno='"+stoklistno+"'")
			#cur.execute("select sira,stkod,stkad,sum(miktar),bf,tutar,stoklistno from stoklist where stoklistno='"+stoklistno+"' group by stkad,bf order by stkad")
			rows = cur.fetchall()
			col_names = [i[0] for i in cur.description]
		rapor=statikrapor()
		topsut=[9,9,9,2,9,4,9,9]
		rapor.sql(sqlstr=None,alt=2,sqlitero=rows,colnam=col_names,link='/stk_goster?sira',yukle="stk_yukle",sil="stk_sil",topsut=topsut,noekle=1)	
		return rapor.getHtml()
	
	def stk_satsil(self,sirano):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:
			cur = con.cursor()
			cur.execute("DELETE FROM stoklist WHERE sira="+sirano)
		return "tamam"
	def stk_list_al(self):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			try:
				cur = con.cursor()    
				cur.execute("SELECT stoklistno FROM stoklist group by stoklistno")
				rows = cur.fetchall()
			except:
				hata=sys.exc_info()[1]
				if(hata[1]=='database is locked'):	
					l.yaz('stoklist.db kilitlendi.')
		return rows
	
	def stk_kontrol(self,stoklistno=""):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		onay="olumsuz"
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT stkod FROM stoklist where stoklistno='"+stoklistno+"'")	
			rows = cur.fetchall()
		for row in rows:
			onay="olumlu"
			if(self.stok(row[0]) is None):
				l.yaz("stk_kontrol sorunlu stok: "+row[0])
				onay="olumsuz"
		return onay
		
	def stk_al(self,stoklistno=""):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			cur = con.cursor()   
			cur.execute("SELECT * FROM stoklist where stoklistno='"+stoklistno+"'")
			rows = cur.fetchall()
		return rows
	
	def stk_rapor_al(self,stkno=""):
		rapordizi=[]
		i=0
		kyt=self.stk_al(stkno)
		uz=len(kyt)
		for ro in kyt:
			i+=1
			if i<=uz:
				rapordizi.append([i,ro[2],ro[3],ro[4],ro[5]])
		rapor=statikrapor()
		dizibas=['no','isim','miktar','bf','tutar']
		top_sutlar=[-1,-1,2,-1,4]
		rapor_html=rapor.diziYhtml(rapordizi,dizibas,top_sutlar)
		return rapor_html
	
	def stk_birlestir(self,stkana,stkek):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:
			
			ekstklist=self.stk_al(stkek)
			cur = con.cursor() 
			for sthar in ekstklist:
				stharek=(sthar[1],sthar[2],float(sthar[3]),float(sthar[4]),float(sthar[5]),stkana)
				cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stharek)
			return "tamam"
		return "stk birlestirme sorun"	
	
	def stk_sira_al(self,stoklistno=""):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT sira FROM stoklist where stoklistno='"+stoklistno+"'")
			rows = cur.fetchall()
			return rows
			
	def stk_har_al(self,guncelsira=""):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT stkod,stkad,miktar,bf FROM stoklist where sira='"+guncelsira+"'")
			rows = cur.fetchall()
			return rows[0]
	
	def stk_kopyala(self,stkno,dbkopya=""):
		arrsiv=0
		stknokop="kopya_"+stkno
		if dbkopya=="":
			dbkopya=self.ayar_al('999','stoklist_db')
			con = lite.connect(dbkopya)
		else:
			arsiv=1
			con = lite.connect("stk_yedek/"+dbkopya+".db")
		with con:
			tbl_kont="SELECT name FROM sqlite_master WHERE type='table' AND name='stoklist';"
			stkhar=self.stk_al(stkno)
			cur = con.cursor()
			cur.execute(tbl_kont)
			rows = cur.fetchall()
			if len(rows)>0:
				print "mevcut vt'e eklendi."
			else:
				print "yeni vt olusturuldu."
				cur.execute("CREATE TABLE stoklist(sira INTEGER PRIMARY KEY AUTOINCREMENT,stkod TEXT,stkad TEXT,miktar REAL,bf REAL,tutar REAL,stoklistno INT)")
			for sthar in stkhar:
				stharek=(sthar[1],sthar[2],float(sthar[3]),float(sthar[4]),float(sthar[5]),stknokop)
				cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stharek)
			
		con.close()
		#self.stk_sil(stkno)
		'''
		if arsiv==1:
			komut="move "+dbkopya+" stk_yedek/"+dbkopya+".db"
			print komut
			os.system(komut)
		'''
		return "tamam"
	
	def stkgcc_tablo_olustur(self):
		con = lite.connect("stoklist.db")
		cur = con.cursor()
		with con:
			cur.execute("CREATE TABLE stoklistgcc(sira INTEGER PRIMARY KEY AUTOINCREMENT,stkod TEXT,stkad TEXT,miktar REAL,bf REAL,tutar REAL,stoklistno INT)")
		print "stoklistgcc tablosu olusturuldu."
	def stk_tablo_olustur(self):
		con = lite.connect("stoklist.db")
		cur = con.cursor()
		with con:
			cur.execute("CREATE TABLE stoklist(sira INTEGER PRIMARY KEY AUTOINCREMENT,stkod TEXT,stkad TEXT,miktar REAL,bf REAL,tutar REAL,stoklistno INT)")
		print "stoklist tablosu olusturuldu."
	def stk_fsb2_al(self,stoklistno=""):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			cur = con.cursor()    
			cur.execute("SELECT sum(tutar) FROM stoklist where stoklistno='"+stoklistno+"'")
			rows = cur.fetchall()
			toptut=rows[0][0]
			top=str(toptut)
			return round(float(top),3)
	def stk_ekle(self,stharyeni):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stharyeni)
	
	def stk_iskonto(self,stkno,icra):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:
			cur = con.cursor() 
			cur.execute("update stoklist set bf=round(bf*"+str(icra)+",2),tutar=round(tutar*"+str(icra)+",2) where stoklistno='"+str(stkno)+"'")
		return "tamam"
	
	def stk_yeniad(self,stkno,yeniad):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:
			cur = con.cursor() 
			sql="update stoklist set stoklistno='"+yeniad+"' where stoklistno='"+str(stkno)+"'"
			cur.execute(sql)
		return "tamam"
		
	def stk_sil(self,stkno):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		with con:    
			cur = con.cursor()    
			cur.execute("delete from stoklist where stoklistno='"+stkno+"'")
		con.close()
	def stkdb_icaktar(self,dbsec):
		yuk="_"+str(randint(0,9999))
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		conye = lite.connect(dbsec)
		with con:
			cur = con.cursor() 
			with conye:
				curye = conye.cursor() 
				curye.execute("SELECT * FROM stoklist")
				rowsye = curye.fetchall()
				for sthar in rowsye:
					if '@' in sthar[6]:
						ystk=sthar[6]
					else:
						ystk=sthar[6]+yuk
					stharek=(sthar[1],sthar[2],float(sthar[3]),float(sthar[4]),float(sthar[5]),ystk)
					cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stharek)	
				#os.system("del stk_yedek/"+dbsec+".db")
				return "tamam"
		return "sorun olustu"
	
	
	def stk_fsb_al(self,stoklistno="",gc='C'):
		fsb=[]
		stharlar=self.stk_al(stoklistno)
		sira=0
		ntop=0
		gtop=0
		
		for sthar in stharlar:
			sira+=1
			if gc=='C':
				kdvsi=self.stok(sthar[1]).kdv_orani
			else:
				kdvsi=self.stok(sthar[1]).alis_kdv_kodu
			if kdvsi is None:
				print "stok kdv bulunamadi"
				return None
			fiyat=sthar[4]
			bf=0.0
			nf=0.0
			nf=decimal.Decimal("%.2g" % nf)
			bf=decimal.Decimal("%.2g" % bf)
			
			nf=decimal.Decimal("%.8g" % fiyat)
			bf=nf
			kdvdahilmi="H"
			nttr=nf*(decimal.Decimal("%.3g" % sthar[3]))	
			gttr=bf*(decimal.Decimal("%.3g" % sthar[3]))*(kdvsi+100)/100
						
			ntop+=nttr.quantize(decimal.Decimal(10) ** -2)
			gtop+=gttr.quantize(decimal.Decimal(10) ** -2)
			
		fsb.append("toplam="+str(ntop))
		fsb.append("+kdv="+str(gtop))
		#dahilse
		stharlar=self.stk_al(stoklistno)
		sira=0
		ntop=0
		gtop=0
		for sthar in stharlar:
			sira+=1
			kdvsi=self.stok(sthar[1]).kdv_orani
			fiyat=sthar[4]
			bf=0.0
			nf=0.0
			nf=decimal.Decimal("%.2g" % nf)
			bf=decimal.Decimal("%.2g" % bf)
			
			bf=decimal.Decimal("%.8g" % fiyat)
			nf=(decimal.Decimal("%.8g" % fiyat)*100)/(kdvsi+100)
			nttr=nf*(decimal.Decimal("%.3g" % sthar[3]))	
			gttr=bf*(decimal.Decimal("%.3g" % sthar[3]))
					
			ntop+=nttr.quantize(decimal.Decimal(10) ** -2)
			gtop+=gttr.quantize(decimal.Decimal(10) ** -2)
			
		fsb.append("-kdv="+str(ntop))
		fsb.append("toplam="+str(gtop))
		return fsb
		
	def stok_virmanx(self,eskikod,yenikod):
		cev="tamam"
		if(self.stok(yenikod) is None):
			sql=open('./altyapi/sql/stok_virman.sql','r').read()	
			sql=sql.replace('@eskikod@',eskikod)
			sql=sql.replace('@yenikod@',yenikod)
			cev=self.calis(sql)
		if(cev=='tamam'):
			sql=open('./altyapi/sql/stok_virman2.sql','r').read()	
			sql=sql.replace('@eskikod@',eskikod)
			sql=sql.replace('@yenikod@',yenikod)
			cev=self.calis(sql)	
		return cev
	
	def cari(self,carikod):
		sql=open('./altyapi/sql/cari.sql','r').read()
		sql=sql.replace('@carikod',carikod)
		return self.cari_format(sql)
	
	def cari2(self,cariad):
		cari=Cari()
		sql=open('./altyapi/sql/cari2.sql','r').read()
		sql=sql.replace('@cariad',cariad)
		return self.cari_format(sql)
		
	def cari_format(self,sql):	
		cari=Cari()
		#self.cursor.execute(sql)
		#rows = self.cursor.fetchall()		
		rows=self.calistir(sql)
		if(rows != None):
			for rowx in rows:
				rowx=list(rowx)
				if(len(rowx)>0):
					#niteliklerin aktarilmasi
					cari.kod=rowx[2]
					cari.isim=rowx[6]
					cari.adres = rowx[14]
					cari.tel=rowx[3]
					cari.tel2=rowx[69]
					cari.vergino=rowx[17]
					cari.vergiyer=rowx[16]
					cari.sube=rowx[0]
					cari.muhkod=rowx[38]
					cari.eposta=rowx[46]
					cari.tip=rowx[7]
					cari.iskoran=rowx[32]
					cari.vadegunu=rowx[33]
					cari.cari_tip=rowx[7]
					cari.grupkod=rowx[8]
					cari.kod1=rowx[9]
					cari.kod2=rowx[10]
					cari.iban=rowx[13]
			return cari
		else:
			return None		
		
	def cariler_getir(self, aranan,tip=""):
		cariler=[]
		sql=open('./altyapi/sql/cariler_getir.sql','r').read()
		sql=sql.replace('@aranan@',aranan)	
		if tip!="":
			tip="and cari_tip in ('"+str(tip)+"')"
		sql=sql.replace('@tip@',tip)	
		#print sql
		rows=self.calistir(sql)
		if(rows):
			for rowx in rows:
				if(len(rowx)>0):
					cariad=rowx[1]
					cariler.append(cariad+"@"+rowx[0])
				else:
					return None
		return cariler
	
	def carihar_dokum(self,kaynak,hedef,bastarih,sontarih,sonuc="dizi"):
		sqldosya='./altyapi/sql/carihar_dokum.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kaynak@',kaynak)
		sql=sql.replace('@iscari@',hedef)
		bastarih=self.tarih_format(bastarih)
		sontarih=self.tarih_format(sontarih)
		sql=sql.replace('@bastarih@',bastarih)
		sql=sql.replace('@sontarih@',sontarih)
		codecs.open("sql_cikti/cari_hareket_data.sql",'w','iso-8859_9').write(sql)
		
		if(sonuc=='html'):
			rapor=statikrapor()
			rapor.sql(sql)	
			return rapor.getHtml()
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows
		
	def carihar_bilgi(self,iscari,karsicari,tarih,fisno,islemturu,hartip,irsdurum,sonuc="",modul="f",chgun=-1):
		mcari=iscari
		kcari=karsicari
		rapor_yas=""
		#print iscari,karsicari,tarih,fisno,islemturu,"gc:",hartip,irsdurum
		sqldosya=""
		devir_rapor=""
		if modul=="c":
			if chgun == -1:
				sqldosya='./altyapi/sql/carihar_bilgi_cx.sql'
			elif chgun == 7:
				sqldosya='./altyapi/sql/carihar_bilgi_cz.sql'
			else:
				sqldosya='./altyapi/sql/carihar_bilgi_cy.sql'
		if modul=="f":
			sqldosya='./altyapi/sql/carihar_bilgi_f.sql'
			iscariler=iscari.split(',')
			iscari=""
			for cari in iscariler:
				iscari+="'"+cari+"',"
			iscari=iscari[1:len(iscari)-2]
		if islemturu in ['K','B']:
			sqldosya='./altyapi/sql/carihar_bilgi_kb.sql'
		if(karsicari!=""):
			karsicariler=karsicari.split(',')
			karsicari=""
			for cari in karsicariler:
				karsicari+="'"+cari+"',"
			karsicari="'"+karsicari[1:len(karsicari)-2]+"'"
		else:
			karsicari="select cari_kod from tblcasabit"
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		if modul=="c":
			sql=sql.replace('@chgun@',str(chgun))
		sql=sql.replace('@iscari@',iscari)
		sql=sql.replace('@karsicari@',karsicari)
		if(tarih!=""):
			tarih=self.tarih_format(tarih)
			sql=sql.replace('@tarih_kriter@',"tarih='"+tarih+"' and ")
		else:
			sql=sql.replace('@tarih_kriter@',"")
		if(fisno!=""):
			sql=sql.replace('@fisno_kriter@',"fno='"+fisno+"' and")
		else:
			sql=sql.replace('@fisno_kriter@',"")
		if(islemturu!=""):
			sql=sql.replace('@islem_kriter@',"islem_turu='"+islemturu[0]+"' and")
		else:
			sql=sql.replace('@islem_kriter@',"")
		if(hartip!=""):
			sql=sql.replace('@hartip_kriter@',"ftip='"+hartip[0]+"' and")
		else:
			sql=sql.replace('@hartip_kriter@',"")
		if(irsdurum!=""):
			sql=sql.replace('@irs_kriter@',"irs='"+irsdurum+"' and")
		else:
			sql=sql.replace('@irs_kriter@',"")
		#14:35 09.01.2015
		#if islemturu=='K':
		if islemturu in ['K','B']:
			sqldosyak='./altyapi/sql/kasa_devir.sql'
			sqlk=codecs.open(sqldosyak,'r','iso-8859_9').read()
			sqlk=sqlk.replace('@kaynak@',iscari)
			sqlk=sqlk.replace('@tarih@',tarih)
			codecs.open("sql_cikti/kasa_devir_data.sql",'w','iso-8859_9').write(sqlk+"\n")
			rapork=statikrapor()
			topsutk=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
			rapork.sql(sqlk,alt=1)	
			devir_rapor=rapork.getHtml()
		if(sonuc=='html'):
			rapor=statikrapor()
			topsut=[5,6,-1,-1,-1,-1,-1,-1,-1,-1,-1]
			#14:35 09.01.2015
			#if islemturu=='K':
			if islemturu in ['K','B']:
				topsut=[3,4,5,-1,-1,-1,-1,-1,-1,-1,-1]
			codecs.open("sql_cikti/carihar_sorgu_data.sql",'w','iso-8859_9').write(sql+"\n")
			rapor.sql(sql,rapbas="rapor",alt=1,link='?fkod',yukle="cahar_yukle",sil="cahar_sil",topsut=topsut)	
			if modul=="c":
				rapor_yas=self.cari_yaslandirma(kcari,mcari,tarih="")
			return rapor.getHtml()+"<br>"+devir_rapor+"<br>"+rapor_yas
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows
	
	def cari_sorgu(self,kriter,aranan,rtip="html"):
		sqldosya='./altyapi/sql/cari_sorgu.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kriter@',kriter)
		sql=sql.replace('@aranan@',aranan)
		#salt sql data icin
		#sqldosyadata='./altyapi/sql/sthar_bilgi_data.sql'
		codecs.open("sql_cikti/cari_sorgu_data.sql",'w','iso-8859_9').write(sql)
		if rtip=="html":
			rapor=statikrapor()
			rapor.sql(sql,alt=2)	
			return rapor.getHtml()
		else:
			rows=self.calistir(sql)
			return rows
			
	def cari_guncelle(self,cari,mod):
		if(mod=='s'):
			sql=open('./altyapi/sql/cari_sil.sql','r').read()
		if(mod=='g'):
			sql=open('./altyapi/sql/cari_guncelle.sql','r').read()
		if(mod=='y'):
			sql=open('./altyapi/sql/cari_ekle.sql','r').read()
		sql=sql.replace('@kod@',cari.kod)
		if(mod=='s'):
			return self.calis(sql)

		sql=sql.replace('@isim@',cari.isim)	
		sql=sql.replace('@adres@',cari.adres)	
		sql=sql.replace('@tel@',cari.tel)
		sql=sql.replace('@tel2@',cari.tel2)	
		sql=sql.replace('@vergino@',cari.vergino)	
		sql=sql.replace('@vergiyer@',cari.vergiyer)
		sql=sql.replace('@eposta@',cari.eposta)	
		sql=sql.replace('@cari_tip@',cari.cari_tip)	
		sql=sql.replace('@iban@',cari.iban)	
		sql=sql.replace('@vade_gunu@',str(cari.vade_gunu))
		sql=sql.replace('@grupkod@',cari.grupkod)
		sql=sql.replace('@kod1@',cari.kod1)
		return self.calis(sql)
	
	def sthar_detay(self,fkod,sonuc='dizi',tasarim=1):
		if(tasarim==1):
			sqldosya='./altyapi/sql/sthar_detay.sql'
		if(tasarim==2):
			sqldosya='./altyapi/sql/sthar_detay2.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@fkod@',str(fkod))
		if(sonuc=='html'):
			rapor=statikrapor()
			rapor.sql(sql,alt=2)	
			return rapor.getHtml()
			'''
			rapor=statikrapor()
			#topsut=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,10,11]
			rapor.sql(sql,alt=1,link='/incno?incno',yukle="stk_yukle",sil="stk_sil",topsut=[])	
			return rapor.getHtml()
			'''
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows
		print "sorgu sonuc tipi secilmedi"
		return None
	
	def sthar_detay_baslik(self,fkod,link="",sonuc='dizi',tasarim=1):
		if(tasarim==1):
			sqldosya='./altyapi/sql/sthar_detay_baslik.sql'
		if(tasarim==2):
			sqldosya='./altyapi/sql/sthar_detay_baslik2.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@fkod@',str(fkod))
		if(sonuc=='html'):
			rapor=statikrapor()
			rapor.sql(sql,alt=2,link=link)	
			return rapor.getHtml()
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows[0]
		print "sorgu sonuc tipi secilmedi"
		return None
	
	def fatura_irsler(self,fkod,sonuc='dizi'):
		sqldosya='./altyapi/sql/fatura_irsler.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@fkod@',str(fkod))
		if(sonuc=='html'):
			rapor=statikrapor()
			rapor.sql(sql,alt=2)	
			return rapor.getHtml()
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows
		print "sorgu sonuc tipi secilmedi"
		return None
	
	def fatura_kayitbilgi(self,fkod,sonuc='dizi'):
		sqldosya='./altyapi/sql/fatura_kayitbilgi.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@fkod@',str(fkod))
		if(sonuc=='html'):
			rapor=statikrapor()
			rapor.sql(sql,alt=2)	
			return rapor.getHtml()
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows
		print "sorgu sonuc tipi secilmedi"
		return None
	
	def stknoYfkod(self,stkno):
		try:
			gecde=stkno.split('.stk')[0]
			fkod=gecde.split('fkod')[1]
			if(fkod):
				return fkod
		except:
			return None
			
	def stk_fiyatdeg(self,stkno,bftip):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		stkharlar=self.stk_al(stkno)
		stknopar=stkno.split('@')
		if len(stknopar)>1:
			kaynak=stknopar[0]
			hedef=stknopar[1]
		else:
			kaynak=""
			hedef=""
		for stkhar in stkharlar:
			stkod=stkhar[1]
			stok=self.stok(stkod)
			if(bftip=='3'):
				bf=stok.satis_fiat3
			if(bftip=='2'):
				bf=stok.satis_fiat2
			if(bftip=='1'):
				bf=stok.satis_fiat1
			if(bftip=='4'):
				bf=stok.alis_fiat1
			if(bftip=='5'):
				bf=stok.alis_fiat2
			if(bftip=='6'):
				bf=stok.alis_fiat3	
			
			if(bftip=='7'):
				bf=self.sonalim_bf(kaynak,hedef,stok.kod)	
			if(bftip=='8'):
				bf=self.sonsatis_bf(kaynak,hedef,stok.kod)	
			
			with con:    
				cur = con.cursor()    
				cur.execute("update stoklist set bf="+str(bf)+",tutar=miktar*"+str(bf)+" where stkod='"+stkod+"' and stoklistno='"+str(stkno)+"'")
		return "tamam"	
		
	def sth_ekle(self,kaynak,fisno,tarih,stkod,miktar,olcubr,bf):	
		now = datetime.datetime.now()
		tblsthar=Tblsthar()
		tblsthar.stok_kodu=stkod
		tblsthar.fisno=fisno
		tblsthar.miktar=miktar
		tblsthar.tarih=self.tarih_format(tarih)
		tblsthar.bf=bf
		tblsthar.olcubr=olcubr
		tblsthar.nf=tblsthar.bf
		tblsthar.kaynak=kaynak
		tblsthar.hedef="sth_servis"
		tblsthar.kdvoran=self.stok(tblsthar.stok_kodu).kdv_orani
		tblsthar.finckeyno=0
		tblsthar.kayittarihi=now
		gc="G"
		if(float(tblsthar.miktar)<0):
			gc="C"
			tblsthar.miktar=-1*float(tblsthar.miktar)
		tblsthar.ftip=gc
		stharsql=""
		sqlsthar=open('./altyapi/sql/tblsthar_ekle.sql','r').read()
		stharsql=tblsthar.ekle(sqlsthar)
		#print stharsql
		self.calistir(stharsql)
		return "tamam"
	
	def sth_sil(self,incno):
		sql=""
		sql=open('./altyapi/sql/sthar_sil.sql','r').read()
		sql=sql.replace('@harkod@',str(incno))
		self.calistir(sql)
		return "tamam"
	
	def sth_bilgi(self,merkez,fisno,sonuc='dizi',tasarim=1):
		fkod=self.fkod_al(fisno,merkez)
		if(tasarim==1):
			sqldosya='./altyapi/sql/sthar_detay.sql'
		if(tasarim==2):
			sqldosya='./altyapi/sql/sthar_detay2.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@fkod@',str(fkod))
		if(sonuc=='html'):
			rapor=statikrapor()
			#topsut=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,10,11]
			rapor.sql(sql,alt=1,link='/incno?incno',yukle="sth_yukle",sil="sth_sil",topsut=[])	
			return rapor.getHtml()	
		if(sonuc=='dizi'):
			rows=self.calistir(sql)
			return rows
		print "sorgu sonuc tipi secilmedi"
		return None
	
	def sthlar_al(self,fkod):
		sql=open('./altyapi/sql/sthlar_al.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		rows=self.calistir(sql)
		if(rows):
			return rows
		else:
			return None
	
	def nakli_agirlik(self,stkno):
		urunler=self.stk_al(stkno)
		topagr=0.0
		for urun in urunler:
			topagr+=self.stok(urun[1]).birim_agirlik*urun[3]
		return topagr
	def fat_sth_islem(self,tblsthar,mod='e'):
		now = datetime.datetime.now()
		fatura=self.fatura_yukle(tblsthar.finckeyno)
		kdvdurum=fatura.kdvdurum
		stok=self.stok(tblsthar.stok_kodu)
		kdvsi=stok.kdv_orani
		#sthar tablosu icin kayit nesnesinin olusturulmasi
		tblsthar.fisno=fatura.fno
		tblsthar.tarih=fatura.tarih
		tblsthar.kaynak=fatura.kaynak
		tblsthar.hedef=fatura.hedef
		tblsthar.kayittarihi=now
		tblsthar.vadetarihi=fatura.vadetarihi
		tblsthar.ftip=fatura.ftip
		tblsthar.duzeltmetarihi=now
		tblsthar.takipkod=fatura.takipkod
		tblsthar.kdvoran=kdvsi
		tblsthar.olcubr=stok.olcu_br1
		tblsthar.miktar=float(tblsthar.miktar)
		fiyat=tblsthar.bf
		fiyat=float(fiyat)
		ntop=0
		gtop=0
		bf=0.0
		nf=0.0
		nf=decimal.Decimal("%.8g" % nf)
		bf=decimal.Decimal("%.8g" % bf)
		if(kdvdurum=="H"):
			nf=decimal.Decimal("%.8g" % fiyat)
			satirkdv=decimal.Decimal("%.8g" % (nf+(nf*(kdvsi/100))))
			bf=nf
			kdvdahilmi="H"
			nttr=nf*(decimal.Decimal("%.8g" % tblsthar.miktar))	
			gttr=bf*(decimal.Decimal("%.8g" % tblsthar.miktar))*(kdvsi+100)/100
		else:
			kdvdurum="E"
			bf=decimal.Decimal("%.8g" % fiyat)
			satirkdv=decimal.Decimal("%.8g" % (bf-(bf/((kdvsi/100)+1))))
			nf=(decimal.Decimal("%.8g" % fiyat)*100)/(kdvsi+100)
			nf=decimal.Decimal("%.8g" % nf)
			nttr=nf*(decimal.Decimal("%.8g" % tblsthar.miktar))	
			gttr=bf*(decimal.Decimal("%.8g" % tblsthar.miktar))
		
		satirkdv=decimal.Decimal("%.8g" %  satirkdv)*decimal.Decimal("%.8g" % tblsthar.miktar)
		satirkdv=decimal.Decimal("{:10.2f}".format(satirkdv))	
	
		if(kdvsi==1.00):
			if mod=='e':fatura.kdv1top+=satirkdv
			if mod=='s':fatura.kdv1top-=satirkdv
		if(kdvsi==8.00):
			if mod=='e':fatura.kdv8top+=satirkdv
			if mod=='s':fatura.kdv8top-=satirkdv
		if(kdvsi==18.00):
			if mod=='e':fatura.kdv18top+=satirkdv
			if mod=='s':fatura.kdv18top-=satirkdv
		
		tblsthar.nf=nf
		tblsthar.bf=bf
			
		ntop=nttr.quantize(decimal.Decimal(10) ** -2)
		gtop=gttr.quantize(decimal.Decimal(10) ** -2)
		gtop=decimal.Decimal("{:10.2f}".format(gtop))
		ntop=decimal.Decimal("{:10.2f}".format(ntop))
		if mod=='e':fatura.khtutar+=ntop
		if mod=='s':fatura.khtutar-=ntop
		if mod=='e':fatura.kdtutar+=gtop
		if mod=='s':fatura.kdtutar-=gtop
		if mod=='e':fatura.kdvtoplam+=gtop-ntop
		if mod=='s':fatura.kdvtoplam-=gtop-ntop
		if mod=='e':fatura.geneltoplam+=gtop
		if mod=='s':fatura.geneltoplam-=gtop
		if mod=='e':sira=self.fis_sonsira(fatura.fno)+1
		if mod=='s':sira=self.fis_sonsira(fatura.fno)-1
		fatura.fatkalem_adedi=sira
		tblsthar.sira=sira
		if mod=='e':#self.sth_ekle(tblsthar.kaynak,tblsthar.fisno,tblsthar.tarih,tblsthar.stok_kodu,tblsthar.miktar,tblsthar.olcubr,tblsthar.bf)
			stharsql=""
			sqlsthar=open('./altyapi/sql/tblsthar_ekle.sql','r').read()
			stharsql=tblsthar.ekle(sqlsthar)
			self.calistir(stharsql)
		if mod=='s':self.sth_sil(tblsthar.incno)
		sqlfatura=codecs.open('./altyapi/sql/tblfatura_ekle.sql','r','iso-8859_9').read()
		self.faturaust_sil(fatura.inckeyno)
		fatura.inckeyno=tblsthar.finckeyno
		faturasql=fatura.ekle(sqlfatura)
		#print faturasql
		self.calistir(faturasql)
		return "tamam"
	
	def chvade_duzen(self,fkod,yenivade):
		sql=""
		yenivade=self.tarih_format(yenivade)
		sql=open('./altyapi/sql/chvade_duzen.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		sql=sql.replace('@yenivade@',str(yenivade))
		self.calis(sql)
		return "tamam"
	
	def spr_fisler(self,merkez):
		sql=open('./altyapi/sql/spr_fisler.sql','r').read()
		sql=sql.replace('@merkez@',str(merkez))
		rows=self.calistir(sql)
		fisler=[]
		if(rows):
			return rows
		else:
			return None
	
	def fis_sonsira(self,fisno):
		sql=open('./altyapi/sql/fis_sonsira.sql','r').read()
		sql=sql.replace('@fisno@',str(fisno))
		rows=self.calistir(sql)
		sira=rows[0][0]
		if(sira is not None):
			return sira
		else:
			return 0
	
	def fatura_kdvdurum(self,fkod):
		sql=open('./altyapi/sql/fatura_kdvdurum.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		rows=self.calistir(sql)
		durum=rows[0][0]
		if(durum is not None):
			return durum
		else:
			return 'X'
	
	def fkod_al(self,fisno,merkez):
		sql=open('./altyapi/sql/fkod_al.sql','r').read()
		sql=sql.replace('@fisno@',str(fisno))
		sql=sql.replace('@merkez@',str(merkez))
		rows=self.calistir(sql)
		if(rows is not None):
			fkod=rows[0][0]
			return fkod
		else:
			return -1
	
	def faturalama(self,fatura,kayitmodu):
		#fatura guncelleme stkno uzerinden kontrol edilir.eski silinir,yeni degerle kayit yapilir.
		islem_turu=""
		eski_fkod=""
		if(kayitmodu=='g'):
			#guncfkod=self.stknoYfkod(fatura.stharlistno)
			if(fatura.fkod):
				print fatura.fkod+" nolu fatura guncellenmek uzere silindi."
				eski_fkod=fatura.fkod
				self.fatura_sil(fatura.fkod)
		fatura.stharlist=self.stharlist_al(fatura.stharlistno)
		fatura.tarih=self.tarih_format(fatura.tarih)
		fatura.vadetarih=self.tarih_format(fatura.vadetarih)
		sira=0
		ftip=''
		ntop=0
		gtop=0
		kdv1top=decimal.Decimal(0.0)
		kdv8top=decimal.Decimal(0.0)
		kdv18top=decimal.Decimal(0.0)
		now = datetime.datetime.now()
		stharsql=""
		sqlsthar=open('./altyapi/sql/tblsthar_ekle.sql','r').read()
		finckeyno=0
		
		ftip=fatura.fattip
		cari=self.cari(fatura.hedef)
		#fatura vadesi guiden geldii icin simdilik iptal edildi.
		#vadesi=cari.vadegunu
		caritip=cari.cari_tip
		fatura.caritip=caritip
		
		if(fatura.islem =='F'):
			print "kalemler ekleniyor"
			ax=datetime.datetime.now()
			for sthar in fatura.stharlist:
				sira+=1
				stok=self.stok(sthar.stkod)
				if stok is None:
					print "mak.faturalama() tanimsiz stok",sthar.stkod
					return "olumsuz"
				kdvsi=stok.alis_kdv_kodu
				if ftip=='C':	
					kdvsi=stok.kdv_orani
				#son alimyer ekleme
				'''oto_alim=open('./altyapi/sql/oto_fiyat_guncelle.sql','r').read()
				sql=sql.replace('@stkod@',str(sthar.stkod))
				sql=sql.replace('@hedef@',str(fatura.hedef))
				self.calis(sql)
				'''
				kdvdurum=fatura.kdvdurum
				#sthar tablosu icin kayit nesnesinin olusturulmasi
				tblsthar=Tblsthar()
				tblsthar.stok_kodu=stok.kod
				tblsthar.fisno=fatura.fisno
				tblsthar.miktar=sthar.miktar
				fatura.toplam_mik+=tblsthar.miktar
				if (stok.isim!=sthar.stokad):
					tblsthar.aciklama=sthar.stokad
				tblsthar.tarih=fatura.tarih
				tblsthar.duzeltmetarihi=now
				tblsthar.takipkod=fatura.takipkod
				tblsthar.sira=sira
				tblsthar.kdvoran=kdvsi
				tblsthar.vadetarihi=fatura.vadetarih
				tblsthar.olcubr=stok.olcu_br1
				fiyat=sthar.bf
				fiyat=float(fiyat)
				bf=0.0
				nf=0.0
				nf=decimal.Decimal("%.8g" % nf)
				bf=decimal.Decimal("%.8g" % bf)
				if(kdvdurum=="H"):
					nf=decimal.Decimal("%.8g" % fiyat)
					satirkdv=decimal.Decimal("%.8g" % ((nf*(kdvsi/100))))
					bf=nf*(kdvsi+100)/100
					nttr=nf*(decimal.Decimal("%.8g" % sthar.miktar))	
					gttr=nf*(decimal.Decimal("%.8g" % sthar.miktar))*(kdvsi+100)/100
				else:
					kdvdurum="E"
					bf=decimal.Decimal("%.8g" % fiyat)
					satirkdv=decimal.Decimal("%.8g" % (bf-(bf/((kdvsi/100)+1))))
					nf=(decimal.Decimal("%.8g" % fiyat)*100)/(kdvsi+100)
					nf=decimal.Decimal("%.8g" % nf)
					nttr=nf*(decimal.Decimal("%.8g" % sthar.miktar))	
					gttr=bf*(decimal.Decimal("%.8g" % sthar.miktar))
				
				satirkdv=decimal.Decimal("%.8g" %  satirkdv)*decimal.Decimal("%.8g" % sthar.miktar)
				satirkdv=decimal.Decimal("{:10.2f}".format(satirkdv))	
			
				if(kdvsi==1.00):kdv1top+=satirkdv
				if(kdvsi==8.00):kdv8top+=satirkdv
				if(kdvsi==18.00):kdv18top+=satirkdv
				
				tblsthar.nf=nf
				tblsthar.bf=bf
				tblsthar.kaynak=fatura.kaynak
				tblsthar.hedef=fatura.hedef
				tblsthar.finckeyno=999999
				tblsthar.kayittarihi=now
				tblsthar.ftip=ftip	
				#bir hareket icin tblsthar vt nesnesinini sqlinin olusturulma
				stharsql+=tblsthar.ekle(sqlsthar)
				ntop+=nttr.quantize(decimal.Decimal(10) ** -2)
				gtop+=gttr.quantize(decimal.Decimal(10) ** -2)
			ay=datetime.datetime.now()
			print sira,"kalem eklendi.",(ay-ax).total_seconds(),"sn"
			gtop=decimal.Decimal("{:10.2f}".format(gtop))
			ntop=decimal.Decimal("{:10.2f}".format(ntop))
		cari1=self.cari(fatura.kaynak)
		cari2=self.cari(fatura.hedef)
		islem_turu=fatura.islem
		
		if(kayitmodu=='g'):
			finckeyno=eski_fkod
		if(kayitmodu=='y'):
			finckeyno=self.finckeyno_al()
		if(kayitmodu=='sayim'):
			finckeyno=-1
		
		if(fatura.islem !='F'):
			ntop=fatura.tutar
			if ntop<=0:
				fatura.fattip='C'
				ntop=ntop*-1
			else:
				fatura.fattip='G'
			gtop=ntop
			#vadesi=0
			kdvdurum="E"
			sira=0
			kdv1top=0
			kdv8top=0
			kdv18top=0
			if(fatura.fisno==""):
				fatura.fisno=islem_turu+fatura.fattip+str(finckeyno)
		fatura.ntop=ntop
		fatura.gtop=gtop
		fatura.kalemsay=sira
		fatura.kdv1top=kdv1top
		fatura.kdv8top=kdv8top
		fatura.kdv18top=kdv18top
		if(kayitmodu=='sayim'):
			finckeyno=0
		fatura.fincno=finckeyno
		fatura.islem_turu=islem_turu
		stharsql=stharsql.replace("999999",str(finckeyno))
		print "sql0"
		self.calistir(stharsql)
		print "sql1"
		kayitsonuc=self.faturalama2(fatura=fatura)
		return kayitsonuc
		
	def faturalama2(self,fatura):
		#sqlfatura=open('./altyapi/sql/tblfatura_ekle.sql','r').read()
		sqlfatura=codecs.open('./altyapi/sql/tblfatura_ekle.sql','r','iso-8859_9').read()
		vadesay=fatura.vadesay
		ntop=fatura.ntop
		gtop=fatura.gtop
		sira=fatura.kalemsay
		tblfatura=Tblfatura()
		tblfatura.kaynak=fatura.kaynak
		tblfatura.ftip=fatura.fattip
		tblfatura.fno=fatura.fisno
		tblfatura.hedef=fatura.hedef
		tblfatura.tarih=fatura.tarih
		tblfatura.khtutar=ntop
		tblfatura.kdtutar=gtop
		tblfatura.kdvtoplam=gtop-ntop
		tblfatura.vadetarihi=fatura.vadetarih
		tblfatura.cari_tip=fatura.caritip
		tblfatura.islem_turu=fatura.islem_turu
		tblfatura.med=fatura.med
		tblfatura.irs=fatura.irs
		tblfatura.kdvdurum=fatura.kdvdurum
		tblfatura.fatkalem_adedi=sira
		tblfatura.toplam_mik=fatura.toplam_mik
		#toplam_mik de olacak burada
		tblfatura.geneltoplam=gtop
		tblfatura.kayityapankul=fatura.kaydeden
		tblfatura.duzeltmeyapankul=fatura.kaydeden
		tblfatura.kayittarihi=datetime.datetime.now()
		tblfatura.duzeltmetarihi=datetime.datetime.now()
		tblfatura.aciklama=fatura.aciklama
		tblfatura.takipkod=fatura.takipkod
		tblfatura.inckeyno=fatura.fincno
		tblfatura.kdv1top=fatura.kdv1top
		tblfatura.kdv8top=fatura.kdv8top
		tblfatura.kdv18top=fatura.kdv18top
		
		vadesay=int(vadesay)
		if(vadesay<1):
			vadesay=1
		if(vadesay>=1):
			ortvade=round(float(gtop)/int(vadesay),3)
			for i in range(vadesay):
				tblfatura.geneltoplam=ortvade
				if(i>0):
					tblfatura.inckeyno=self.finckeyno_al()
				faturasql=tblfatura.ekle(sqlfatura)
				self.calistir(faturasql)
		return "tamam"
		
	def ust_guncelle(self,fatura):
		fatura.vadetarih=self.tarih_format(fatura.vadetarih)
		fatura.tarih=self.tarih_format(fatura.tarih)
		#sql=open('./altyapi/sql/ust_guncelle.sql','r').read()
		sql=codecs.open('./altyapi/sql/ust_guncelle.sql','r','iso-8859_9').read()
		sql=sql.replace('@fno@',str(fatura.fisno))
		sql=sql.replace('@fkod@',str(fatura.fkod))
		sql=sql.replace('@tarih@',str(fatura.tarih))
		sql=sql.replace('@vadetarih@',str(fatura.vadetarih))
		sql=sql.replace('@tutar@',str(fatura.tutar))
		sql=sql.replace('@aciklama@',fatura.aciklama)
		sql=sql.replace('@med@',str(fatura.med))
		sql=sql.replace('@irs@',str(fatura.irs))
		sql=sql.replace('@hedef@',str(fatura.hedef))
		sonuc=self.calis(sql)
		
		vade_kont=self.vadeleme_kontrol(fatura.fkod)
		if vade_kont!=0.0:
			return "tutar uyusmazligi var-kayit yapildi."
		return sonuc
		
	def vadeleme_kontrol(self,fkod):
		sql=open('./altyapi/sql/vadeleme_kontrol.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		rows=self.calistir(sql)
		if(rows):
			vadelitop=float(rows[0][0])
			gertop=float(rows[0][1])
			return round(vadelitop-gertop,3)
		else:
			return "vadelenecek kriter yok!"
	
	def fatisko_yap(self,stkno,fatisko,kdvdur):
		fatisko=fatisko.replace(',','.')
		if self.stk_fsb_al(stkno) is None:
			return None
		icra=1
		if(fatisko[0]=='%'):
			fatiskoran=fatisko[1:]
			icra=(100-float(fatiskoran))/100
		else:	
			fatisko=float(fatisko)
			tutarfsb=self.stk_fsb_al(stkno)
			if(kdvdur=='E'):
				tutarsda=float(tutarfsb[0].split('=')[1])
				icra=(tutarsda-fatisko)/tutarsda
			else:
				tutarsha=float(tutarfsb[1].split('=')[1])
				icra=(tutarsha-fatisko)/tutarsha
		return self.stk_iskonto(stkno,icra)
	
	def satisko_icra(self,bf,satisko):
		satiskolar=satisko.split('-')
		for satisko in satiskolar:
			satisko=float(str(satisko).replace(',','.'))
			icra=(100-float(satisko))/100
			bf=float(bf)*icra
		return round(bf,2)
	
	def fatura_ustbilgi(self,fkod):
		#sql=open('./altyapi/sql/fatura_ustbilgi.sql','r').read()
		sql=codecs.open('./altyapi/sql/fatura_ustbilgi.sql','r','iso-8859_9').read()
		sql=sql.replace('@fkod@',str(fkod))
		rows=self.calistir(sql)
		data=[]
		for rowx in rows:
			data.append(rowx[0])
			data.append(rowx[1])
			data.append(rowx[2][0])
			data.append(rowx[3])
			data.append(rowx[4])
			data.append(rowx[5])
			kaynak=rowx[6]
			kaynakad=self.cari(kaynak).isim
			data.append(kaynakad+"@"+kaynak)
			hedef=rowx[7]
			hedefad=self.cari(hedef).isim
			data.append(hedefad+"@"+hedef)
			data.append(rowx[8])
			data.append(float(rowx[9]))
			data.append(rowx[10])
			data.append(rowx[11])
			data.append(float(rowx[12]))
			data.append(float(rowx[13]))
			data.append(float(rowx[14]))
			data.append(float(rowx[15]))
			data.append(float(rowx[16]))
			data.append(float(rowx[17]))
			data.append(float(rowx[18]))
			data.append(rowx[19])
			data.append(rowx[20])
			data.append(rowx[21])
			data.append(float(rowx[22]))
			data.append(rowx[23])
			data.append(rowx[24])
		return data
	
	def fatura_bilgi(self,kimlik):
		sqldosya='./altyapi/sql/fatura_bilgi.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@kimlik@',str(kimlik))
		rows=self.calistir(sql)
		return rows
		#salt sql data icin
		#sqldosyadata='./altyapi/sql/sthar_bilgi_data.sql'
		#codecs.open(sqldosyadata,'w','iso-8859_9').write(sql)
		'''print sql
		rapor=statikrapor()
		rapor.sql(sql)	
		return rapor.getHtml()'''
	
	def fatura_sil(self,kimlik):
		sql=open('./altyapi/sql/fatura_sil.sql','r').read()
		sql=sql.replace('@kimlik@',str(kimlik))
		sonuc=self.calis(sql)
		if(sonuc=="tamam"):
			return sonuc
		else:
			return "fatura silinirken vt hatasi"
	def faturaust_sil(self,kimlik):
		sql=open('./altyapi/sql/faturaust_sil.sql','r').read()
		sql=sql.replace('@kimlik@',str(kimlik))
		sonuc=self.calis(sql)
		if(sonuc=="tamam"):
			return sonuc
		else:
			return "fatura silinirken vt hatasi"
	def fiyat_guncelle(self,fkod):
		sql=open('./altyapi/sql/fiyat_guncelle.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		return self.calis(sql)
	
	def fisno_kontrol(self,fisno):
		sql=open('./altyapi/sql/fisno_kontrol.sql','r').read()
		sql=sql.replace('@fisno@',str(fisno))
		rows=self.calistir(sql)
		if(rows is None):
			return "yok"
		else:
			return "var"
	
	def fisno_al(self,fkod):
		sql=open('./altyapi/sql/fisno_al.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		rows=self.calistir(sql)
		if(rows is None):
			return "yok"
		else:
			return rows[0][0]
	
	def fisno_serial(self,onek,caritip):
		sql=open('./altyapi/sql/fisno_serial.sql','r').read()
		sql=sql.replace('@onek@',str(onek))
		sql=sql.replace('@caritip@',str(caritip))
		rows=self.calistir(sql)
		for rowx in rows:
			if(rowx[0] is not None):
				mvcfis=rowx[0]
				mvcfis=mvcfis.split(onek)[1]
				sksm=int(mvcfis)
				sksm1=sksm+1
				mvcfis=mvcfis.replace(str(sksm),str(sksm1))
				yenifis=onek+mvcfis
				#print "yeni:",yenifis
				return yenifis
			else:
				mvcfis=onek
				for i in range(len(onek),9):
					mvcfis+='0'
				mvcfis+='1'
				return mvcfis
	def fisno_serial2(self,onek,gctur):
		print onek,gctur
		onek=onek.upper()
		sql=open('./altyapi/sql/fisno_serial2.sql','r').read()
		sql=sql.replace('@onek@',str(onek))
		sql=sql.replace('@gctur@',str(gctur))
		rows=self.calistir(sql)
		for rowx in rows:
			if(rowx[0] is not None):
				mvcfis=rowx[0]
				mvcfis=mvcfis.split(onek)[1]
				sksm=int(mvcfis)
				sksmy=sksm+1
				eskifissy=str(sksm)
				ek=""
				if len(str(sksm))<len(str(sksmy)):
					fark=len(str(sksmy))-len(str(sksm))
					if fark==1:
						ek="0"
					if fark==2:
						ek="00"
				mvcfis=mvcfis.replace(ek+eskifissy,str(sksmy))
				yenifis=onek+mvcfis
				return yenifis
			else:
				mvcfis=onek
				for i in range(len(onek),9):
					mvcfis+='0'
				mvcfis+='1'
				return mvcfis
	
	def fatura_islemturu(self,fkod):
		sql=open('./altyapi/sql/fatura_islemturu.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		rows = self.calistir(sql)
		if(rows):
			return rows[0][0]
		else:
			return None
	
	def spr_yukle(self,sprno):
		sql=open('./altyapi/sql/spr_yukle.sql','r').read()
		sql=sql.replace('@sprno@',str(sprno))
		sprhar=[]
		sprhar=self.calistir(sql)
		return sprhar
	
	def fatura_yukle(self,fkod):
		tblfatura=Tblfatura()
		sql=open('./altyapi/sql/fatura_yukle.sql','r').read()
		sql=sql.replace('@fkod@',str(fkod))
		fatura=self.calistir(sql)
		tblfatura.yukle(fatura[0])
		#for attr, value in tblfatura.__dict__.iteritems():
		#	print attr,value
		return tblfatura
	
	def sth_yukle(self,incno):
		sthar=Tblsthar()
		sql=open('./altyapi/sql/sth_yukle.sql','r').read()
		sql=sql.replace('@incno@',str(incno))
		row=self.calistir(sql)
		sthar.yukle(row[0])
		#for attr, value in tblfatura.__dict__.iteritems():
		#	print attr,value
		return sthar
	
	def finckeyno_turet(self):
		finckey=0
		finckey=randint(0,999999)
		if(self.finckeyno_kontrol(finckey)=="yok"):
			return finckey
		else:
			self.finckeyno_turet()
	
	def finckeyno_al(self):
		sql=open('./altyapi/sql/finckeyno_al.sql','r').read()
		rows = self.calistir(sql)
		maxfinc=rows[0][0]
		if(type(maxfinc) is long):	
			maxfinc=maxfinc+1
		else:
			maxfinc=1
		return maxfinc
	def finckeyno_kontrol(self,finckeyno):
		sql=open('./altyapi/sql/finckeyno_kontrol.sql','r').read()
		sql=sql.replace('@finckeyno',str(finckeyno))
		rows = self.calistir(sql)
		if(rows):
			return "var"
		else:
			return "yok"
	
	def stharlist_al(self,stoklistno="xxx"):
		stharlist=[]
		con = lite.connect(self.stoklistvt)
		with con:    
			cur = con.cursor() 
			sql=open('./altyapi/sql/stharlist_al.sql','r').read()
			sql=sql.replace('@stoklistno',stoklistno)
			cur.execute(sql)
			rows = cur.fetchall()
			for row in rows:
				sthar=Stokhareket()
				sthar.sira=row[0]
				sthar.stkod=row[1]
				sthar.stokad=row[2]
				sthar.miktar=float(row[3])
				sthar.bf=float(row[4])
				sthar.tutar=sthar.miktar*sthar.bf
				sthar.stoklistno=row[6]
				stharlist.append(sthar)
		return stharlist
		
	def stharlist_goster(self,stoklistno="xxx"):
		stharlist=self.stharlist_al(stoklistno)
		for sthar in stharlist:
			sthar.goster()
	
	def stharYstk(self,fkod):
		stkno='fkod'+fkod+".stk"
		self.stk_sil(stkno)
		sqldosya='./altyapi/sql/sthar_detay.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@fkod@',fkod)
		rows=self.calistir(sql) 
		kdvdurum=self.fatura_kdvdurum(fkod)
		if kdvdurum=="X":
			return "olumsuz"
		if(rows):
			for sthar in rows:			
				fiat=""
				if kdvdurum=='H':
					fiat=sthar[5]
				else:
					fiat=sthar[6]
				stharyeni=(sthar[1],sthar[2],float(sthar[3]),float(fiat),float(sthar[7]),stkno)
				self.stk_ekle(stharyeni)
			return stkno
		return "olumsuz"
	
	def cogul_stkbir(self,fkodlar):
		#str(random.randrange(1,1000))
		#self.stk_sil(stkno)
		stkno=""
		for fkod in fkodlar:
			stkno+=str(fkod)+"@"
		stkno+=".irs"
		for fkod in fkodlar:
			sqldosya='./altyapi/sql/sthar_detay.sql'
			sql=codecs.open(sqldosya,'r','iso-8859_9').read()
			sql=sql.replace('@fkod@',str(fkod))
			rows=self.calistir(sql) 
			if(rows):
				for sthar in rows:			
					stharyeni=(sthar[1],sthar[2],float(sthar[3]),float(sthar[6]),float(sthar[7]),stkno)
					self.stk_ekle(stharyeni)
		return stkno
	
	def irs_topfat(self,fkodlar,tarih,fisno,kaydeden):
		yenifkod=self.finckeyno_al()
		sqlfatura=codecs.open('./altyapi/sql/tblfatura_ekle.sql','r','iso-8859_9').read()
		tblfatura=Tblfatura()
		
		for fkod in fkodlar:
			eskifat=self.fatura_ustbilgi(fkod)
			irsdurum=eskifat[11]
			if irsdurum=='E':
				print eskifat
				sqldosya='./altyapi/sql/sth_guncelle.sql'
				sql=codecs.open(sqldosya,'r','iso-8859_9').read()
				sql=sql.replace('@fkod@',str(fkod))
				sql=sql.replace('@yenifkod@',str(yenifkod))
				sql=sql.replace('@fisno@',str(fisno))
				self.calis(sql) 
				tblfatura.kaynak=eskifat[6].split('@')[1]
				tblfatura.ftip=eskifat[1]
				tblfatura.fno=fisno
				tblfatura.hedef=eskifat[7].split('@')[1]
				tblfatura.tarih=self.tarih_format(tarih)
				tblfatura.khtutar+=float(eskifat[12])
				tblfatura.kdtutar+=float(eskifat[13])
				tblfatura.kdvtoplam+=float(eskifat[17])
				tblfatura.vadetarihi=self.tarih_format(tarih)
				tblfatura.cari_tip=eskifat[19]
				tblfatura.islem_turu=eskifat[20]
				tblfatura.med='E'
				tblfatura.irs='H'
				tblfatura.kdvdurum=eskifat[21]
				tblfatura.fatkalem_adedi+=float(eskifat[18])
				tblfatura.toplam_mik+=eskifat[22]
				tblfatura.geneltoplam+=float(eskifat[9])
				tblfatura.kayityapankul=kaydeden
				tblfatura.duzeltmeyapankul=kaydeden
				tblfatura.kayittarihi=datetime.datetime.now()
				tblfatura.duzeltmetarihi=datetime.datetime.now()
				tblfatura.aciklama=""
				tblfatura.takipkod=""
				tblfatura.inckeyno=yenifkod
				tblfatura.kdv1top+=float(eskifat[14])
				tblfatura.kdv8top+=float(eskifat[15])
				tblfatura.kdv18top+=float(eskifat[16])
			else:
				return "irsaliye olmayan fis hatasi"
			#faturalasan irs in silinmesi
			self.faturaust_sil(fkod)
		faturasql=tblfatura.ekle(sqlfatura)
		self.calistir(faturasql)
		return "tamam"
	
	def sayim_hazirla(self,stkno,carikod,tarih,satis):
		self.stk_sadelestir(stkno)
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		saykod=str(randint(0,999999))
		if satis=="":
			satis="SAYIM_MODULU"
		#cikis_stkno=carikod+'@'+'CIKIS'+'@'+tarih.split()[0]+"@SYM"
		#giris_stkno=carikod+'@'+'GIRIS'+'@'+tarih.split()[0]+"@SYM"
		tarih=self.tarih_format(tarih)
		cikis_stkno=carikod+'@'+str(satis)+'@sayim'+saykod+'@CIKIS'+'@'+tarih.split()[0]+".sym"
		giris_stkno=carikod+'@'+str(satis)+'@sayim'+saykod+'@GIRIS'+'@'+tarih.split()[0]+".sym"
		#ustune yazmaz eski sayim hazir stksini siler.
		self.stk_sil(cikis_stkno)
		self.stk_sil(giris_stkno)
		sql=open('./altyapi/sql/stok_bakiye.sql','r').read()
		sql=sql.replace('@tarih@',tarih)
		sql=sql.replace('@merkez@',carikod)
		sqltemel=sql
		stharlar=self.stharlist_al(stkno)
		for sthar in stharlar:
			stokod=self.stok(sthar.stkod).kod
			stokad=sthar.stokad
			miktar=sthar.miktar
			bf=sthar.bf
			sql=sql.replace('@stokod@',stokod)
			netc=self.calistir(sql)
			bakiye=0.0
			if netc:
				gcbak=netc[0][0]
				if gcbak:
					bakiye=float(gcbak)
			satilan=bakiye-miktar
			tutar=round(bf*satilan,2)
			stkno=""
			if satilan!=0:
				if(satilan>0):
					stkno=cikis_stkno
				else:
					stkno=giris_stkno
					satilan=satilan*-1
					tutar=tutar*-1
				stokhar=(stokod,stokad,satilan,bf,tutar,stkno)
				self.stk_ekle(stokhar)
			sql=sqltemel
		return "tamam"
	
	def sayim_islet(self,stkno,kaydeden):
		now = datetime.datetime.now()
		stk=stkno.split('@')
		carikod=str(stk[0])
		yon=stk[1]
		tarih=stk[2]
		tarih=str(tarih)
		#tarih=tarih.replace('-','.')
		kdvsi=0.0
		sonek=str(randint(1000,9999))
		sayack="SAYIM"+carikod+'_'+sonek
		fisno="s_"+carikod+'_'+sonek
		sayim_fatura=Fatura()
		sayim_fatura.tarih=tarih
		sayim_fatura.vadetarih=tarih
		sayim_fatura.fisno=fisno
		if(yon=='GIRIS'):
			sayim_fatura.fattip="G"
			sayim_fatura.kaynak=carikod
			sayim_fatura.hedef="SAYIM_MODULU"
		else:
			sayim_fatura.fattip="C"
			sayim_fatura.kaynak=carikod
			sayim_fatura.hedef="SAYIM_MODULU"
		
		sayim_fatura.stharlistno=stkno
		sayim_fatura.kdvdurum="E"
		sayim_fatura.aciklama=sayack
		sayim_fatura.islem="F"
		sayim_fatura.tutar=0
		sayim_fatura.med='H'
		sayim_fatura.irs='H'
		sayim_fatura.kaydeden=kaydeden
		sayim_fatura.vadesay=1
		sayim_fatura.takipkod=''
		sonuc=self.faturalama(sayim_fatura,'sayim')
		sonuc2="sayim vt hatasi"
		if(sonuc=='tamam'):
			sonuc2=self.fatura_sil('0')
		return sonuc2
	
	def stok_sifirla(self,carikod,tarih,kriter="",aranan="",dizi=None):
		con = lite.connect(self.ayar_al('999','stoklist_db'))
		tarih=self.tarih_format(tarih)
		saykod=str(randint(0,999999))
		cikis_stkno=carikod+'@SAYIM_MODULU@sym'+saykod+'@CIKIS'+'@'+tarih.split()[0]+"@.stk"
		giris_stkno=carikod+'@SAYIM_MODULU@sym'+saykod+'@GIRIS'+'@'+tarih.split()[0]+"@.stk"
		self.stk_sil(cikis_stkno)
		self.stk_sil(giris_stkno)
		sql=open('./altyapi/sql/stok_bakiye.sql','r').read()
		sql=sql.replace('@tarih@',tarih)
		sql=sql.replace('@merkez@',carikod)
		sqltemel=sql
		eksorgu=""
		if(kriter!=""):
			eksorgu=" and sb."+kriter+" like '%"+str(aranan)+"%'"
		#ilgili stokların stok kodlarinin cekilmesi
		sqlbak=open('./altyapi/sql/stok_sifirla.sql','r').read()
		sqlbak=sqlbak.replace('@tarih@',tarih)
		sqlbak=sqlbak.replace('@carikod@',carikod)
		sqlbak=sqlbak.replace('@eksorgu@',eksorgu)
		stoklist=self.calistir(sqlbak)	
		#print stoklist,sqltemel,sqlbak
		if dizi:
			stoklist=dizi
		
		if(stoklist):
			for stokod in stoklist:
				stokod=stokod[0]
				stok=self.stok(stokod)
				bf=stok.satis_fiat3
				sql=sql.replace('@stokod@',stokod)
				netc=self.calistir(sql)
				print stokod
				if(netc):
					bakiye=netc[0][0]
					if bakiye:
						bakiye=float(str(bakiye))
					else:
						bakiye=0
				else:
					bakiye=0.0
				tutar=round(bf*bakiye,2)
				stkno=""
				if(bakiye>0):
					stkno=cikis_stkno
				else:
					bakiye=bakiye*-1
					tutar=tutar*-1
					stkno=giris_stkno
				stokhar=(stokod,stok.isim,bakiye,bf,tutar,stkno)
				with con:
					cur = con.cursor() 
					cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar)
				sql=sqltemel
			return "tamam"
		else:
			return "ilgili stokların hareket kaydı yok!"
	
	def dizin_cek(self,dizin='rapor',uzanti="",anadizin="altyapi"):
		dizinyol='./'+anadizin+'/'+dizin
		flst=[]
		lst=os.listdir(dizinyol)
		if uzanti=="":
			return sorted(lst)
		else:
			for dosya in lst:
				if dosya.endswith("."+uzanti):
					flst.append(dosya)
			return sorted(flst)
	
	def sql_al(self,dizin,dosya):
		sqlyol='./altyapi/'+dizin+'/'+dosya
		sql=codecs.open(sqlyol,'r','iso-8859_9').read()
		return sql
		
	def sql_kaydet(self,dizin,dosya,kod,kayitmodu):
		sqlyol='./altyapi/'+dizin+'/'+dosya
		try:
			codecs.open(sqlyol,"w",'iso-8859_9').write(kod)
			return "tamam"
		except Exception,e: 
			print str(e)
			return "sql kayit hatasi:sorunlu yol"
		
	def param_guncelle(self,dosya,paramlar,dizin='rapor'):
		sqlyol='./altyapi/'+dizin+'/'+dosya
		prm=""
		param=paramlar.split('set ')
		for par in param:
			if par!="":
				prm+="set "+par+";"+"\n"	
		kod=codecs.open(sqlyol,'r','iso-8859_9').read()
		oz=kod.split('#sql')[1]
		yenikod=prm+oz
		print yenikod
		return yenikod
		
	def rapor_paramlar(self,dosya,dizin='rapor'):
		sqlyol='./altyapi/'+dizin+'/'+dosya
		paramlar=""
		try:
			kod=codecs.open(sqlyol,'r','iso-8859_9').read()
			kod=kod.split('#sql')[0]
			kod=kod.split(';')
			for kodsat in kod:
				kodsat=kodsat.lower()
				kodsat=kodsat.strip()
				if kodsat.startswith("set ") or kodsat.startswith("#"):
					paramlar+=kodsat+"\n"
			return paramlar
		except Exception,e: 
			print str(e)
	
	def etoYstk(self,dosya):
		data=[]
		stkno=dosya.split("/")[1]+".stk"
		self.stk_sil(stkno)
		jsondata=open(dosya,"r").read()
		data=json.loads(jsondata)
		print data
		sayac=0
		rapor=""
		for dat in data:
			if sayac!=0:
				stkod=str(dat[0])
				stkad=str(dat[1])
				if stkod=="":
					stkod="---"
				if stkad=="":
					stkad="***"
				kostok=self.stok(stkod)
				kostok2=self.stok2(stkad)
				print "---",stkod,stkad
				stokbul=0
				if (kostok):
					stkod=kostok.kod
					stkad=kostok.isim
					print "kod_tanimli",kostok.kod,kostok.isim
					stokbul=1		
				elif (kostok2):
					stkod=kostok2.kod
					stkad=kostok2.isim
					print "isim_tanimli",kostok2.kod,kostok2.isim
					stokbul=1
				else:
					rapor+=stkod+":"+stkad+","
				
				if stokbul==1:
					miktar=0
					bf=0
					if dat[2]!="" and dat[2]:
						ms=dat[2]
						ms=ms.replace(",",".")
						miktar=float(ms)
					if dat[3]!="" and dat[3]:
						if dat[3]=="-1":
							bf=self.stok(stkod).satis_fiat3
						elif dat[3]=="-2":
							bf=self.stok(stkod).satis_fiat2
						else:	
							bfs=dat[3]
							bfs=bfs.replace(",",".")
							bf=float()
					tutar=miktar*bf	
					if miktar !=0:
						stharyeni=(stkod,stkad,miktar,bf,tutar,stkno)
						self.stk_ekle(stharyeni)
			sayac+=1
		if rapor=="":
			return "tamam"
		else:
			return rapor
		
	def stk_sadelestir(self,stkno):
		print stkno+" stk sadelestiriliyor....."  
		ax = datetime.datetime.now()
		con = lite.connect("stoklist.db")
		with con:    
			cur = con.cursor()
			sql="insert into stoklist(stkod,stkad,miktar,bf,tutar,stoklistno) select * from (SELECT stkod,stkad,sum(miktar) as toplam,bf,sum(miktar)*bf as tutar,stoklistno FROM stoklistgcc where stoklistno='"+stkno+"' group by stkad,bf order by stkod) as t where toplam > 0 "
			cur.execute(sql)
			cur.execute("delete FROM stoklistgcc where stoklistno='"+stkno+"'")
		ay = datetime.datetime.now()
		print "stk sadelestirildi.  ",(ay-ax).total_seconds()," saniye surdu."   
		
			
	def gtfYstk(self,gtfdos,poscari,merkez):
		print "gtf --> stk donusumu yapiliyor..."
		stokads=self.stoklar_ads()
		anastk=[]
		sthar=[]
		s=0
		sgec=0
		hata='yok'
		'''
		trh=gtfdos.split('@')[0]
		trh=self.tarih_format(trh)
		trh=trh.split()[0]
		stkno=poscari+"@POS@x@SATIS@"+trh+".stk" 
		'''
		with open(gtfdos,'r') as f:
			for ikstr in f:
				ikstr=ikstr.split()
				stra=ikstr[0]
				if stra != "SIGNATURE=GNDSALES.GDF":
					trh=ikstr[2]
					trh=self.tarih_format(trh)
					trh=trh.split()[0]
					stkno=poscari+"@POS@x@SATIS@"+trh+".st2"
					break
					
		with open(gtfdos,'r') as f:	
			for line in f:
				line=line.split()
				islemtip=line[0]
				if(islemtip=='01'):
					gecerli=line[7]

				if(islemtip=='02' and gecerli=='00'):
					stokod=line[2]
					iptal=line[3]
					miktar=line[6]
					miktar=miktar.replace(',','.')
					miktar=float(miktar)
					if(iptal=='10'):
						miktar=miktar*-1
					olcubr=line[7][0] 
					if(olcubr=='1'):
						miktar=miktar/1000
					bf= line[7][1:]
					bf=bf.replace(',','.')
					bf=float(bf)
					isk= line[10]
					tutar=line[8]
					tutar=tutar.replace(',','.')
					tutar=float(tutar)
					if(isk!='0'):
						isk=isk.replace(',','.')
						isk=float(isk)
						tutar=tutar-isk
						bf=tutar/miktar
						#bf=round(bf,3)
					tutar=bf*miktar
					#tutar=round(tutar,3)
					#if(stok not in anastk):
					if(stokod in stokads and stokads[stokod]):
						stokad=str(stokads[stokod])
						sthar=[stokod,stokad,miktar,bf,tutar,stkno]
						#print stokod
					else:
						sthar=None
						print 'stok kodlu urun bulunamadi:',stokod
						l.yaz("POS AKTARIM HATASI: "+stokod+" stok kodlu urun bulunamadi")
						hata='var'
						break
					anastk.append(sthar)	
					sgec+=1	
				
		if(hata=='yok'):
			odemeler=self.gtf_analiz(gtfdos)
			kasa=odemeler[0]
			kredi=odemeler[1]
			veresiye=odemeler[2]
			odemeler=[]
			cariler=self.ayar_al('999',poscari+'_poscari')
			kasa_cari=cariler[0]
			kasa_odemestk=kasa_cari+"@POS"+"@x@KGIRIS@"+trh+".st2"
			sthar=["NAKIT","NAKIT",1,kasa,kasa,kasa_odemestk]
			odemeler.append(sthar)
			kredi_cari=cariler[1]
			kredi_odemestk=merkez+"@"+kredi_cari+"@x@KCIKIS@"+trh+".st2"
			sthar=["NAKIT","NAKIT",1,kredi,kredi,kredi_odemestk]
			odemeler.append(sthar)
			veresiye_cari=cariler[2]
			veresiye_odemestk=merkez+"@"+veresiye_cari+"@x@KCIKIS@"+trh+".st2"
			sthar=["NAKIT","NAKIT",1,veresiye,veresiye,veresiye_odemestk]
			odemeler.append(sthar)
			
			con = lite.connect(self.ayar_al('999','stoklist_db'))
			cur = con.cursor()
			with con:
				for stokhar in anastk:
					cur.execute("INSERT INTO stoklistgcc (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar)
				for stokhar2 in odemeler:
					cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar2)
			print "donusum datasi cevriliyor....."
			self.stk_sadelestir(stkno)
			print "pos > stk islemi bitti."
			return "tamam"
		else:
			return "hata"
	
	def pos_urunliste(self,kriter,aranan):
		pos_dizin="./pos/"#self.ayar_al('999','pos_dizin')
		pos_dizin_sablon="./pos/sablon/"#self.ayar_al('999','pos_dizin_sablon')
		dosya=open(pos_dizin+"/"+'GNCPLUF.GTF','w')
		urunlist="SIGNATURE=GNDPLU.GDF"+"\n"
		stoklar=self.stoklar_pos(kriter,aranan)
		for stok in stoklar:
			stkod=stok[0]
			stkad=stok[1]
			stkad=stkad.upper()
			stkadks=stkad[0:20]
			sf1=stok[2]
			sf1=round(sf1,2)
			sf1=str(sf1)
			sf1=sf1.replace('.',',')
			sf2=stok[3]
			sf2=round(sf2,2)
			sf2=str(sf2)
			sf2=sf2.replace('.',',')
			sf3=stok[4]
			sf3=round(sf3,2)
			sf3=str(sf3)
			sf3=sf3.replace('.',',')
			kdvoran=stok[5]
			kdvkod=""
			if(kdvoran==0.00):
				kdvkod='00'
			if(kdvoran==1.00):
				kdvkod='03'
			if(kdvoran==8.00):
				kdvkod='01'
			if(kdvoran==18.00):
				kdvkod='02'
			if(str(stok[6])!='NULL'):
				orta_sabit=open(pos_dizin_sablon+"pos_orta_sabit.pos",'r').read()
				son_sabit=open(pos_dizin_sablon+"pos_son_sabit.pos",'r').read()
				orta_sabit=orta_sabit.replace('@grupkod@',str(stok[6]))
				if(str(stok[7]).upper() in ['KG','GR','LT']):
					orta_sabit=orta_sabit.replace('@olcubr@','11000')
					son_sabit=son_sabit.replace('@olcubr@','10')
				else:
					orta_sabit=orta_sabit.replace('@olcubr@','01   ')
					son_sabit=son_sabit.replace('@olcubr@','00')
				son_sabit=son_sabit.replace('@kdv@',kdvkod)
				for i in range(0,403):
					if(i==0):
						urunlist+="01  1"+stkod.upper()
					if(i<30 and i>5+len(stkod)):
						urunlist+=" "
					if(i==31):
						urunlist+=stkod.upper()
					if(i==55):
						urunlist+=stkad
					if(i<54 and i>29+len(stkod)):
						urunlist+=" "
					if(i==135):
						urunlist+=stkadks
					if(i<135 and i>54+len(stkad)):
						urunlist+=" "
					if(i==190):
						urunlist+=orta_sabit
					if(i<190 and i>133+len(stkadks)):
						urunlist+=" "
					if(i==356):
						urunlist+=sf1
					if(i<371 and i>355+len(sf1)):
						urunlist+=" "
					if(i==370):
						urunlist+=sf2
					if(i<386 and i>370+len(sf2)):
						urunlist+=" "
					if(i==386):
						urunlist+=sf3
					if(i==401):
						urunlist+=son_sabit
					if(i<401 and i>385+len(sf3)):
						urunlist+=" "

					'''	
					if(i==356):
						urunlist+=sf1
					if(i<370 and i>355+len(sf1)):
						urunlist+=" "
					if(i==371):
						urunlist+=sf2
					if(i<386 and i>370+len(sf2)):
						urunlist+=" "
					if(i==386):
						urunlist+=sf3
					if(i==401):
						urunlist+=son_sabit
					if(i<401 and i>385+len(sf3)):
						urunlist+=" "
					'''
				#stoka ait barkodlarin ayarlanmasi
				barkodlist=""
				urunlist+="\n"
				barkod1=stok[8]
				if(barkod1!="" and barkod1!="NULL"):
					for j in range(0,90):
						if(j==0):
							barkodlist+="02  1"+stkod.upper()
						if(j<30 and j>5+len(stkod)):
							barkodlist+=" "
						if(j==31):
							barkodlist+=barkod1	
						if(j==55):
							barkodlist+=barkod1	
						if(j<54 and j>29+len(barkod1)):
							barkodlist+=" "
						if(j==78):
							barkodlist+="1     001"
						if(j<77 and j>52+len(barkod1)):
							barkodlist+=" "
					urunlist+=barkodlist+"\n"
					barkodlist=""
				barkod2=stok[9]
				if(barkod2!="" and barkod2!="NULL"):
					for j in range(0,90):
						if(j==0):
							barkodlist+="02  1"+stkod.upper()
						if(j<30 and j>5+len(stkod)):
							barkodlist+=" "
						if(j==31):
							barkodlist+=barkod2
						if(j==55):
							barkodlist+=barkod2
						if(j<54 and j>29+len(barkod2)):
							barkodlist+=" "
						if(j==78):
							barkodlist+="1     002"
						if(j<77 and j>52+len(barkod2)):
							barkodlist+=" "
					urunlist+=barkodlist+"\n"
					barkodlist=""
				barkod3=stok[10]
				if(barkod3!="" and barkod3!="NULL"):
					for j in range(0,90):
						if(j==0):
							barkodlist+="02  1"+stkod.upper()
						if(j<30 and j>5+len(stkod)):
							barkodlist+=" "
						if(j==31):
							barkodlist+=barkod3
						if(j==55):
							barkodlist+=barkod3
						if(j<54 and j>29+len(barkod3)):
							barkodlist+=" "
						if(j==78):
							barkodlist+="1     003"
						if(j<77 and j>52+len(barkod3)):
							barkodlist+=" "
					urunlist+=barkodlist+"\n"
					barkodlist=""	
				barkod4=stok[11]
				if(barkod4!="" and barkod4!="NULL"):
					for j in range(0,90):
						if(j==0):
							barkodlist+="02  1"+stkod.upper()
						if(j<30 and j>5+len(stkod)):
							barkodlist+=" "
						if(j==31):
							barkodlist+=barkod4
						if(j==55):
							barkodlist+=barkod4
						if(j<54 and j>29+len(barkod4)):
							barkodlist+=" "
						if(j==78):
							barkodlist+="1     004"
						if(j<77 and j>52+len(barkod4)):
							barkodlist+=" "
					urunlist+=barkodlist+"\n"
					barkodlist=""	
				barkod5=stok[12]
				if(barkod5!="" and barkod5!="NULL"):
					for j in range(0,90):
						if(j==0):
							barkodlist+="02  1"+stkod.upper()
						if(j<30 and j>5+len(stkod)):
							barkodlist+=" "
						if(j==31):
							barkodlist+=barkod5
						if(j==55):
							barkodlist+=barkod5
						if(j<54 and j>29+len(barkod5)):
							barkodlist+=" "
						if(j==78):
							barkodlist+="1     005"
						if(j<77 and j>52+len(barkod5)):
							barkodlist+=" "
					urunlist+=barkodlist+"\n"
					barkodlist=""	
				barkod6=stok[13]
				if(barkod6!="" and barkod6!="NULL"):
					for j in range(0,90):
						if(j==0):
							barkodlist+="02  1"+stkod.upper()
						if(j<30 and j>5+len(stkod)):
							barkodlist+=" "
						if(j==31):
							barkodlist+=barkod6
						if(j==55):
							barkodlist+=barkod6
						if(j<54 and j>29+len(barkod6)):
							barkodlist+=" "
						if(j==78):
							barkodlist+="1     006"
						if(j<77 and j>52+len(barkod6)):
							barkodlist+=" "
					urunlist+=barkodlist+"\n"
					barkodlist=""		
		dosya.write(urunlist)
		return "0"
		
	def tarih_format(self,tarih):
		tarih=tarih.replace('.','-')
		tarih=tarih.replace(',','-')
		tarih=tarih.replace('/','-')
		tarih=tarih.split('-')
		#enttarih=tarih[2][2:4]+tarih[1]+tarih[0]
		tarih=tarih[2]+"-"+tarih[1]+"-"+tarih[0]
		tarih=str(tarih)
		tarih=tarih+" 00:00:00"
		return tarih
		
	def tarih_turk(self,tarih):
		tarih=str(tarih)
		tarih=tarih.split()
		tarih=tarih[0]
		tarih=tarih.split('-')
		tarih=tarih[2]+"-"+tarih[1]+"-"+tarih[0]
		tarih=str(tarih)
		return tarih
	
	def calistir(self,sql):
		#print sql
		con=""
		sqlparca=""
		try:
			con = pymysql.connect(baglanti.host, baglanti.kullanici,baglanti.sifre,baglanti.vt,charset='latin5')
			#con.set_character_set('latin5')
			cur = con.cursor()
			#print "mysqlmak.py-baglanti acildi"
			sql=sql.split(';')
			for sqlparca in sql:
				cur.execute(sqlparca)
				rows = cur.fetchall()
				if(rows):
					rows=list(rows)
					if con:    
						#print "mysqlmak.py-baglanti kapandi-select islemi"
						con.close()	
					return rows	
			if con:    
				#print "mysqlmak.py-baglanti kapandi-select islemi"
				con.close()	
			#00:23 06.02.2014
		except :
			print "mysqlmak.py-HATA:",str(sys.exc_info()[1])
			if con:    
				print "baglanti kapandi-select islemi"
				con.close()	
	
	def calis(self,sql):
		#print sql
		hata=""
		sql=sql.split(';')
		try:
			con = pymysql.connect(baglanti.host, baglanti.kullanici,baglanti.sifre,baglanti.vt,charset='latin5')
			#con.set_character_set('latin5')
			cur = con.cursor()
			for sqlparca in sql:
				cur.execute(sqlparca)
		except:
			hata=sys.exc_info()[1]
			if(hata[1]=='Query was empty'):
				con.commit()	
			else:
				con.rollback()
				print "SQL CALISTIRMA HATASI:",str(sys.exc_info()[1])
				return str(sys.exc_info()[1])
			
		if con:    
			con.close()
		'''if(hata[1]=='Query was empty'):
			self.conn.commit()
			return "tamam"
		else:
			self.conn.rollback()
			print str(sys.exc_info()[1])'''
		return "tamam"
	
	def yaziyla(self,tutar):
		yazi=[]
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
		yazi.append(yaziyla1)
		yazi.append(yaziyla2)
		return yazi
	
	def carikod_degistir(self,eskikod,yenikod):
		sqldosya='./altyapi/sql/carikod_degistir.sql'
		sql=codecs.open(sqldosya,'r','iso-8859_9').read()
		sql=sql.replace('@eskikod@',eskikod)
		sql=sql.replace('@yenikod@',yenikod)
		sonuc=self.calis(sql)
		return sonuc
	
	def cari_yaslandirma(self,iscari,hedef,tarih=""):
		
		simdiki_zaman=datetime.datetime.now()
		
		if tarih=="":
			tarih =simdiki_zaman 
		else: 
			tarih=self.tarih_format(tarih)
		sql=open('./altyapi/sql/cari_borc_liste.sql','r').read()
		sql=sql.replace('@hedef@',str(hedef))
		sql=sql.replace('@vade_tarihi@',str(tarih))
		#open("./sql_cikti/yaslandirma.sql",'w').write(sql)
		#print sql
		vagebolar=self.calistir(sql)
		
		sql=open('./altyapi/sql/cari_borc_top.sql','r').read()
		sql=sql.replace('@hedef@',str(hedef))
		sql=sql.replace('@vade_tarihi@',str(tarih))
		vagebot=self.calistir(sql)[0][0]
		if(vagebot):
			vagebot=float(str(vagebot))
			#print "topborc",vagebot
			#07:30 17.01.2015
			#iscariler=iscari.split(',')
			#iscari=""
			#for cari in iscariler:
			#	iscari+="'"+cari+"',"
			#iscari="'"+iscari[1:len(iscari)-2]+"'"
			sql=open('./altyapi/sql/cari_toplam_cikis.sql','r').read()
			sql=sql.replace('@kaynak@',str(iscari))
			sql=sql.replace('@hedef@',str(hedef))
			sql=sql.replace('@vade_tarihi@',str(tarih))
			open("./sql_cikti/yaslandirma2_data.sql",'w').write(sql)
			odemetop=self.calistir(sql)
			odemetop=odemetop[0][0]
			if odemetop is None:
				odemetop=0
			else:
				odemetop=float(str(odemetop))
			#print "odediimiz top",odemetop

			vadelimit=0
			vadegecler=[]
			#vadesi gecenlerde borc kadar olan kayitlari bulmak
			for vagebo in vagebolar:
				vageborc=float(vagebo[1])
				#print "odenecek",vageborc
				odemetop=float('{0:.2f}'.format(odemetop))
				vageborc=float('{0:.2f}'.format(vageborc))
				kalanodeme=odemetop-vageborc
				eko='{0:.20f}'.format(kalanodeme)
				if eko[0:5]=="-0.00":
					print "zz",kalanodeme
					kalanodeme=0
				
				if(kalanodeme<0 and odemetop!=0):
					kalanborc=kalanodeme*-1
					odemetop=0
				else:
					kalanborc=vageborc
					
				if odemetop>=vageborc:	
					odemetop=kalanodeme
				else:
					diff=vagebo[2]-simdiki_zaman
					ftrh=str(vagebo[0]).split()[0]
					ftutar=float(vagebo[1])
					vtrh=str(vagebo[2]).split()[0]
					vadegecler.append([ftrh,vtrh,ftutar,kalanborc,diff.days])
		else:
			return "rapor yok"
		#for vadegec in vadegecler:
		rapor=statikrapor()
		dizibas=['fatura','vade','fatura tutar','geciken tutar','gun']
		top_sutlar=[-1,-1,-1,3]
		rapor_html=rapor.diziYhtml(vadegecler,dizibas,top_sutlar)
		return rapor_html
	
	def sube_cariler(self,merkez):
		sql=open('./altyapi/sql/sube_cariler.sql','r').read()
		sql=sql.replace('@merkez@',str(merkez))
		cariler=self.calistir(sql)
		cr=[]
		for cari in cariler:
			cr.append(cari[0])
		return cr
	
	def iban_dokum(self):
		sql=open('./altyapi/sql/iban_dokum.sql','r').read()
		rapor=statikrapor()
		topsut=[9,9,2,3]
		rapor.sql(sql,rapbas="IBAN RAPORU",alt=1,topsut=topsut)
		sonuc=rapor.getHtml()
		return sonuc
		
	def cari_borc_dokum(self,merkez,tarih=""):
		kaynak=merkez
		#kaynak=self.sube_cariler(merkez)
		#kaynak=self.diziYstr_dizi(str(kaynak))
		simdiki_zaman=datetime.datetime.now()
		if tarih=="":
			tarih =simdiki_zaman 
		else: 
			tarih=self.tarih_format(tarih)
			
		sql=open('./altyapi/sql/cari_borc_dokum.sql','r').read()
		sql=sql.replace('@kaynak@',str(kaynak))
		sql=sql.replace('@vade_tarihi@',str(tarih))
		codecs.open('sql_cikti/cari_borc_dokum_data.sql','w','iso-8859_9').write(sql)
		rapor=statikrapor()
		topsut=[9,9,2,3]
		rapor.sql(sql,rapbas="BORC RAPORU",alt=1,topsut=topsut)
		sonuc=rapor.getHtml()
		
		sql2=open('./altyapi/sql/cari_alacak_dokum.sql','r').read()
		sql2=sql2.replace('@kaynak@',str(kaynak))
		sql2=sql2.replace('@vade_tarihi@',str(tarih))
		codecs.open('sql_cikti/cari_alacak_dokum_data.sql','w','iso-8859_9').write(sql2)
		rapor2=statikrapor()
		topsut2=[9,9,2,3]
		rapor2.sql(sql2,rapbas="ALACAK RAPORU",alt=1,topsut=topsut2)
		sonuc2=rapor2.getHtml()
		
		sql3=open('./altyapi/sql/cari_alacak_dokum_per.sql','r').read()
		sql3=sql3.replace('@kaynak@',str(kaynak))
		sql3=sql3.replace('@vade_tarihi@',str(tarih))
		codecs.open('sql_cikti/cari_alacak_dokumper_data.sql','w','iso-8859_9').write(sql3)
		rapor3=statikrapor()
		topsut3=[9,9,2,3]
		rapor3.sql(sql3,rapbas="PERSONEL HESAPLARI",alt=1,topsut=topsut3)
		sonuc3=rapor3.getHtml()
		
		
		sql4=open('./altyapi/sql/cari_alacak_dokum_seyyar.sql','r').read()
		sql4=sql4.replace('@kaynak@',str('seyyar'))
		sql4=sql4.replace('@vade_tarihi@',str(tarih))
		codecs.open('sql_cikti/cari_alacak_dokumseyyar_data.sql','w','iso-8859_9').write(sql4)
		rapor4=statikrapor()
		topsut4=[9,9,2,3]
		rapor4.sql(sql4,rapbas="SEYYAR SATICI CARILERI",alt=1,topsut=topsut4)
		sonuc4=rapor4.getHtml()
		
		
		
		htmlrp="<table><tr><td rowspan='3'>"+sonuc+"</td><td></td>-<td>"+sonuc2+"</td></tr><tr><td>-</td><td>"+sonuc4+"</td></tr><tr><td>-</td><td>"+sonuc3+"</td></tr></table>"
		return htmlrp
		#return sonuc+"<br>"+sonuc2
		'''borcdok=self.calistir(sql)
		rapor=statikrapor()
		dizibas=['cari kod','cari isim','vadesi geçen borc','toplam borc']
		top_sutlar=[9,9,2,3]
		rapor_html=rapor.diziYhtml(borcdok,dizibas,top_sutlar)
		return rapor_html
		'''
	def kontrol_cari_hareket(self,merkez,tarih=""):
		kaynak=merkez
		#kaynak=self.sube_cariler(merkez)
		#kaynak=self.diziYstr_dizi(str(kaynak))
		simdiki_zaman=datetime.datetime.now()
		if tarih=="":
			tarih =simdiki_zaman 
		else: 
			tarih=self.tarih_format(tarih)
			
		sql=open('./altyapi/sql/kontrol_cari_takip.sql','r').read()
		sql=sql.replace('@kaynak@',str(kaynak))
		sql=sql.replace('@vade_tarihi@',str(tarih))
		#codecs.open('cari_borc_dokum_data.sql','w','iso-8859_9').write(sql)
		rapor=statikrapor()
		topsut=[]
		rapor.sql(sql,rapbas="CARI KONTROLU",alt=1,topsut=topsut)
		sonuc=rapor.getHtml()
		
		htmlrp="<table><tr><td>"+sonuc+"</td><td>-</td><td>"+"r2"+"</td></tr></table>"
		return htmlrp
		
	def kontrol_cari_dokum(self,merkez,tarih=""):
		kaynak=merkez
		#kaynak=self.sube_cariler(merkez)
		#kaynak=self.diziYstr_dizi(str(kaynak))
		simdiki_zaman=datetime.datetime.now()
		if tarih=="":
			tarih =simdiki_zaman 
		else: 
			tarih=self.tarih_format(tarih)
			
		sql=open('./altyapi/sql/kontrol_cari_borc_dokum.sql','r').read()
		sql=sql.replace('@kaynak@',str(kaynak))
		sql=sql.replace('@vade_tarihi@',str(tarih))
		#codecs.open('cari_borc_dokum_data.sql','w','iso-8859_9').write(sql)
		rapor=statikrapor()
		topsut=[9,9,2,3]
		rapor.sql(sql,rapbas="BORCLU CARI KONTROLU",alt=1,topsut=topsut)
		sonuc=rapor.getHtml()
		
		sql2=open('./altyapi/sql/kontrol_cari_alacak_dokum.sql','r').read()
		sql2=sql2.replace('@kaynak@',str(kaynak))
		sql2=sql2.replace('@vade_tarihi@',str(tarih))
		#codecs.open('cari_alacak_dokum_data.sql','w','iso-8859_9').write(sql2)
		rapor2=statikrapor()
		topsut2=[9,9,2,3]
		rapor2.sql(sql2,rapbas="ALACAK CARI KONTROLU",alt=1,topsut=topsut2)
		sonuc2=rapor2.getHtml()
		
		htmlrp="<table><tr><td>"+sonuc+"</td><td>-</td><td>"+sonuc2+"</td></tr></table>"
		return htmlrp
	
	def cari_odeme_plani(self,merkez,gun="60",raptip="dizi"):
		cariler=[]
		for row in self.cari_sorgu("rapor_kodu1","takip","dizi"):
			cariler.append(row[0])
		kaynak=merkez
		data=""
		plan=[]
		for cari in cariler:
			sql=open('./altyapi/sql/cari_odeme.sql','r').read()
			sql=sql.replace('@carikod@',str(cari))
			odeme=self.calistir(sql)[0][0]
			if odeme:
				odeme=float(str(odeme))
			else:
				odeme=0
			sql=open('./altyapi/sql/cari_alacak.sql','r').read()
			sql=sql.replace('@carikod@',str(cari))
			alacaklar=self.calistir(sql)
			kalan=0
			if alacaklar:
				for alacak in alacaklar:
					borc=float(alacak[1])
					if odeme>borc:
						odeme=odeme-borc
					else:
						kalan=borc-odeme+kalan
						odeme=0
						tarih=str(alacak[0]).split()[0]
						if kalan>0:
							plan.append([self.cari(cari).isim,alacak[2],tarih,borc,kalan])
		rapor=statikrapor()
		dizibas=['isim','aciklama','vade_tarihi','vdtutar','tutar']
		top_sutlar=[0,1]
		rapor_html=rapor.diziYhtml(plan,dizibas,top_sutlar)
		return rapor_html
	
	def satis_raporu_kdvli(self,subekod,bastarih,sontarih):
		bastarih=self.tarih_format(bastarih)
		sontarih=self.tarih_format(sontarih)
		sql=open('./altyapi/sql/kdvlisatistop.sql','r').read()
		sql=sql.replace('@bastarih@',bastarih)
		sql=sql.replace('@sontarih@',sontarih)
		sql=sql.replace('@subekod@',subekod)
		satislar=self.calistir(sql)
		#codecs.open('kdvlisatis_data.sql','w','iso-8859_9').write(sql)
		#print satislar[0],satislar[1]
		gc_trh=satislar[0][3]
		gctop=0
		satisharlar=[]
		satisharlar.append(["tarih",satislar[0][3]])
		for satis in satislar:
			if(satis[3]!=gc_trh):
				#print "guntoplam",gctop
				if len(satisharlar)>1:
					satisharlar.append(["-","toplam satis",gctop])
					satisharlar.append(["-","----------------------","-"])
				#print self.tarih_turk(satis[3])
					satisharlar.append(["tarih",satis[3]])
					gc_trh=satis[3]
				gctop=0
			satisharlar.append([satis[0],satis[1],satis[2]])	
			gctop+=satis[2]
		#print "guntoplam",gctop
		satisharlar.append(["0","toplam satis",gctop])
		
		rapor=statikrapor()
		dizibas=['kodu','kdv grup ismi','tutar']
		top_sutlar=[-1,-1,-1]
		rapor_html=rapor.diziYhtml(satisharlar,dizibas,top_sutlar)
		return rapor_html
	
	def bakiye_tutar(self,subekod,tarih):
		tarih=self.tarih_format(tarih)
		sql=open('./altyapi/sql/tarihli_bakiye_tutar.sql','r').read()
		sql=sql.replace('@bastarih@',tarih)
		sql=sql.replace('@subekod@',subekod)
		meblag=self.calistir(sql)[0][0]
		if meblag:
			return meblag
		else:
			return 0
	
	def cari_alim_toplami(self,mkod,subekod,bastarih,sontarih):
		bastarih=self.tarih_format(bastarih)
		sontarih=self.tarih_format(sontarih)
		sql=open('./altyapi/sql/cari_alim_toplami.sql','r').read()
		sql=sql.replace('@bastarih@',bastarih)
		sql=sql.replace('@sontarih@',sontarih)
		sql=sql.replace('@subekod@',subekod)
		sql=sql.replace('@mkod@',mkod)
		meblag=self.calistir(sql)[0][0]
		if meblag:
			return meblag
		else:
			return 0
		
	def cari_satis_toplami(self,subekod,bastarih,sontarih):
		bastarih=self.tarih_format(bastarih)
		sontarih=self.tarih_format(sontarih)
		sql=open('./altyapi/sql/cari_satis_toplami.sql','r').read()
		sql=sql.replace('@bastarih@',bastarih)
		sql=sql.replace('@sontarih@',sontarih)
		sql=sql.replace('@subekod@',subekod)
		meblag=self.calistir(sql)[0][0]
		if meblag:
			return meblag
		else:
			return 0
			
	def cari_satis_maliyet(self,subekod,bastarih,sontarih):
		bastarih=self.tarih_format(bastarih)
		sontarih=self.tarih_format(sontarih)
		sql=open('./altyapi/sql/cari_satis_maliyeti.sql','r').read()
		sql=sql.replace('@bastarih@',bastarih)
		sql=sql.replace('@sontarih@',sontarih)
		sql=sql.replace('@subekod@',subekod)
		meblag=self.calistir(sql)[0][0]
		if meblag:
			return meblag
		else:
			return 0
		
	def cari_iade_toplami(self,mkod,subekod,bastarih,sontarih):
		bastarih=self.tarih_format(bastarih)
		sontarih=self.tarih_format(sontarih)
		sql=open('./altyapi/sql/cari_iade_toplami.sql','r').read()
		sql=sql.replace('@bastarih@',bastarih)
		sql=sql.replace('@sontarih@',sontarih)
		sql=sql.replace('@subekod@',subekod)
		sql=sql.replace('@mkod@',mkod)
		meblag=self.calistir(sql)[0][0]
		if meblag:
			return meblag
		else:
			return 0
	
	def pazar_rapor(self,mkod,subekod,bastarih,sontarih):
		raporana=[]
		devreden=self.bakiye_tutar(subekod,bastarih)
		devredecek=self.bakiye_tutar(subekod,sontarih)
		alimtop=self.cari_alim_toplami(mkod,subekod,bastarih,sontarih)
		iadetop=self.cari_iade_toplami(mkod,subekod,bastarih,sontarih)
		satistop=self.cari_satis_toplami(subekod,bastarih,sontarih)
		stokaj=devreden-devredecek
		#12:09 07.04.2015
		#gat=alimtop+stokaj-iadetop
		maliyet=self.cari_satis_maliyet(subekod,bastarih,sontarih)
		#codecs.open('./sql_cikti/pazar_rapor_data.sql','w','iso-8859_9').write(sql)
		raporana.append(['devreden',devreden])
		raporana.append(['devredecek',devredecek])
		raporana.append(['stokaj',stokaj])
		raporana.append(['iade_toplami',iadetop])
		raporana.append(['alim_toplami',alimtop])
		raporana.append(['satilan_mal_maliyeti',maliyet])
		raporana.append(['satilan_mal_tutari',satistop])
		raporana.append(['kar_orani %',round(((satistop/maliyet)-1)*100,2)])
		
		
		rapor=statikrapor()
		dizibas=[self.cari(subekod).isim,bastarih+"-"+sontarih]
		top_sutlar=[-1,-1,-1]
		rapor_html=rapor.diziYhtml(raporana,dizibas,top_sutlar)
		return rapor_html
	
	def diziYstr_dizi(self,dizi):
		diziler=dizi.split(',')
		dizis=""
		for cari in diziler:
			dizis+=""+cari+","
		dizis=""+dizis[1:len(dizis)-2]+""
		return dizis
		
	def sonalim_bf(self,kaynak,hedef,stokod):
		sql=open('./altyapi/sql/sonalim_bf.sql','r').read()
		sql=sql.replace('@hedef@',str(hedef))
		sql=sql.replace('@kaynak@',str(kaynak))
		sql=sql.replace('@stokod@',str(stokod))
		bf=self.calistir(sql)
		if bf:
			bf=bf[0][0]
			if(bf):
				return round(float(bf),3)
		return 0
	
	def sonsatis_bf(self,kaynak,hedef,stokod):
		sql=open('./altyapi/sql/sonsatis_bf.sql','r').read()
		sql=sql.replace('@hedef@',str(hedef))
		sql=sql.replace('@kaynak@',str(kaynak))
		sql=sql.replace('@stokod@',str(stokod))
		bf=self.calistir(sql)
		if bf:
			bf=bf[0][0]
			if(bf):
				return round(float(bf),3)
		return 0
	
	
	def stkYftr(self,stkno,kdvdurum='E',med='H',kaydeden="giom"):
		ax=datetime.datetime.now()
		print "mak.stkYftr islemi basladi...."
		stknog=stkno
		stkno=stkno.split('@')	
		otofisno=''
		merkez=stkno[0]
		if self.cari(merkez) is None:
			return "hata merkez cari tanimsiz"
		hedef=stkno[1]	
		hedef=stkno[1]	
		if self.cari(hedef) is None:
			return "hata hedef cari tanimsiz"
		urtkod=stkno[2]	
		fattip=stkno[3]	
		tarih=stkno[4].split('.')[0]
		yil=tarih.split('-')[0]
		ay=tarih.split('-')[1]
		if(len(ay)==1):
			ay='0'+ay
		gun=tarih.split('-')[2]
		if(len(gun)==1):
			gun='0'+gun
		randfis=randint(1000,9999)
		tarih=gun+'-'+ay+'-'+yil
		otofisno=fattip[0:2]+ay+gun+str(randfis)	
		yon=""
		if(fattip in ("ALIS","AGIRIS","GIRIS","KGIRIS")):
			yon="G"
		if(fattip in ("SATIS","ACIKIS","DAT","CIKIS","KCIKIS")):
			yon="C"
	
		if(self.fisno_kontrol(otofisno)=="yok"):
			fatura=Fatura()
			fatura.islem='F'
			fatura.fattip=yon
			fatura.vadesay=1
			fatura.tarih=tarih
			fatura.vadetarih=tarih
			fatura.fisno=otofisno
			fatura.kaynak=merkez
			fatura.hedef=hedef
			fatura.med=med
			fatura.irs='H'
			fatura.kaydeden=kaydeden
			fatura.stharlistno=stknog
			fatura.kdvdurum=kdvdurum
			fatura.takipkod=urtkod
			fatura.aciklama=""
			
			if(fattip in ["KCIKIS","KGIRIS"]):
				fatura.islem='K'
				fatura.kdvdurum='E'
				tutarfsb=self.stk_fsb_al(stknog)
				if tutarfsb is None:
					return "olumsuz"
				tutarsda=float(tutarfsb[0].split('=')[1])
				if fattip=='KCIKIS':
					tutarsda=tutarsda*-1
				fatura.tutar=tutarsda
				
				
			fatsonuc=self.faturalama(fatura,'y')
			if fatsonuc != "olumsuz":
				#faturalama olduktsan sonra silme
				self.stk_sil(stknog)
				ay=datetime.datetime.now()
				print "mak.stkYftr bitti.",(ay-ax).total_seconds()
				return "stk > fatura islemi basarili."
			else:
				return "stok kaynakli hata logu inceleyin"
		else:
			return "fisno uyumsuzluk sorunu"
		
	def gtf_analiz(self,gtfdos):
		with open(gtfdos,'r') as f:
			gtop=0
			ktop=0
			vtop=0
			for line in f:
				sat=line
				line=line.split()
				islemtip=line[0]
				#odemetip: 0 odeme 1 para ustu 2 doviz
				odemetipi=sat[11:12]
				#odemeref :0 nakit 0-39 1 kredi 2 veresiye
				odemeref=sat[9:10]
				#odeme iptali :0 iptal - 1 normal odendi
				odemeiptal=sat[12:13]
				if islemtip=='03' and odemetipi=='0':
					tt=sat[13:19]
					tt=tt.replace(',','.')
					tutar=float(tt)
					if odemeiptal=='0':
						tutar=tutar*-1
					#veresiye
					if odemeref=='2':
						vtop+=tutar
					#kredi
					if odemeref=='1':
						ktop+=tutar
						
				if(islemtip=='01'):
					gecerli=line[7]
					if(gecerli=='00'):
						tutar=line[11]
						tutar=tutar.replace(",",".")
						tutar=float(tutar)
						gtop+=tutar
			ntop=round(gtop-(ktop+vtop),2)
			ktop=round(ktop,2)
			vtop=round(vtop,2)
			return [ntop,ktop,vtop]	
			
	def kasabanka_rapor(self,merkez=""):
		cariler=[]
		caribankalar=self.cariler_getir("","B")
		for cari in caribankalar:
			kod=cari.split('@')[1]
			cariler.append(kod)
		
		carikasalar=self.cariler_getir("","K")
		for cari in carikasalar:
			kod=cari.split('@')[1]
			cariler.append(kod)
		raporana=""
		for carix in cariler:
			sql=open('./altyapi/sql/kasabanka_rapor.sql','r').read()
			sql=sql.replace('@kaynak@',str(carix))
			codecs.open('sql_cikti/kasabanka_rapor_data.sql','w','iso-8859_9').write(sql)
			rapor=statikrapor()
			topsut=[4,3,9,9,9,9,9]
			rapor.sql(sql,alt=1,topsut=topsut)
			raporana+=rapor.getHtml()+"<br>"
		return raporana
	
	def kasa_rapor(self,kasa,bastarih,sontarih,sonuc='html'):
		sql=open('./altyapi/sql/kasa_rapor2.sql','r').read()
		sql=sql.replace('@bastarih@',str(self.tarih_format(bastarih)))
		sql=sql.replace('@sontarih@',str(self.tarih_format(sontarih)))
		sql=sql.replace('@kaynak@',str(kasa))
		open("kr2.sql",'w').write(sql)
		if sonuc=='html':
			rapor=statikrapor()
			topsut=[4,3,9,9,9,9,9]
			rapor.sql(sql,alt=1,topsut=topsut)
			return rapor.getHtml()
		else:
			row=self.calistir(sql)
			return row
	
	def kasa_rapor_kir(self,kasa,bastarih,sontarih,sonuc='html'):
		row=self.kasa_rapor(kasa,bastarih,sontarih,sonuc='dizi')
		sqldosyak='./altyapi/sql/kasa_devir.sql'
		sqlk=codecs.open(sqldosyak,'r','iso-8859_9').read()
		sqlk=sqlk.replace('@kaynak@',kasa)
		sqlk=sqlk.replace('@tarih@',str(self.tarih_format(bastarih)))	
		devir=self.calistir(sqlk)
		devredecek=devir[0][0]
		rapor=[]
		rapor.append(["-----","-----","------","------","------",devredecek,"------"])
		aratop=0
		tarihgc=row[0][0]
		for r in row:
			tarih=r[0]
			if tarih != tarihgc:
				tarihgc=r[0]
				rapor.append(["-----","-----","------","------","------","------","------"])
				aratop=0
			if r[3]==0:
				aratop-=r[4]
			else:
				aratop+=r[3]
			
			rapor.append([r[0],r[1],r[2],r[3],r[4],r[5]+devredecek,r[6]])
		rapor.append(["-----","-----","------","------","------","------","------"])
		if sonuc=='html':
			dizibas=["tarih","cari","ack","giris","cikis","bakiye","r/gr"]
			rapok=statikrapor()
			return rapok.diziYhtml(rapor,dizibas,topsut=[-1,-1,-1,-1,-1,-1,-1])
		else:
			return rapor
	
	def nesne_goster(self,nesne):
		for attr, value in nesne.__dict__.iteritems():
			print attr,value
		
	def kullanicilar(self,sonuc='html'):
		sql=open('./altyapi/sql/kullanicilar.sql','r').read()
		if sonuc=='html':
			rapor=statikrapor()
			rapor.sql(sql,alt=1)
			return rapor.getHtml()
		else:
			row=self.calistir(sql)
			return row
			
	def kullanici_getir(self,no):
		sql=open('./altyapi/sql/kullanici_getir.sql','r').read()
		sql=sql.replace('@no@',str(no))
		row=self.calistir(sql)
		dizi=self.dizi_dekod(row[0])
		return dizi
	
	def kullanici_getir2(self,no):
		sql=open('./altyapi/sql/kullanici_getir.sql','r').read()
		sql=sql.replace('@no@',str(no))
		row=self.calistir(sql)
		return row[0][2]
	
	def kullanici_posta(self,no):
		sql=open('./altyapi/sql/kullanici_getir.sql','r').read()
		sql=sql.replace('@no@',str(no))
		row=self.calistir(sql)
		return row[0][3]

	
	def kullanici_islem(self,kull,mod):
		if(mod=='s'):
			sql=open('./altyapi/sql/kullanici_sil.sql','r').read()
			sql=sql.replace('@no@',str(kull.no))
		if(mod=='g'):
			sql=open('./altyapi/sql/kullanici_guncelle.sql','r').read()
			sql=sql.replace('@no@',str(kull.no))
		if(mod=='y'):
			sql=open('./altyapi/sql/kullanici_ekle.sql','r').read()
		if(mod in ['y','g']):	
			sql=sql.replace('@sifre@',str(kull.sifre))
			sql=sql.replace('@eposta@',str(kull.eposta))
			sql=sql.replace('@yetki@',str(kull.yetki))
			sql=sql.replace('@uisim@',kull.uisim)
			sql=sql.replace('@isim@',str(kull.isim))
		if self.calis(sql)=="tamam":
			return self.kullanicilar()
		
		
	def giris_kontrol(self,isim,sifre):
		sql=open('./altyapi/sql/giris_kontrol.sql','r').read()
		sql=sql.replace('@isim@',str(isim))
		sql=sql.replace('@sifre@',str(sifre))
		row=self.calistir(sql)
		if (row):
			return row[0][0]
		return None
	
	def girdi_kontrol(self,id):
		sql=open('./altyapi/sql/girdi_kontrol.sql','r').read()
		sql=sql.replace('@id@',str(id))
		row=self.calistir(sql)
		if (row):
			return row[0][0]
		return None
	
	def girdi_isim(self,id):
		sql=open('./altyapi/sql/girdi_isim.sql','r').read()
		sql=sql.replace('@id@',str(id))
		row=self.calistir(sql)
		if (row):
			return row[0][0]
		return None
	
	def girdi_liste(self,sonuc='html'):
		sql=open('./altyapi/sql/girdi_liste.sql','r').read()
		if sonuc=='html':
			rapor=statikrapor()
			rapor.sql(sql,rapbas='bagli_kullanicilar',alt=1)
			return rapor.getHtml()
		else:
			row=self.calistir(sql)
			return row
	
	def giris_ekle(self,id):
		if self.girdi_kontrol(id) is None:
			sql=open('./altyapi/sql/giris_ekle.sql','r').read()
			sql=sql.replace('@id@',str(id))
			return self.calis(sql)
	
	def giris_sil(self,id):
		sql=open('./altyapi/sql/giris_sil.sql','r').read()
		sql=sql.replace('@id@',str(id))
		return self.calis(sql)
	
	def yetki_al(self,id):
		sql=open('./altyapi/sql/yetki_al.sql','r').read()
		sql=sql.replace('@id@',str(id))
		row=self.calistir(sql)
		if (row):
			return row[0][0]
		return None
	
	#yapimasamasinda
	
	def yetki_kontrol(self,oper,yetki):
		sql=open('./altyapi/sql/yetki_kontrol.sql','r').read()
		sql=sql.replace('@id@',str(id))
		row=self.calistir(sql)
		if (row):
			return row[0][0]
		return None
	
	def ayar_islem(self,ayar,mod):
		if(mod=='s'):
			sql=open('./altyapi/sql/ayar_sil.sql','r').read()
			sql=sql.replace('@no@',str(ayar.no))
		if(mod=='g'):
			sql=open('./altyapi/sql/ayar_guncelle.sql','r').read()
			sql=sql.replace('@no@',str(ayar.no))
		if(mod=='y'):
			sql=open('./altyapi/sql/ayar_ekle.sql','r').read()
		if(mod in ['y','g']):	
			sql=sql.replace('@ayar_kulno@',str(ayar.kulno))
			sql=sql.replace('@ayar_bas@',str(ayar.bas))
			sql=sql.replace('@ayar_deger@',ayar.deger.encode('iso-8859_9'))
		if self.calis(sql)=="tamam":
			return self.ayar_liste()
	
	def ayar_liste(self,sonuc='html'):
		sql=open('./altyapi/sql/ayar_liste.sql','r').read()
		if sonuc=='html':
			rapor=statikrapor()
			rapor.sql(sql,rapbas='ayarlar',alt=1)
			return rapor.getHtml()
		else:
			row=self.calistir(sql)
			return row
		
	def ayar_getir(self,no):
		sql=open('./altyapi/sql/ayar_getir.sql','r').read()
		sql=sql.replace('@no@',str(no))
		row=self.calistir(sql)
		degerler=[]
		if row:
			vt_degerler=row[0]
			for vtd in vt_degerler:
				degerler.append(vtd)
		return degerler
			#row[0][3]=vt_degerler
			
			
	def ayar_al(self,kul_no,ayar_bas):
		sql=open('./altyapi/sql/ayar_al.sql','r').read()
		sql=sql.replace('@kul_no@',str(kul_no))
		sql=sql.replace('@ayar_bas@',str(ayar_bas))
		row=self.calistir(sql)
		if row:
			ayar_deger=row[0][0]
			if '#' in ayar_deger:
				ayar_deger=ayar_deger.split('#')
				degerler=[]
				for ayar in ayar_deger:
					degerler.append(ayar)
				return degerler
			return ayar_deger
		else:
			return None
		
	def vt_yedekle(self,vt_isim):
		now=str(datetime.datetime.now()).split()[0]
		os.system("mysqldump -u root -pmysql_1234 "+vt_isim+" > /opt/yedekler/giom_dbyedek/"+vt_isim+"_yedek_"+str(now)+".sql")
		os.system("mysqldump -u root -pmysql_1234 "+vt_isim+" > /opt/yedekler2/"+vt_isim+"_yedek_"+str(now)+".sql")
		return "kontrol ediniz"
	
	def vt_yukle(self,yedek_isim):
		os.system("mysql -u root -pmysql_1234 giomvt < giomvtyedek.sql")
		#gunzip -c test.sql.gz | mysql -u root -pmysql_1234 giomvt
		return "kontrol ediniz"
		
	def stkYxls2(self,stkno):
		#stkod,stkad,miktar,bf,tutar,stoklistno
		wb = xlwt.Workbook(encoding='latin-1')
		ws = wb.add_sheet(stkno)
		satir=1
		sutunlar=[0,1,2]
		basliklar=["isim","miktar","barkod"]
		harlist=self.stk_al(stkno)
		for sutun in sutunlar:
				data=basliklar[sutun]
				ws.write(satir-1,sutun,data)
		for kayit in harlist:
			for sutun in sutunlar:
				data=kayit[sutun+2]
				print data,satir,sutun
				if sutun==0:
					ws.write(satir,sutun,data)
					ws.col(sutun).width = 0x3600
				if sutun==2:
					ws.write(satir,sutun,self.stok(kayit[1]).barkod6)
					ws.col(sutun).width = 0x0f00
				if sutun==1:
					ws.write(satir,sutun,data)
			satir+=1
		wb.save('./stkYxls/stk_'+stkno+'.xls')
	
	def stkYxls(self,stknolar,dosya):
		#stkod,stkad,miktar,bf,tutar,stoklistno
		wb = xlwt.Workbook(encoding='latin-1')
		ws = wb.add_sheet("stklar")
		satir=1
		sutunlar=[0,1,2,3]
		basliklar=["isim","miktar","bf","tutar"]
		stklar=[]
		for stkno in stknolar:
			harlist=self.stk_al(stkno)	
			stklar.append(["-","-","-","-","toplam",""])
			stklar.append(["","",stkno,"-","-","-"])
			for har in harlist:
				#print har
				#stklar.append([har[2],har[3],har[4],har[5]])
				stklar.append(har)	
		for sutun in sutunlar:
				data=basliklar[sutun]
				ws.write(satir-1,sutun,data)
		for kayit in stklar:
			print kayit
			for sutun in sutunlar:
				data=kayit[sutun+2]
				#print data,satir,sutun
				if sutun==0:
					ws.write(satir,sutun,data)
					ws.col(sutun).width = 0x3600
				else :
					ws.write(satir,sutun,data)
			satir+=1
		wb.save('./stkYxls/'+dosya+'.xls')
	
	def terazi_data(self):
		sql=open('./altyapi/sql/terazi_data.sql','r').read()		
		row=self.calistir(sql)
		return row
	
	def teraziYxls(self):
		#stkod,stkad,miktar,bf,tutar,stoklistno
		wb = xlwt.Workbook(encoding='latin-1')
		ws = wb.add_sheet("PLU")
		satir=1
		basliklar="abcdefghijklmnoprstuvwqyzABCDEFGHIKLMNOPRSTUVYZQWX"
		for sutun in range(50):
			data=basliklar[sutun]
			ws.write(satir-1,sutun,data)
		kayitlar=self.terazi_data()
		for kayit in kayitlar:
			for sutun in range(50):
				#print kayit,satir,sutun
				if sutun==0 or sutun==2:
					ws.write(satir,sutun,"1")
				if sutun==1 or sutun==3:
					#barkod
					ws.write(satir,sutun,kayit[0])
				if sutun==4:
					#isim
					ws.write(satir,sutun,kayit[1])
					ws.col(sutun).width = 0x3000
				if sutun==17:
					#bf
					ws.write(satir,sutun,float(kayit[2])*100)
				if sutun in [5,6,13,19,21,22,23,25,26,28,31] or sutun>32:
					ws.write(satir,sutun,"")
				if sutun in [7,8,9,10,11,12,14,15,16,18,20,24,27,29,30,32]:
					ws.write(satir,sutun,"0")
			satir+=1
		wb.save('terazi_data.xls')
	
	def entegre(self):
		sql=open('./altyapi/sql/entegre.sql','r').read()
		#sql=sql.replace('@kul_no@',str(kul_no))
		#sql=sql.replace('@ayar_bas@',str(ayar_bas))
		row=self.calistir(sql)
		entegre=[]
		for ro in row:
			tarih=self.tarih_turk(str(ro[0]))
			fno=ro[1]
			isim=ro[2]
			vno=ro[3]
			tip=ro[10]
			kdv0=0
			mat1=ro[4]
			mat1=float(mat1)
			if mat1!=0:
				kdv0=1
				oran=1
				kdv1=ro[5]
				kdv1=float(kdv1)
				entegre.append([tarih,fno,isim,vno,oran,mat1,kdv1,mat1+kdv1,tip])
			mat8=ro[6]
			mat8=float(mat8)
			if mat8!=0:
				kdv0=1
				oran=8
				kdv8=ro[7]
				kdv8=float(kdv8)
				entegre.append([tarih,fno,isim,vno,oran,mat8,kdv8,mat8+kdv8,tip])
			mat18=ro[8]
			mat18=float(mat18)
			if mat18!=0:
				kdv0=1
				oran=18
				kdv18=ro[9]
				kdv18=float(kdv18)
				entegre.append([tarih,fno,isim,vno,oran,mat18,kdv18,mat18+kdv18,tip])
			if kdv0==0:
				oran=0
				mat0=ro[11]
				mat0=float(mat0)
				entegre.append([tarih,fno,isim,vno,oran,mat0,0,mat0,tip])
		wb = xlwt.Workbook(encoding='latin-1')
		ws = wb.add_sheet('entegre')
		satir=1
		sutunlar=[0,1,2,3,4,5,6,7,8]
		basliklar=["tarih","fatura no","cari isim","vergi numarasi","kdv orani","kdv matrah","kdvtop","kalem tutar","tip"]
		for sutun in sutunlar:
				data=basliklar[sutun]
				ws.write(satir-1,sutun,data)
		for kayit in entegre:
			for sutun in sutunlar:
				data=kayit[sutun]
				#print data
				if sutun==2:
					ws.write(satir,sutun,data)
				else:
					ws.write(satir,sutun,data)
				ws.col(sutun).width = 0x0f00
				if sutun==2:
					ws.col(sutun).width = 0x3600
			satir+=1
		wb.save('entegre_giom.xls')
		print "entegresyon tamam.->entegre_giom.xls"
		'''rapor=statikrapor()
		basliklar=["tarih","fatura no","cari isim","vergi numarasi","kdv orani","kdv matrah","kdvtop","kalem tutar","tip"]
		top_sutlar=[0,1]
		rapor_html=rapor.diziYhtml(entegre,basliklar,top_sutlar)
		return rapor_html'''
	
	def dizi_dekod(self,dizi):
		dekod=[]
		for d in dizi:
			yd=d
			if isinstance(d, str):
				yd=d
			dekod.append(yd)
		return dekod
	
	def etk_basim_kaydet(self,kod,bf):
		sqldosya='./altyapi/sql/etk_basim_kaydet.sql'
		sql=open(sqldosya,'r').read()
		sql=sql.replace('@kod@',str(kod))
		sql=sql.replace('@bf@',str(bf))
		sonuc=self.calis(sql)
		return sonuc
	
	def etk_basim_kontrol(self,kod,bf):
		bf=str(bf).replace(',','.')
		sqldosya='./altyapi/sql/etk_basim_kontrol.sql'
		sql=open(sqldosya,'r').read()
		sql=sql.replace('@kod@',str(kod))
		sql=sql.replace('@bf@',str(bf))
		sonuc=self.calistir(sql)
		if sonuc:
			return str(sonuc[0][0])
		else:
			return "yok"
	
	def bakim1(self,bakim,sonuc='html'):
		sql=""
		bakim=str(bakim)
		if bakim=="1":
			sql=open('./altyapi/sql/cift_inckey_tespit.sql','r').read()
		if bakim=="2":
			sql=open('./altyapi/sql/kontrol_tarih_uyumsuz.sql','r').read()
		if bakim=="3":
			sql=open('./altyapi/sql/tutar_toplam_uyumsuzlugu.sql','r').read()
		if sonuc=='html':
			rapor=statikrapor()
			rapor.sql(sql,rapbas='ayarlar',alt=1)
			return rapor.getHtml()
		else:
			row=self.calistir(sql)
			return row
	
	def stk_shsifirlama(self,stkno,merkezkod,carikod,caribag=""):
		con = lite.connect("stoklist.db")
		sqldosya='./altyapi/sql/sube_giren_mallar.sql'
		sql=open(sqldosya,'r').read()
		sql=sql.replace('@carikod@',str(carikod))
		sql=sql.replace('@merkezkod@',str(merkezkod))
		sonuc=self.calistir(sql)
		maltum=[]
		for son in sonuc:
			maltum.append(son)
		stkhar=self.stk_al(stkno)
		stkodlar=[]
		for kod in stkhar:
			stkodlar.append(kod[1])		
		with con:
			
			cur = con.cursor()
			for mal in maltum:
				stkod=mal[0]
				if stkod not in stkodlar:
					stkad=mal[1]
					if caribag=="":
						bf=self.stok(stkod).satis_fiat1
					else:
						bf=self.sonsatis_bf(carikod,caribag,stkod)	
					stharek=(stkod,stkad,float(0),float(bf),float(0),stkno)
					cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stharek)
				
		con.close()
		
		return "tm"
