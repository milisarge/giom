# -*- coding: utf-8 -*-

import datetime
#import MySQLdb as mdb
import pymysql
import sys,time
import decimal
from mysql_ayar import *

class statikrapor:
	
	global baglanti
	baglanti=MysqlBaglanti()
	
	col_names=[]
	stoklistvt='stoklist.db'
	html=""
	deger=0
	sirano=1
	def __init__(self):
		#self.html="<META http-equiv=content-type content=text/html;charset=windows-1254>"
		self.html=""
		self.deger=0.0
		self.data = []	
		
	def tabloekle(self):	
		#self.html+="<table border=1>"+"\n"
		self.html+="<table id='hareketrapor' border=1 class='tablesorter' ><thead>"+"\n"
	def tablobitir(self):
		self.html+="</tbody></table>"+"\n"
	def satirekle(self,noekle=0):
		if noekle==0:
			self.html+="<tr align='left'>"+"\n"
		else:
			self.html+="<tr align='left'><td>"+str(self.sirano)+"</td>"+"\n"
			self.sirano+=1
	def satirbitir(self):
		self.html+="</tr>"+"\n"
	def sutunekle(self,string):
		if "href" in string  or "input" in string:
			self.html+="<td><font color='black'>"+string+"</font></td>"+"\n"
		else:
			self.html+="<td id=pano_kopya@"+string+"><font color='black'>"+string+"</font></td>"+"\n"
	def sutunac(self):
		self.html+="<td>"+"\n"
	def thsutunekle(self,string):
		self.html+="<th align='left'><font color=#003366>"+string+"</font></th>"+"\n"
	def sutunbitir(self):
		self.html+="</td>"+"\n"
	def tablo_baslik_bitir(self):
		self.html+="</thead><tbody>"+"\n"
	def tablobaslik(self,basliklar):
		self.satirekle()
		for baslik in basliklar:
			self.sutunekle(str(baslik))
		self.satirbitir()
	def linkekle(self,link,linkbas,yukle,sil):
		self.sutunekle("<a id=sisLink href="+link+">"+linkbas+"</a><p>")	
		#17:52 26.10.2014
		if yukle!="":
			#self.sutunekle("<div id="+"yukle"+"@"+linkbas+" ><img src='static/yukle.jpeg' alt=''></div><p>")
			self.sutunekle("<input type='image' src='back16.png' name='"+yukle+"@"+linkbas+"' id='"+yukle+"@"+linkbas+"' value='<--' style='margin-left:5px;margin-right:0px; margin-top:0px;' />")
		if sil!="":
			#self.sutunekle("<div id="+"sil"+"@"+linkbas+" >sil</div><p>")
			self.sutunekle("<input type='image' src='delete16.png' name='"+sil+"@"+linkbas+"' id='"+sil+"@"+linkbas+"' value='X' style='margin-left:5px;margin-right:0px; margin-top:0px;' />")
		
		#16:38 26.10.2014 kapandi
		#self.sutunekle("<a href="+link+">"+linkbas+"</a><p>")	
		#self.divekle("deneme",linkbas)

	def sql(self,sqlstr,rapbas="rapor",tabbas=[],alt="sayac",link="",sqlitero=None,colnam=None,yukle="",sil="",topsut=[],noekle=0):		
		alttoplam=[]#[0,0,0,0,0,0,0,0,0,0,0,0,0]
		ekolon_sayi=0
		for j in range(0,len(topsut)):
			alttoplam.append(0)
		
		if(sqlitero!=None):
			rows=sqlitero
			self.col_names = colnam
		else:
			ta=time.clock()
			rows =self.calistir(sqlstr)
			tm=time.clock()
			print "htmlrapor.py sql calisma hizi:",tm-ta
		if(rows is None):
			return None
		#sonuc tablosunun eklenmesi
		self.tabloekle()		
		#rapor baslik eklenmesi
		self.satirekle()
		if(alt is "bag"):
			self.linkekle(link,rapbas)
		else:
			self.sutunekle(rapbas)
		self.satirbitir()
		self.tablobaslik(tabbas)
		#col_names = [cn[0] for cn in cursor.description]
		self.satirekle()
		if noekle==1:
			self.thsutunekle("no")
		for sutoba in self.col_names:	
			self.thsutunekle(sutoba)
		if yukle!="":
			self.thsutunekle("yukle")
			ekolon_sayi+=1
			#self.sutunekle("<input type='submit' name='"+"yukle@"+linkbas+"' id='"+"yukle@"+linkbas+"' value='<--' style='margin-left:20px;margin-right:20px; margin-top:10px;' />")
		if sil!="":
			self.thsutunekle("sil")
			ekolon_sayi+=1
			#self.sutunekle("<input type='submit' name='"+"sil@"+linkbas+"' id='"+"sil@"+linkbas+"' value='X' style='margin-left:20px;margin-right:20px; margin-top:10px;' />")
		self.satirbitir()
		self.tablo_baslik_bitir()
		s=0
		for rowx in rows:
			s+=1
			if noekle==1:
				self.satirekle(1)
			else:
				self.satirekle()
			for baslik in range(0,len(rowx)):
				self.deger=rowx[baslik]
				if(self.deger is None):
					self.deger=""
				if(type(self.deger) in [datetime.date,datetime.datetime,decimal.Decimal,int,float,long]):
					if(type(self.deger) is int or type(self.deger) is float or type(self.deger) is decimal.Decimal):	
						if baslik in topsut:
							alttoplam[baslik]+=float(self.deger)
					self.deger=str(self.deger)
				if(link!="" and self.col_names[baslik] in link):
					self.linkekle(link+"="+self.deger,self.deger,yukle,sil)
				else:
					self.sutunekle(self.deger)					
			self.satirbitir()
		#alttoplam ekleme	
		self.satirekle()
		if noekle==1:
			self.sutunekle("-")
		for i in range(0,len(self.col_names)+ekolon_sayi):
			if i in topsut:
				self.sutunekle(str(alttoplam[i]))
			else:
				self.sutunekle('-')
		self.satirbitir()
		
		if(alt is "sayac"):
			self.satirekle()
			self.sutunekle(str(s)+" kayit")
			self.satirbitir()
		self.tablobitir()
	
	def getHtml(self):
		return self.html
		#return "<html><div id='printableArea'>"+self.html+"</div></html>"
	def getdosHtml(self,dosya):
		self.html=""
		with open(dosya) as f:
			content = f.readlines()
		self.tabloekle()
		for row in content:
			self.satirekle()
			hareket=row.split('@')
			for atom in hareket:
				self.sutunekle(atom)
			self.satirbitir()
		self.tablobitir()
		return "<html>"+self.html+"</html>"
	def getHrkt(self,dosya):
		hareketler=[[]]
		with open(dosya) as f:
			content = f.readlines()
		
		for row in content:
			row=row.split('@')
			hareketler.append(row)
			
		return hareketler
	def getlisteHtml(self,liste):
		#self.html=""
		self.tabloekle()
		for row in liste:
			self.satirekle()
			#self.sutunekle(row[2])#stkod
			self.sutunekle("<a href=http://192.168.1.254:5000/halis/"+row[2]+">"+row[2]+"</a>")
			self.sutunekle(row[4])#stkad
			self.sutunekle(row[54])#barkod1
			self.sutunekle(row[55])#barkod2
			self.sutunekle(row[56])#barkod3
			self.satirbitir()
		self.tablobitir()
		#return "<html>"+self.html+"</html>"	
		return self.html
	
	def getlisteHtml_test(self,liste):
		#self.html=""
		self.tabloekle()
		for row in liste:
			self.satirekle()
			self.sutunekle(str(row[0]))
			self.sutunekle(row[1])
			self.sutunekle(row[2])
			self.sutunekle(str(row[3]))
			self.sutunekle(str(row[4]))
			self.sutunekle(str(row[5]))
			self.sutunekle(str(row[6]))
			self.sutunekle(str(row[7]))
			self.sutunekle(str(row[8]))
			self.satirbitir()
		self.tablobitir()
		#return "<html>"+self.html+"</html>"	
		return self.html
	
	def diziYhtml(self,dizi,dizibas,topsut=[]):
		alttoplam=[]
		for j in range(0,len(topsut)):
			alttoplam.append(0)
		self.tabloekle()
		#self.tablobaslik(dizibas)
		for bas in dizibas:
			self.thsutunekle(bas)
		self.tablo_baslik_bitir()
		for row in dizi:
			self.satirekle()
			for i in range(0,len(row)):
				deger=row[i]
				if(type(deger) is int or type(deger) is float or type(deger) is decimal.Decimal):	
					if i in topsut:
						alttoplam[i]+=deger
				self.sutunekle(str(deger))
			self.satirbitir()
		#alttoplam ekleme	
		self.satirekle()
		for i in range(0,len(dizibas)):
			if i in topsut:
				self.sutunekle(str(alttoplam[i]))
			else:
				self.sutunekle('-')
		self.satirbitir()
		self.tablobitir()
		return self.html
	
	def calistir(self,sql):
		sqlparca=""
		con=""
		try:
			con = pymysql.connect(baglanti.host, baglanti.kullanici,baglanti.sifre,baglanti.vt,charset='latin5')
			#con.set_character_set('latin5')
			cur = con.cursor()
			#print "htmlrapor.py-baglanti acildi"
			sql=sql.split(';')
			for sqlparca in sql:
				cur.execute(sqlparca)
				rows = cur.fetchall()
				if(rows):
					self.col_names = [i[0] for i in cur.description]
					#print col_names
					rows=list(rows)
					if con:    
						#print "htmlrapor.py-baglanti kapandi-select islemi"
						con.close()	
					return rows	
			if con:    
				print "htmlrapor.py-baglanti kapandi-select islemi"
				con.close()	
			#00:23 06.02.2014
		except :
			print "htmlrapor.py-HATA:",str(sys.exc_info()[1])
			if con:    
				#print "htmlrapor.py-baglanti kapandi-select islemi"
				con.close()
