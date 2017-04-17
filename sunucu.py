#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os,time
import copy
import json
from flask import Flask, url_for
from flask import g
from flask import render_template #render yapmak icin
from flask import request 
from flask import Flask, current_app
import werkzeug 
from werkzeug.datastructures import ImmutableMultiDict
from flask import Flask,jsonify, request, Response, session,g,redirect, url_for,abort, render_template, flash
from htmlrapor import *
from mysqlmak import * 
from fatura import * 
from cari import * 
from kullanici import * 
from genelfonks import * 
from termalsab import *
from yetkilendirme import * 
from tblsthar import * 
from uyesatislari import *
import sqlite3 as lite
import dizayn
import codecs
import random
import md5
import ctypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from logging.handlers import RotatingFileHandler 
#from sayidan_yaziya import cevir
#from uyesatislari import *
from iniparse import INIConfig
from iniparse import ConfigParser
import subprocess
import math
from logcu import *
import xlrd
import datetime
import socket
import platform

# configuration
platform=platform.system()
DEBUG = True
SECRET_KEY = 'D3xvb2Gl'
USERNAME = 'giomkull'
PASSWORD = 'giomsifre***'
KULL_ID=-1
LOGGED='hayir'
ADMINMI='hayir'
ICERIK=''
YENISQL='yeni.sql'
DZNDOSYA='serbest.xsql'
INIDOSYA=''
AYARDIZIN='.\sql\\'
UPLOAD_FOLDER = '.\YUKLEMELER\\'
EXNET_FOLDER = '.\exnet\DATA\\'
STKOD=''
KDVDURUM=None
STOKLIST="bos"
STOK=[]
kriter="NULL"
arama=''
STHARSIRA='yeni'
fisno=""
ftip=""
merkez='28'

mak=mysqlmak()
arge=Arge()
yetki=Yetki()
kull=Kullanici()
kull.no="ws"
kull.isim="sss"
l=Logcu()
kullanici=ConfigParser()
kullanici.read('./ayarlar/kullanici.ini')
DATABASE = mak.ayar_al('999','stoklist_db')

etoku_dizin=mak.ayar_al('999','etoku_dizin')
db_dizin=mak.ayar_al('999','db_dizin')
etodizin="etablo"
etoku_komut="etoku\\etYstk.py "
stkdb_yedekal_komut='copy stoklist.db.yedek stoklist.db'
stkdb_yedekle_komut='copy stoklist.db stoklist.db.yedek'
lazeryaz_komut="lazer_yazici.py f "
lazeryaz_komut2="lazer_yazici.py s "
etkyazdir_komut="etk_lzyazdir.bat"
tasima_komutu="move "
kopya_komutu="copy "
ayrac="\\"
if platform=='Linux':
	etoku_dizin="etoku/DATA/"
	db_dizin="stk_yedek"
	etoku_komut="python etoku/etYstk.py "
	stkdb_yedekal_komut='cp stoklist.db.yedek stoklist.db'
	stkdb_yedekle_komut='cp stoklist.db stoklist.db.yedek'
	lazeryaz_komut="python lazer_yazici.py f "
	lazeryaz_komut2="python lazer_yazici.py s "
	etkyazdir_komut="etk_lzyazdir.sh"
	tasima_komutu="mv "
	kopya_komutu="cp "
	ayrac="/"

app = Flask(__name__)
app.config.from_object(__name__)

#@app.before_request
#def log_request():
	#print mak.girdi_isim(session['KULL_ID'])
	#print request.headers
	#print request.remote_addr
#	print "xxxx",request.headers.getlist("Connection")

@app.errorhandler(404)
def notfound_error(exception):
	app.logger.info(exception)
	#return "404"
	return "gecersiz bir sayfa girdiniz."
	#return render_template('404.html')

@app.errorhandler(500)
def internal_error(exception):
	app.logger.info(exception)
	return "500"
	
@app.route('/')
def anasayfa():
	if "KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) :
			ip="tanimsiz"
			if not request.headers.getlist("X-Forwarded-For"):
				ip = request.remote_addr
			else:
				ip = request.headers.getlist("X-Forwarded-For")[0]
			bilgiler=""
			g_isim=mak.girdi_isim(session['KULL_ID'])
			bilgiler+="<p>"+"erişim ip: ".decode("utf-8")+ip
			os.system("uname -a > bilgiler")
			bilgiler+="<p>"+"erişim kullanıcısı: ".decode("utf-8")+g_isim
			bilgiler+="<p>"+"sunucu makine:   "
			bilgiler+=open("bilgiler","r").read()
			bilgiler+="<p>"+"mysql sunucu ip:   "
			bilgiler+=MysqlBaglanti.host #open("mysql_ayar.py","r").read()
			return render_template('anasayfa.html')+bilgiler
	return redirect(url_for('giris'))

@app.route('/giris', methods=['GET', 'POST'])
def giris():
	onay='yok'
	ip="tanimsiz"
	session["KULL_ID"]=-1
	if not request.headers.getlist("X-Forwarded-For"):
		ip = request.remote_addr
	else:
		ip = request.headers.getlist("X-Forwarded-For")[0]
	error = None
	#yetkili ipler
	if(ip in ["192.168.1.299"]):session["ID"]=99
	if request.method == 'POST':
		open("./log/giris.log","a").write(str(datetime.datetime.now())[0:19]+"   -   "+ip+"   -   "+request.form['username']+"/"+request.form['password']+"\n")
		isim=request.form['username']
		sifre=request.form['password']
		id=mak.giris_kontrol(isim,sifre)
		if(id):
			if mak.girdi_kontrol(id) is None:
				mak.giris_ekle(id)
			session['KULL_ID']=id
			return render_template('anasayfa.html')+"KULLANICI IP: "+ip
				
	return render_template('giris.html', error=error)+"KULLANICI IP: "+ip
	

@app.route('/exit')
def exit():
	session['LOGGED']='hayir'
	mak.giris_sil(session['KULL_ID'])
	session['KULL_ID']=-1
	return render_template('giris.html')
	
@app.route('/temp')
def sayfa1(): 
    return '''<html>
	<h2>DENEME SAYFASI</h2>
	<a href="../">ANA SAYFA</a> </html>'''

@app.route('/s2')
def s2():
	if "KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']):
		app.logger.info(mak.girdi_isim(session['KULL_ID']))
		return '''<html><h2>DENEME SAYFASI</h2><a href="../">ANA SAYFA</a> </html>'''
	else:
		return render_template('giris.html')
	
@app.route('/dys',methods=['GET', 'POST'])
def dys():
	if request.method == 'POST':
		file = request.files['file']
		if file:
			mimetype = file.content_type
			filename = werkzeug.secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return "dosya yuklendi"
	return render_template('dys.html')
	
@app.route('/add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	print a,b
	return jsonify(result=a + b)

@app.route('/hareket')
def hareket():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		return render_template('hareket.html')	
	return render_template('giris.html',error='isim ve sifre giriniz!!!')	

@app.route('/otokod',methods=['GET', 'POST'])
def otokod():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		if request.method == 'POST':
			if request.form["komut"] == "KULANICI SERVIS YENILEME" :
				os.system(".\otokod\KULLANICI.bat")
				return "KOMUT YERINE GETIRILDI.KONTROL EDINIZ!!!"+"<br><a href=./otokod>GERI DON</a>"	
		return render_template('otokod.html')	
	return render_template('giris.html',error='isim ve sifre giriniz!!!')	

@app.route('/exnet',methods=['GET', 'POST'])
def exnet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		if request.method == 'POST':
			file = request.files['file']
			if file:
				mimetype = file.content_type
				filename = werkzeug.secure_filename(file.filename)
				file_konum=os.path.join(app.config['EXNET_FOLDER'], filename)
				file.save(file_konum)
				
				file2 = request.files['file2']
				if file2:
					mimetype = file2.content_type
					filename2 = werkzeug.secure_filename(file2.filename)
					file_konum2=os.path.join(app.config['EXNET_FOLDER'], filename2)
					file2.save(file_konum2)
					os.system(".\exnet\exnet.py "+file_konum2)
					#subprocess.call([".\exnet\exnet.py "+file_konum2,"exnet.log"])
					return "EXCEL VERI AKTARIMI YAPILDI!!!"+"<br><a href=./exnet>GERI DON</a>"	
				else:
					return "ini ayar dosya secin"
			else:
				return "excel veri dosya secin"
		return render_template('exnet.html')	
	return render_template('giris.html',error='isim ve sifre giriniz!!!')

	
@app.route('/karsilama/')
@app.route('/karsilama/<name>')
def karsilama(name=None):
    return render_template('karsilama.html', name=name)

@app.route('/yetkili')
def yetkili():
	if(session['ADMINMI'] is "EVET" ):
		return '''<html>
		<h2>admin bolgesi</h2>
		<a href="../">ana sayfa</a> </html>'''	
	return redirect(url_for('login'))
		
@app.route('/login', methods=['GET', 'POST'])
def login():
	
	ip="tanimsiz"
	if not request.headers.getlist("X-Forwarded-For"):
		ip = request.remote_addr
	else:
		ip = request.headers.getlist("X-Forwarded-For")[0]
	error = None
	#yetkili ipler
	if(ip in ["192.168.1.299"]):session["LOGGED"]="EVET"
	if request.method == 'POST':
		open("./log/giris.log","a").write(str(datetime.datetime.now())[0:19]+"   -   "+ip+"   -   "+request.form['username']+"/"+request.form['password']+"\n")
		if request.form['username'] != app.config['USERNAME']:
			error = 'kayit disi isim'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'kayit disi sifre'
		else:
			session["LOGGED"]="EVET"
			#return karsilama(session['USERNAME'])
			return render_template('anasayfa.html')+"KULLANICI IP: "+ip
	return render_template('giris.html', error=error)+"KULLANICI IP: "+ip
	
	


	
@app.route('/editor', methods=['GET', 'POST'])
def editor():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		if not DZNDOSYA in session:
			session['DZNDOSYA']='serbest.xsql'
		
		dosyalar=os.listdir(app.config["AYARDIZIN"])
		if(os.path.isfile(app.config["AYARDIZIN"]+session["DZNDOSYA"])):
			gelensql = open(app.config["AYARDIZIN"]+session["DZNDOSYA"], 'r').read()
		if request.method == 'POST':
			session["DZNDOSYA"]=request.form['sqldosyasi']
			session["ICERIK"]=request.form['sqlcumlesi']
			if request.form["komut"] == "sec" :
				app.config["AYARDIZIN"]=request.form['ayardizini']
				dosyalar=os.listdir(app.config["AYARDIZIN"])
				return render_template('editor.html', gonderilen=session["ICERIK"],dosyalar=dosyalar,akdos=session["DZNDOSYA"])
			if request.form["komut"] == "kaydet" and session["ICERIK"]!="":
				f = open(app.config["AYARDIZIN"]+session["DZNDOSYA"],'w')
				f.write(session["ICERIK"])
				return render_template('editor.html', gonderilen=session["ICERIK"],dosyalar=dosyalar,akdos=session["DZNDOSYA"])
			if request.form["komut"] == "yenikaydet" and session["ICERIK"]!="" :
				session["YENISQL"]=request.form['yenidosya']
				if session["ICERIK"]!="" :
					f = open(app.config["AYARDIZIN"]+session["YENISQL"],'w')
					f.write(session["ICERIK"])
					dosyalar=os.listdir(app.config["AYARDIZIN"])
					return render_template('editor.html', gonderilen=session["ICERIK"],dosyalar=dosyalar,akdos=session["DZNDOSYA"])
			if request.form["komut"] == "calistir" and session["ICERIK"]!="":
				t0 = time.clock()
				rapor=htmlrapor()
				rapor.sql(session["ICERIK"])
				islemhizi="{:10.3f}".format(time.clock()-t0)
				
				#return  render_template('editor.html', gonderilen=gelensql,sonuc=rapor.getHtml())
				return  render_template('editor.html',islemhizi=islemhizi, gonderilen=session["ICERIK"],dosyalar=dosyalar,akdos=session["DZNDOSYA"])+rapor.getHtml()
			if request.form["komut"] == "yukle" and session["ICERIK"]!="":
				session["DZNDOSYA"]=request.form['sqldosyasi']
				if(os.path.isfile(app.config["AYARDIZIN"]+session["DZNDOSYA"])):
					gelensql = open(app.config["AYARDIZIN"]+session["DZNDOSYA"], 'r').read()
				return render_template('editor.html',gonderilen=gelensql,dosyalar=dosyalar,akdos=session["DZNDOSYA"])
			if request.form["komut"] == "sil" :
				session["DZNDOSYA"]=request.form['sqldosyasi']
				os.remove(app.config["AYARDIZIN"]+session["DZNDOSYA"])
				session["DZNDOSYA"]="yeni.sql"
				dosyalar=os.listdir(app.config["AYARDIZIN"])
				return render_template('editor.html',gonderilen=session["ICERIK"],dosyalar=dosyalar,akdos=session["DZNDOSYA"])
		return render_template('editor.html', gonderilen=gelensql,dosyalar=dosyalar,akdos=session["DZNDOSYA"])
	
	return render_template('giris.html', error="isim ve sifre giriniz")


@app.route('/sql')		
def sql():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		rapor=htmlrapor()
		rapor.sql("select * from dp_otospr where osn='tdm'")
		#rapor.sqldosya("a")
		#print "sql icinde"
		print "deger-->",rapor.deger
		return  '''<a href="../">ana sayfa</a><br> '''+rapor.getHtml()
		'''<html>
		<h2>sql server sahifesi</h2>
		<a href="../">ana sayfa</a> </html>'''
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/raporlama/', methods=['GET', 'POST'])
@app.route('/raporlama/<sayfa>')
def raporlama(sayfa="ana.html"):
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		ayarlar=os.listdir(".\ini")
		t0 = time.clock()
		rapor1=rapor()
		if(session["INIDOSYA"] is ''):
			session["INIDOSYA"]=ayarlar[0]
		if request.method == 'POST':
			if request.form["komut"] == "raporla" :
				session["INIDOSYA"]=request.form['inidosyasi']
			if request.form["komut"] == "ayarla" :
				session["INIDOSYA"]=request.form['inidosyasi']
		rapor1.ayar_yukle(session["INIDOSYA"])
		rapor1.bitir()
		rapordos=open("rapor\\"+sayfa, 'r').read()
		ishiz="{:10.2f}".format(time.clock()-t0)
		return render_template('raporayar.html',dosyalar=ayarlar,iniakdos=session["INIDOSYA"])\
		+'''<html>islem hizi:'''+ishiz+'''<br><html>'''\
		+rapordos+"<br><a href=./>geri<a>"+"<br><a href=../>ana sayfa</a>"
	return render_template('giris.html', error="isim ve sifre giriniz")
	
	
@app.route('/uyesatislari', methods=['GET', 'POST'])
def uyesatislari():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fisler = []
		pos_dizin=mak.ayar_al('999','pos_dizin')+"\\AYLIK\\"
		if request.method == 'POST':
			if "submit_box" in request.form and "uye_no" in request.form :
				dosyayolu = pos_dizin + request.form["ay"] + ".GTF"
				uyeno = request.form["uye_no"]
				toplamAlisveris = 0
				gtfDosya = open(dosyayolu, "r")
				if gtfDosya :
					gtfsatir = gtfDosya.readline()
					gtfsatir = gtfDosya.readline()
					while gtfsatir:
						# satirin basindaki karaktere gore islem yapilacak
						# 1 ise fis baslangÃƒÂ¯Ã‚Â¿Ã‚Â½cÃƒÂ¯Ã‚Â¿Ã‚Â½'''
						if gtfsatir[1] == "1" :
						    # tarih ve uye numarasina bakmak icin ilk satiri parcaliyoruz '''
						    gtfparcali = gtfsatir.split()
						    ''' uye no karsilasitirmasi. tutuyorsa fisi olustur '''
						    if gtfparcali[19] == uyeno :
								
								''' fisi oluÃƒÂ¯Ã‚Â¿Ã‚Â½tururken tarih ve saati de fise ekliyoruz '''
								tempsaat = gtfparcali[4][0:2] +  ":" + gtfparcali[4][2:4] + ":" + gtfparcali[4][4:]
								fis = Fis(gtfparcali[2], tempsaat, 0, [])
								
								''' fise kaydedilecek urunleri okuyacaz, 2 ile baslayan sira '''
								while 1:
									gtfsatir = gtfDosya.readline()
									
									''' fiste urun var demektir, urunler fise eklenecek '''
									if gtfsatir[1] == "2" :
										urunsatiri = gtfsatir.split()
										urunkodu =  urunsatiri[2]
										
										stok = mak.stok(urunkodu)
										print "kod:",urunkodu
										urunismi = stok.isim
										miktar = urunsatiri[6]
										birim = ""
										if urunsatiri[7][0] == "0" :
											birim = "AD"
										elif urunsatiri[7][0] == "1" :
											birim = "GR"
										birimfiyat = urunsatiri[7][1:]
										# iptal satırlarını bulduruyor.
										tutar = ""
										if urunsatiri[3][0] == "1" :
											tutar = "-" + urunsatiri[8]
										else :
											tutar = urunsatiri[8]
										
										''' fisteki urunlerin toplam tutari hesaplanacak '''
										fis.toplamtutar += float(tutar.replace(",", "."))
										
										urun = Urun(urunkodu, urunismi, miktar, birim, birimfiyat, tutar)
										fis.urunler.append(urun)
										
									elif gtfsatir[1] == "6" :
										''' fiste urunler bitti ( 6 ile baslıyorsa fis sonu geldi) '''
										''' fis tamamlandi. toplam tutar, urunler, tarih ve saat '''
										''' olusturulan fis uye fislerine eklenecek '''
										toplamAlisveris += fis.toplamtutar
										fisler.append(fis)
										del fis
										break
									
									elif gtfsatir[1] == "1" :
										del fis
										break
						''' dosyadan okumaya devam et '''
						gtfsatir = gtfDosya.readline()
				
				''' yazilan fisleri 
				for temp1 in fisler :
					print "---------------------------------------------------"
					print "fis: ->tarih:" + temp1.tarih + "   saat:" + temp1.saat
					for temp2 in temp1.urunler :
						print temp2.urunkodu + "    " + temp2.urunismi + "   " + temp2.miktar + "   " + temp2.tutar
					print "fis toplamtutar:" + str(temp1.toplamtutar)
				'''
				
				return render_template("uyesatislari.html", fisler=fisler, toplamAlisveris=toplamAlisveris)
		else :
			return render_template("uyesatislari.html")
	
	return render_template('giris.html', error="isim ve sifre giriniz")		
	

@app.route('/faturaDetay', methods=['GET', 'POST'])
def faturaDetay():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		rapor=""
		raporbas=""
		if('fkod' in request.args):
			fkod=request.args.get('fkod')
			raporbas=mak.sthar_detay_baslik(fkod,link='/faturaDetay?fkodstk',sonuc='html')
			rapor=mak.sthar_detay(fkod,sonuc='html')
			irsrapor=mak.fatura_irsler(fkod,sonuc='html')
			kytrapor=mak.fatura_kayitbilgi(fkod,sonuc='html')
		if('fkodstk' in request.args):
			fkodstk=request.args.get('fkodstk')
			sonuc=mak.stharYstk(fkodstk)
			if(sonuc=="olumsuz"):
				return "stk çevrimi olumsuz!"
			else:
				return redirect(url_for('faturaModul'))
		return render_template('faturaDetay.html')+raporbas+"<br>"+rapor+"<br>"+irsrapor+"<br>"+kytrapor		
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/faturaYardim', methods=['GET', 'POST'])
def faturaYardim():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		return render_template('faturaYardim.html')
	return render_template('giris.html', error="isim ve sifre giriniz")	
@app.route('/faturaModul', methods=['GET', 'POST'])
def faturaModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		if('fkod' in request.args):
			fkod=request.args.get('fkod')
			islem_turu=mak.fatura_islemturu(fkod)
			if(islem_turu=='F'):
				return redirect(url_for('faturaDetay', fkod=fkod))
			else:
				data=mak.sthar_detay_baslik(fkod,sonuc='dizi')	
		error = None
		stkod = ''
		stkad = ''
		bf='0'
		con = lite.connect(app.config["DATABASE"])
		#cabuk faturalastirma eklentisi
		if not 'merkezsube' in session:
			session['merkezsube']='28'
		if not 'transsube' in session:
			session['transsube']='28'
		if not 'fattip' in session:
			session['fattip']='DAT'
		if not 'urtkod' in session:
			session['urtkod']=''	
		if not kriter in session:
			session['kriter']='STOK_ADI'
		if not arama in session:
			session['arama']=''
		if not KDVDURUM in session:
			session["KDVDURUM"]=None
		if not STKOD in session:
			session["STKOD"]=''
		if not STOKLIST in session:
			session["STOKLIST"]="bos"
		hardos = mak.stk_list_al()
		kull=mak.kullanici_getir2(session["KULL_ID"])
		print kull+" fatura modulunu yeniledi."
		kayanlar=mak.ayar_al('999','kayan_yazilar')
		return render_template('faturaModul.html',kullanici=kull, hardos=hardos,stok="",kayanlar=kayanlar)
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/yeniSTkHarList', methods=['GET', 'POST'])
def yeniSTkHarList():
	stkno=str(random.randrange(1,1000))+".stk"
	while(mak.stkno_kontrol(stkno)):
		stkno=str(random.randrange(1,1000))+".stk"
	return stkno

@app.route('/stkSatirSil', methods=['GET', 'POST'])
def stkSatirSil():
	print request.form
	sirano="yok"
	stoklist=""
	if request.form["modulAd"] =='fatura':
		sirano=request.form["stksira"]
		if "stkHarList" in request.form:
			stoklist=request.form["stkHarList"]
	if request.form["modulAd"] =='sayim':
		sirano=request.form["guncelsira"]
	if request.form["modulAd"] =='siparis':	
		sirano=request.form["stksira"]
		stksecim="spr"+request.form["stksecim"]
		stoklist=request.form[stksecim]
	mak.stk_satsil(sirano)
	stokTablosu=mak.stk_bilgi(stoklist)
	return Response(json.dumps(stokTablosu),mimetype='application/json')
	
@app.route('/stkHarListGetir', methods=['GET', 'POST'])
def stkHarListGetir():
	bx=datetime.datetime.now()
	if('stksecim' in request.form):
		stksecim=request.form["stksecim"]
		if(stksecim=='stk1'):
			stoklist=request.form['sprstk1']
		if(stksecim=='stk2'):
			stoklist=request.form['sprstk2']
		if(stksecim=='no'):
			stoklist=request.form['sprno']
		if(stksecim=='sayimstk'):
			stoklist=request.form['stklist']
	else:
		stoklist=request.form["stkHarList"]
	stokTablosu=mak.stk_bilgi(stoklist)
	by=datetime.datetime.now()
	print "stk getirme sn:",(by-bx).total_seconds()
	return Response(json.dumps(stokTablosu),  mimetype='application/json')


@app.route('/stkTanimGetir', methods=['GET', 'POST'])
def stkTanimGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		if('stkno' in request.args):
			data=None
			stkno=request.args.get('stkno')
			stk_ayar="@stk_"+stkno
			stkayr=mak.ayar_al('999',stk_ayar)
			if stkayr:	
				data=[]
				kaynak=stkayr[0]
				data.append(kaynak)
				hedef=stkayr[1]
				data.append(hedef)
				gctur=stkayr[2]
				data.append(gctur)
		return Response(json.dumps(data), mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")		

	
@app.route('/sthEkle', methods=['GET', 'POST'])
def sthEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		durum="sthbilgi"
		stkod=request.form['kod']
		if(stkod is not ""):
			fisno=request.form['sthFisno']
			miktar=str(request.form['sthMiktar']).replace(',','.')
			tarih=request.form['sthTarih']
			bf=str(request.form['satis_fiat3']).replace(',','.')
			olcubr=request.form['olcubr1']
			kaynak=str(request.form['gozcari']).split('@')[1]
			mak.sth_ekle(kaynak,fisno,tarih,stkod,miktar,olcubr,bf)	
			durum=mak.sthar_bilgi(stkod,kaynak)
		else:
			durum="stok kodu boş olamaz"
		return Response(json.dumps(durum),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")		
	
@app.route('/sthSil2', methods=['GET', 'POST'])
def sthSil2():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="olumsuz"
		sthkod=request.args.get('sthkod')
		sthar=mak.sth_yukle(sthkod)
		if sthar.finckeyno==0 or sthar.finckeyno==-1:
			mak.sth_sil(sthar.incno)
			data="hareket silindi"
		else:
			data="fatura içi hareket silinemez."
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/sthSil', methods=['GET', 'POST'])
def sthSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sthTablo="x"
		merkez=""
		fisno=""
		if('sthkod' in request.form):
			sthkod=request.form["sthkod"]
			if('stksecim' in request.form):
				stksecim=request.form["stksecim"]
				if('merkeznokta' in request.form):
					merkez=request.form["merkeznokta"]
					merkez=merkez.split('@')[1]
					if(stksecim=='sth1'):
						fisno=request.form['spr1fis']
					if(stksecim=='sth2'):
						fisno=request.form['spr2fis']
					sthar=mak.sth_yukle(sthkod)
					mak.fat_sth_islem(sthar,'s')
		sthTablo=mak.sth_bilgi(merkez,fisno,sonuc='html')
		return Response(json.dumps(sthTablo),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")		
	
@app.route('/sthGetir', methods=['GET', 'POST'])
def sthGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		merkez=""
		fisno=""
		if('stksecim' in request.form):
			stksecim=request.form["stksecim"]
			if('merkeznokta' in request.form):
				merkez=request.form["merkeznokta"]
				merkez=merkez.split('@')[1]
				if(stksecim=='sth1'):
					fisno=request.form['spr1fis']
				if(stksecim=='sth2'):
					fisno=request.form['spr2fis']
		sthTablo=mak.sth_bilgi(merkez,fisno,sonuc='html')
		return Response(json.dumps(sthTablo),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/stkSiraAl', methods=['GET', 'POST'])
def stkSiraAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklist=request.args.get('stkno')
		data=mak.stk_sira_al(stoklist)
		return Response(json.dumps(data),  mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
@app.route('/stkHarAl', methods=['GET', 'POST'])
def stkHarAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		guncelsira=request.args.get('guncelsira')
		data=mak.stk_har_al(guncelsira)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")		
@app.route('/stkFsbAl', methods=['GET', 'POST'])
def stkFsbAl():		
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklist=request.args.get('stkno')
		gctip=request.args.get('gctip')
		data=mak.stk_fsb_al(stoklist,gctip)
		if data is None:
			data="stk listesinde tanimsiz stok var"
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/nagAl', methods=['GET', 'POST'])
def nagAl():		
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklist=request.args.get('stkno')
		data=mak.nakli_agirlik(stoklist)
		if data is None:
			data="stk listesinde tanimsiz stok var"
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/barkodTamamla', methods=['GET', 'POST'])
def barkodTamamla():		
	barkod=request.args.get('barkod')
	arge=Arge()
	data=arge.barkod_tamamla(barkod)
	if data is None:
		data="hata"
	return Response(json.dumps(data),mimetype='application/json')
	
@app.route('/stklistAl', methods=['GET', 'POST'])
def stklistAl():
	stoklist=mak.stk_list_al()
	return Response(json.dumps(stoklist),mimetype='application/json')	
	
@app.route('/addanStokAra', methods=['GET', 'POST'])
def addanStokAra():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklar=[]
		aranan = request.args.get('term')
		stoklar=mak.stokadlar_getir(aranan)
		#print stoklar
		return Response(json.dumps(stoklar), mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")


@app.route('/stokGetir', methods=['GET', 'POST'])
def stokGetir():
	#if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		stok=Stok()
		bf=0
		#print request.args
		hedef = request.args.get('hedef')
		hedef=hedef.split('@')
		if(len(hedef)>1):
			hedef=hedef[1]
		else:
			hedef=""
		kaynak = request.args.get('kaynak')
		kaynak=kaynak.split('@')
		if(len(kaynak)>1):
			kaynak=kaynak[1]
		else:
			kaynak=""
		kriter = request.args.get('kriter')
		if(kriter=='kod'):
			stokod = request.args.get('stokod')
			stok=mak.stok(stokod)
		else:
			stokad = request.args.get('stokad')
			stok=mak.stok2(stokad)
		bftip = request.args.get('bftip')
		
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
		if(kaynak!="" and hedef!=""):
			if(bftip=='7'):
				bf=mak.sonalim_bf(kaynak,hedef,stok.kod)	
			if(bftip=='8'):
				bf=mak.sonsatis_bf(kaynak,hedef,stok.kod)		
		stok = [ stok.kod, stok.isim, bf ]
		return Response(json.dumps(stok),mimetype='application/json')
	#return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/stokNesneGetir', methods=['GET', 'POST'])
def stokNesneGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stok=Stok()
		kriter = request.args.get('kriter')
		if(kriter=='kod'):
			stokod = request.args.get('stokod')
			stok=mak.stok(stokod)
		else:
			stokad = request.args.get('stokad')
			stok=mak.stok2(stokad)
		if(stok!=None):
			stok=stok.jsonla()
		else:
			stok=""
		return Response(json.dumps(stok),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/stokBakiyeGetir', methods=['GET', 'POST'])
def stokBakiyeGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		bakiyeler=[]
		stokod=request.args.get('stokod')
		merkez=request.args.get('merkez')
		if(len(merkez)>1):
			merkez=merkez.split('@')[1]
		else:
			merkez="xxx"
		merkezbak=mak.stok_bakiye(stokod,merkez)
		bakiyeler.append(merkezbak)
		nokta1=request.args.get('nokta1')
		if(len(nokta1)>1 and nokta1!='undefined'):
			nokta1=nokta1.split('@')[1]
		else:
			nokta1="xxx"
		bak1=mak.stok_bakiye(stokod,nokta1)
		bakiyeler.append(bak1)
		nokta2=request.args.get('nokta2')
		if(len(nokta2)>1 and nokta2!='undefined'):
			nokta2=nokta2.split('@')[1]
		else:
			nokta2="xxx"
		bak2=mak.stok_bakiye(stokod,nokta2)
		bakiyeler.append(bak2)
		return Response(json.dumps(bakiyeler),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/stokSatisGetir', methods=['GET', 'POST'])
def stokSatisGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		satislar=[]
		stokod=request.args.get('stokod')
		gerigun=request.args.get('gerigun')
		nokta1=request.args.get('nokta1')
		nokta1=nokta1.split('@')[1]
		sat1=mak.stok_satis(stokod,nokta1,gerigun)
		satislar.append(sat1)
		nokta2=request.args.get('nokta2')
		nokta2=nokta2.split('@')[1]
		sat2=mak.stok_satis(stokod,nokta2,gerigun)
		satislar.append(sat2)
		
		sstrh1=mak.son_satis(stokod,nokta1)
		satislar.append(sstrh1)
		sstrh2=mak.son_satis(stokod,nokta2)
		satislar.append(sstrh2)
		
		sgtrh1=mak.son_giris(stokod,nokta1)
		satislar.append(sgtrh1)
		sgtrh2=mak.son_giris(stokod,nokta2)
		satislar.append(sgtrh2)
		
		saytrh1=mak.son_sayim(stokod,nokta1)
		satislar.append(saytrh1)
		saytrh2=mak.son_sayim(stokod,nokta2)
		satislar.append(saytrh2)
		return Response(json.dumps(satislar),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

#siparis hazirlama bilgileri
#5-7-15
@app.route('/stokShb', methods=['GET', 'POST'])
def stokShb():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=[]
		
		stokod=request.form["kod"]
		'''
		stok=mak.stok(stokod)
		data.append(stok.kod)
		data.append(stok.isim)
		data.append(stok.satis_fiat3)
		data.append(stok.payda)
		stokod=stok.kod
		'''
		merkez=request.form["merkeznokta"]
		if(len(merkez)>1):
			merkez=merkez.split('@')[1]
		else:
			merkez="xxx"
		merkezbak=mak.stok_bakiye(stokod,merkez)
		data.append(merkezbak)
		nokta1=request.form["nokta1"]
		if(len(nokta1)>1 and nokta1!='undefined'):
			nokta1=nokta1.split('@')[1]
		else:
			nokta1="xxx"
		bak1=mak.stok_bakiye(stokod,nokta1)
		data.append(bak1)
		nokta2=request.form["nokta2"]
		if(len(nokta2)>1 and nokta2!='undefined'):
			nokta2=nokta2.split('@')[1]
		else:
			nokta2="xxx"
		bak2=mak.stok_bakiye(stokod,nokta2)
		data.append(bak2)
		gerigun=request.form["gerigun"]
		sat1=mak.stok_satis(stokod,nokta1,gerigun)
		data.append(sat1)
		sat2=mak.stok_satis(stokod,nokta2,gerigun)
		data.append(sat2)
		sstrh1=mak.son_satis(stokod,nokta1)
		data.append(sstrh1)
		sstrh2=mak.son_satis(stokod,nokta2)
		data.append(sstrh2)
		sgtrh1=mak.son_giris(stokod,nokta1)
		data.append(sgtrh1)
		sgtrh2=mak.son_giris(stokod,nokta2)
		data.append(sgtrh2)
		saytrh1=mak.son_sayim(stokod,nokta1)
		data.append(saytrh1)
		saytrh2=mak.son_sayim(stokod,nokta2)
		data.append(saytrh2)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/stokSorgu', methods=['GET', 'POST'])
def stokSorgu():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kriter=request.form["kriter"]
		aranan=request.form["arama"]
		sor_rapor=mak.stok_sorgu(kriter,aranan)
		return Response(json.dumps(sor_rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

#yapimda
@app.route('/stokArama', methods=['GET', 'POST'])
def stokArama():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kriter=request.args.get("kriter")
		aranan=request.args.get("aranan")
		sira=request.args.get("sira")
		sor_rapor=mak.stok_sorgu_perfo(kriter,aranan,sira)
		stokod=sor_rapor
		return Response(json.dumps(stokod),mimetype='application/json')
	
@app.route('/stokSorgu2', methods=['GET', 'POST'])
def stokSorgu2():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklar=[]
		fkod=request.form["fkod"]
		if(fkod!=""):
			sor=mak.sthar_detay(fkod,sonuc='dizi')
			for sorx in sor:
				stoklar.append(sorx[1])
		else:
			kriter=request.form["kriter"]
			aranan=request.form["arama"]
			sor=mak.stok_sorgu2(kriter,aranan)
			for sorx in sor:
				stoklar.append(sorx[0])
		return Response(json.dumps(stoklar),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/stokVirman', methods=['GET', 'POST'])
def stokVirman():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod=request.form["fkod"]
		kod=request.form["kod"]
		if kod<>"":
			if(fkod!=""):
				sor=mak.sthar_detay(fkod,sonuc='dizi')
			else:
				kriter=request.form["kriter"]
				aranan=request.form["arama"]
				sor=mak.stok_sorgu2(kriter,aranan)
			if(len(sor)==1):
				stokod=sor[1][0]
				cevb=mak.stok_virman(kod,stokod)
				if(cevb=='tamam'):
					sonuc=kod+" --> "+stokod+" stoguna virman edildi."
				else:
					sonuc="vt sorunu olustu."
			else:	
				sonuc="tek stok secilmelidir."
		else:
			sonuc="stok kod bos olamaz"
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/sayimHazirla', methods=['GET', 'POST'])
def sayimHazirla():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sonuc="x" 
		stkno = request.form['stklist']
		tarih = request.form['sayimTarih']
		merkez = request.form['sayimCari']
		satis = request.form['satisCari']
		if '@' in merkez:
			merkez=merkez.split('@')[1]
		else:
			return "gecersiz sayim merkezi"
		if '@' in satis:
			satis=satis.split('@')[1]
		else:
			satis=""
		sonuc=mak.sayim_hazirla(stkno,merkez,tarih,satis)
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

	
@app.route('/sayimIslet', methods=['GET', 'POST'])
def sayimIslet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sonuc="x" 
		stkno = request.form['stklist']
		kaydeden=mak.kullanici_getir(session["KULL_ID"])[0]
		sonuc=mak.sayim_islet(stkno,kaydeden)
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/stokSifirla', methods=['GET', 'POST'])
def stokSifirla():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sonuc="x" 
		tarih = request.form['sayimTarih']
		carikod = request.form['sayimCari'].split('@')[1]
		kriter = request.form['kriter']
		aranan = request.form['arama']
		sonuc=mak.stok_sifirla(carikod,tarih,kriter,aranan)
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/barkodKontrol', methods=['GET', 'POST'])
def barkodKontrol():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		stok=Stok()
		kod = request.args.get('kod')
		barkod = request.args.get('barkod')
		data=mak.barkod_kontrol(kod,barkod)
		if(data is None):
			data='##'
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	


@app.route('/chEkle', methods=['GET', 'POST'])
def chEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		durum="chbilgi"
		mkod=request.form['kod_mcari']
		chfkod=request.form['chfkod']
		print chfkod,"---------"
		if(mkod is not "" and chfkod=='nev'):
			ofatura=Fatura()
			kkod=request.form["kod"]
			if ',' in kkod:
				kkod=kkod.split(',')[0]
			ocari=mak.cari(kkod)
			if(ocari):
				ofatura.kaydeden=mak.kullanici_getir(session["KULL_ID"])[0]
				ofatura.fisno=request.form['chFisno']
				ofatura.tutar=str(request.form['chTutar']).replace(',','.')
				ofatura.islem='A'
				ofatura.tarih=request.form['chTarih']
				#22-03-2015 fatura trh ile ayni yapildi.
				ofatura.vadetarih=request.form['chvdTarih']
				#ofatura.vadetarih=ofatura.tarih
				if(float(ofatura.tutar)<0):
					ofatura.fattip='C'
					#ofatura.tutar=-1*float(ofatura.tutar)
				else:
					ofatura.fattip='G'
				ofatura.tutar=float(ofatura.tutar)
				ofatura.kaynak=mkod
				ofatura.hedef=kkod
				ofatura.med='H'
				ofatura.irs='H'
				ofatura.kdvdurum='E'
				ofatura.aciklama=request.form['chAck']
				oksonuc=mak.faturalama(ofatura,'y')
				if(oksonuc!='tamam'):
					durum="ch kaydında  bir hata oluştu!"
				else:
					print "ch odeme kaydi tamamlandi."
					#durum=mak.carihar_bilgi(kkod,mkodana,sonuc='html')
					durum=mak.carihar_bilgi(kkod,mkod,tarih="",fisno="",islemturu="",hartip="",irsdurum="",sonuc='html',modul='c')
					print kkod,mkod
					print durum
			else:
				durum="cari tnaimsiz"
		else:
			if (mak.finckeyno_kontrol(chfkod)=="var"):
				yenivade=request.form['chvdTarih']
				sonuc=mak.chvade_duzen(chfkod,yenivade)
				print "chvade:",sonuc
		return Response(json.dumps(durum),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/stkEkle', methods=['GET', 'POST'])
def stkEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		#print request.form
		kod=""
		ad=""
		miktar=""
		bf=""
		tutardan=""
		sira=""
		stoklist=""
		miktarlar=[]
		modul=request.form['modulAd']
		
		if(modul=="sayim"):
			if "kod" in request.form :
				kod=request.form['kod']
			if "ad" in request.form :
				ad=request.form['ad']
			if "miktar" in request.form :
				miktar=request.form['miktar']
			
			if "datfiat" in request.form :
				bf=request.form['datfiat']
			sira=request.form['guncelsira']
			stoklist=request.form['stklist']
			
		else:
			ad=request.form['stkStokAdi']
			kod=request.form['stkStokKodu']
			sira=request.form['stksira']
			stoklist=request.form['stkHarList']
			miktar=request.form['stkMiktar']
			bf=request.form['stkTutar']	
			if 'stkTutardan' in request.form :
				tutardan=request.form['stkTutardan']
		miktar=arge.coklu_topla(miktar)
		bf=arge.coklu_topla(bf)
		if bf.find(",") > 0 :
			bf=bf.replace(',','.')
		if miktar.find(",") > 0 :
			miktar=miktar.replace(',','.')
		bf=float(bf)
		miktar=float(miktar)
		if tutardan=='on' :
			tutar=bf
			bf=tutar/miktar
			bf=round(bf,5)
		else :
			tutar=round(bf*miktar,3)
		#tutar=math.ceil(tutar)
		#satir iskontosunun uygulanmsi
		
		if 'satisko' in request.form :
			satisko=request.form["satisko"]
			if(satisko!="" and satisko!='0'):
				bf=mak.satisko_icra(bf,satisko)
				tutar=bf*miktar
		stokhar=(kod,ad,miktar,bf,tutar,stoklist)
		con = lite.connect(app.config["DATABASE"])
		cur = con.cursor()
		if(sira =='nev' ):
			with con:
				cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar)
		else :
			with con:
				cur.execute("UPDATE stoklist SET stkod=?,stkad=?,miktar=?,bf=?,tutar=? WHERE sira=?", (kod,ad,miktar,bf,tutar,sira))
		stokTablosu=mak.stk_bilgi(stoklist)
		return Response(json.dumps(stokTablosu),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/fiyatDeg', methods=['GET', 'POST'])
def fiyatDeg():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklist = request.form['stkHarList']
		bftip=request.form['bftip']
		sonuc=mak.stk_fiyatdeg(stoklist,bftip)
		if sonuc=='tamam':
			stokTablosu=mak.stk_bilgi(stoklist)
		else:
			print "fiyat deisim sorun var"
		return Response(json.dumps(stokTablosu),mimetype='application/json')	
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/sprStkEkle', methods=['GET', 'POST'])
def sprStkEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stkod=request.form['kod']
		stkad=request.form['ad']
		miktar=request.form['otospr']
		stksecim=request.form['stksecim']
		stokList=""
		if(stksecim=='stk1'):
			stokList=request.form['sprstk1']
		if(stksecim=='stk2'):
			stokList=request.form['sprstk2']
		if(stksecim=='no'):
			stokList=request.form['sprno']
		bf=request.form['datfiat']
		if bf.find(",") > 0 :
			bf=bf.replace(',','.')
		if miktar.find(",") > 0 :
			miktar=miktar.replace(',','.')
		bf=float(bf)
		miktar=float(miktar)
		tutar=round(bf*miktar,2)
		stokhar=(stkod,stkad,miktar,bf,tutar,stokList)
		
		con = lite.connect(app.config["DATABASE"])
		cur = con.cursor()
		with con:
			cur.execute("INSERT INTO stoklist (stkod,stkad,miktar,bf,tutar,stoklistno) VALUES(?, ?,?, ?, ?,?)", stokhar)
		stokTablosu=mak.stk_bilgi(stokList)
		return Response(json.dumps(stokTablosu),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/sprSthEkle', methods=['GET', 'POST'])
def sprSthEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sthTablo="eklemede hata"
		stkod=request.form['kod']
		if(stkod is not ""):
			now = datetime.datetime.now()
			simditrh=str(now)[0:19]
			trhdz=simditrh.split()
			trhdz=trhdz[0].split('-')
			kaynak=request.form['merkeznokta']
			kaynak=kaynak.split('@')[1]
			stksecim=request.form['stksecim']
			if stksecim=='sth1':
				fisno=request.form['spr1fis']
			if stksecim=='sth2':
				fisno=request.form['spr2fis']
			tblsthar=Tblsthar()
			tblsthar.finckeyno=mak.fkod_al(fisno,kaynak)
			if tblsthar.finckeyno==-1:
				return "fisno tanimsiz"
			fatura=mak.fatura_yukle(tblsthar.finckeyno)
			tblsthar.stok_kodu=stkod
			tblsthar.miktar=str(request.form['otospr']).replace(',','.')
			tblsthar.bf=str(request.form['datfiat']).replace(',','.')
			tblsthar.nf=tblsthar.bf
			if fatura.kaynak==kaynak:
				tblsthar.kaynak=fatura.kaynak
			else:
				return "kaynak uyumsuzlugu"
			durum=mak.fat_sth_islem(tblsthar,'e')	
			if durum=='tamam':
				sthTablo=mak.sth_bilgi(kaynak,fisno,sonuc='html')
		else:
			sonuc="stok kodu boş olamaz"
		return Response(json.dumps(sthTablo),mimetype='application/json')
	
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/stkKilitle', methods=['GET', 'POST'])
def stkKilitle():
	stk=request.form["stkHarList"]
	stkuz=len(stk)
	stk_uza=stk[stkuz-4:stkuz]
	con = lite.connect(app.config["DATABASE"])
	with con:
		cur = con.cursor()
		if stk_uza =='.stk':
			cur.execute("update stoklist set stoklistno='"+str(stk[:stkuz-4])+"' WHERE stoklistno='"+stk+"'")
		else:
			stkye=stk+".stk"
			cur.execute("update stoklist set stoklistno='"+str(stkye)+"' WHERE stoklistno='"+stk+"'")
	hardos = mak.stk_list_al()
	return Response(json.dumps(hardos),mimetype='application/json')

@app.route('/stkAdGuncelle', methods=['GET', 'POST'])
def stkAdGuncelle():
	stk=request.form["stkHarList"]
	stkye=request.form["yenistkAd"]
	con = lite.connect(app.config["DATABASE"])
	with con:
		cur = con.cursor()
		cur.execute("update stoklist set stoklistno='"+str(stkye)+"' WHERE stoklistno='"+stk+"'")
	hardos = mak.stk_list_al()
	return Response(json.dumps(hardos),mimetype='application/json')


@app.route('/stkHarListSil', methods=['GET', 'POST'])
def stkHarListSil():
	stk=request.form["stkHarList"]
	stkuz=len(stk)
	stk_uza=stk[stkuz-4:stkuz]
	if stk_uza =='.stk':
		con = lite.connect(app.config["DATABASE"])
		with con:
			cur = con.cursor()
			cur.execute("DELETE FROM stoklist WHERE stoklistno='"+stk+"'")
	hardos = mak.stk_list_al()
	return Response(json.dumps(hardos),mimetype='application/json')

@app.route('/tumStkHarListSil', methods=['GET', 'POST'])
def tumStkHarListSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			os.system(stkdb_yedekle_komut)
			con = lite.connect(app.config["DATABASE"])
			with con:
				cur = con.cursor()
				#cur.execute("DROP TABLE IF EXISTS stoklist")
				#cur.execute("CREATE TABLE stoklist(sira INTEGER PRIMARY KEY AUTOINCREMENT,stkod TEXT,stkad TEXT,miktar REAL,bf REAL,tutar REAL,stoklistno INT)")
				cur.execute("delete from stoklist where stoklistno like '%.stk'")
			hardos = mak.stk_list_al()
			return Response(json.dumps(hardos),  mimetype='application/json')
		else: 
			return "yetkisiz erisim"	
	return render_template('giris.html', error="isim ve sifre giriniz")
@app.route('/tumstkGerial', methods=['GET', 'POST'])
def tumstkGerial():
	os.system(stkdb_yedekal_komut)
	data="tumstk geri yuklendi."
	return Response(json.dumps(data),mimetype='application/json')
	
@app.route('/posAktar', methods=['GET', 'POST'])
def posAktar():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="sorun olustu"
		pos_dizin=mak.ayar_al('999','pos_dizin')
		posdosya = request.args.get('posdosya')
		poscari = request.args.get('poscari')
		poscari=poscari.split('@')[1]
		if 'merkez' in request.args and request.args.get('merkez')!="":
			merkez = request.args.get('merkez')
			merkez=merkez.split('@')[1]
			if(posdosya!="" and mak.cari(poscari) is not None):
				data=mak.gtfYstk(pos_dizin+ayrac+posdosya,poscari,merkez)
				pdosy=pos_dizin+ayrac+"aktarilan"+ayrac+poscari
				if os.path.isdir(pdosy) is False :
					os.system("mkdir "+pdosy)
					print "yeni klasor tanimlandi." 
				komut=tasima_komutu+pos_dizin+ayrac+posdosya+" "+pdosy+ayrac+posdosya
				print "komut",komut
				os.system(komut)
				data="tamam"
			else:
				data="pos noktasi tanimsiz"
		else:
			data="merkez nokta tanimsiz"
		return Response(json.dumps(data),mimetype='application/json') 
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/posGonder', methods=['GET', 'POST'])
def posGonder():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		prog_anadizin=mak.ayar_al('999','prog_anadizin')
		pos_dizin=mak.ayar_al('999','pos_dizin')
		kriter = request.args.get('kriter')
		if(kriter==""):
			kriter='kod_1'
		arama = request.args.get('arama')
		data=mak.pos_urunliste(kriter,arama)
		print "posgonder:",kriter,arama
		if(data=='hata'):
			data=""
		else:
			data="pos listesi olusturuldu.kontrol ediniz."
			komut=kopya_komutu+pos_dizin+ayrac+"GNCPLUF.gtf  "+prog_anadizin+"static"+ayrac
			print komut
			os.system(komut)
		return Response(json.dumps(data),mimetype='application/json') 
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/posYukle',methods=['GET', 'POST'])
def posYukle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		path=mak.ayar_al('999','prog_anadizin')
		pos_dizin=mak.ayar_al('999','pos_dizin')
		pdosyalar=[]
		if request.method == 'POST':
			file = request.files['pos_dosya']
			if file:
				mimetype = file.content_type
				filename = werkzeug.secure_filename(file.filename)
				print filename, "dosyasi yukleniyor.............."
				file_konum=os.path.join(pos_dizin, filename)
				file.save(file_konum)
				pdosyalar = [f for f in os.listdir(pos_dizin) if re.match(r'.*\.GTF', f)]
				return Response(json.dumps(pdosyalar),mimetype='application/json') 
			else:
				return Response(json.dumps(None),mimetype='application/json') 
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/dosYukle',methods=['GET', 'POST'])
def dosYukle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="dosya gecersiz"
		if request.method == 'POST':
			file = request.files['sdosya']
			if file:
				mimetype = file.content_type
				filename = werkzeug.secure_filename(file.filename)
				print filename, "dosyasi yukleniyor.............."
				file_konum=os.path.join(filename)
				file.save(file_konum)
				tarih = request.form['sayimTarih']
				carikod = request.form['sayimCari'].split('@')[1]
				sonuc=mak.stok_sifirla(carikod,tarih,"","",arge.dosyaYdizi(filename))
				if sonuc=="tamam":
					data="sifirlama tamam"
				else:
					data="sifirlamada sorun olustu"
				return Response(json.dumps(data),mimetype='application/json') 
			else:
				return Response(json.dumps(data),mimetype='application/json') 
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/posdossil',methods=['GET', 'POST'])
def posdossil():	
	prog_anadizin=mak.ayar_al('999','prog_anadizin')
	os.system("del  "+prog_anadizin+"static\\gncpluf.gtf")
	return Response(json.dumps("islem tamam"),mimetype='application/json') 
	
@app.route('/posdosyaal',methods=['GET', 'POST'])
def posdosyaal():
	if request.method == 'POST':
		sifre=request.form['sifre']
		pos_dizin=mak.ayar_al('999','pos_dizin')
		prog_anadizin=mak.ayar_al('999','prog_anadizin')
		if(sifre==mak.ayar_al('999','pos_sifre')):
			#guncel butun stoklari cekiyor.
			mak.pos_urunliste("kod_1","")
			os.system("copy "+pos_dizin+"\\"+"GNCPLUF.gtf  "+prog_anadizin+"static\\kamusal\\")
			return "dosya geldi."
		else:
			hata="aktarim sifreniz hatali"
	return hata

@app.route('/posdosyasil',methods=['GET', 'POST'])
def posdosyasil():
	if request.method == 'POST':
		sifre=request.form['sifre']
		prog_anadizin=mak.ayar_al('999','prog_anadizin')
		if(sifre==mak.ayar_al('999','pos_sifre')):
			os.system("del  "+prog_anadizin+"static\\kamusal\\GNCPLUF.gtf")
			return "islem bitti."
		else:
			hata="aktarim sifreniz hatali"
	return hata
	
@app.route('/posdosyagonder',methods=['GET', 'POST'])
def posdosyagonder():
	#path = os.path.expanduser(u'~')
	path=mak.ayar_al('999','pos_dizin')
	hata=""
	if request.method == 'POST':
		sifre=request.form['sifre']
		if(sifre==mak.ayar_al('999','pos_sifre')):
			print "dogru sifre"
			file = request.files['file']
			if file:
				mimetype = file.content_type
				filename = werkzeug.secure_filename(file.filename)
				file_konum=os.path.join(path+"/", filename)
				file.save(file_konum)
				os.system("move "+file_konum+" "+path.split('\pos')[0])
				return "DOSYA AKTARIMI YAPILDI!!!"+"<br><a href=./posdosyagonder>GERI DON</a>"	
			else:
				return "dosya secin"
		else:
			hata="aktarim sifreniz hatali"
	return render_template('liste2.html', tree=make_tree(path),hata=hata)
	
@app.route('/teraziDataAl',methods=['GET', 'POST'])
def teraziDataAl():
	if request.method == 'POST':
		data="tamam"
		pos_dizin=mak.ayar_al('999','pos_dizin')
		prog_anadizin=mak.ayar_al('999','prog_anadizin')
		#guncel butun stoklari cekiyor.
		mak.teraziYxls()
		os.system("copy  terazi_data.xls "+prog_anadizin+"static\\kamusal\\")
		return Response(json.dumps(data),mimetype='application/json')
	
@app.route('/fisnoMevcutKontrol', methods=['GET', 'POST'])
def fisnoMevcutKontrol():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fisno=request.args.get('fisno')
		sonuc=mak.fisno_kontrol(fisno)
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")


	
@app.route('/otoFatuNo', methods=['GET', 'POST'])
def otoFatuNo():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		fisno=request.form["fatuNo"]
		gctur=request.form["hartip"][0]
		if fisno=="":
			fisno="DP"+gctur
		seriFisNo=mak.fisno_serial2(fisno,gctur)
		return seriFisNo
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/otoTanimGetir', methods=['GET', 'POST'])
def otoTanimGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		onek = request.args.get('onek')
		gctur = request.args.get('gctur')
		otofisno=mak.fisno_serial2(onek,gctur[0])
		islemturu=onek[0]
		#ontanim=kullanici.get('ontanimlar',islemturu).decode('latin5')
		kod=mak.ayar_al(session['KULL_ID'],islemturu+'_noktasi')
		ontanim=mak.cari(kod).isim+"@"+kod
		data=[otofisno,ontanim]
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/cariBilgiGetir', methods=['GET', 'POST'])
def cariBilgiGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		if 'carikod' in request.args:
			cari=Cari()
			carikod = request.args.get('carikod')
			if('@' in carikod):
				carikod=carikod.split('@')[1]
				cari=mak.cari(carikod)
				#simdilik vadegunu. gerektikce eklenecek
				data=cari.vadegunu
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/cariBul', methods=['GET', 'POST'])
def cariBul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		tip=""
		cariAd = request.args.get('term')
		if "tip" in request.args:
			tip=request.args.get('tip')
		cariler=mak.cariler_getir(cariAd,tip)
		return Response(json.dumps(cariler),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/fatuSil', methods=['GET', 'POST'])
def fatuSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99","90"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			data=""
			if "fkod" in request.args :
				fkod = request.args.get('fkod')
				l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+mak.fisno_al(fkod)+" faturasini sildi.")
				data=mak.fatura_sil(fkod)	
			else :
				data='silinecek fatura mevcut degil!'
			return Response(json.dumps(data),mimetype='application/json')
		else:
			return "yetkisiz islem"
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/fatuKaydet', methods=['GET', 'POST'])
def fatuKaydet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		odemetip=""
		otogc=""
		if "fatuKDV" in request.form :
			kdvdurum="E"
		else :
			kdvdurum="H"
		if "med" in request.form :
			medurum="E"
		else :
			medurum="H"
		if "irs" in request.form :
			irsdurum="E"
		else :
			irsdurum="H"
		kayitmodu=request.form["kayitmodu"]
		kaynak=request.form["fatuKaynak"]
		hedef=request.form["fatuHedef"]
		kaynakkod=kaynak.split('@')[1]
		if ',' in kaynakkod:
			kaynakkod=kaynakkod.split(',')[0]
		hedefkod=hedef.split('@')[1]
		if ',' in hedefkod:
			hedefkod=hedefkod.split(',')[0]
		if(mak.cari(kaynakkod) is not None and mak.cari(hedefkod) is not None):
			fatura=Fatura()
			fatura.kaydeden=mak.kullanici_getir(session["KULL_ID"])[0]
			print fatura.kaydeden
			fatura.islem=request.form["islemturu"][0]
			gecftip=request.form["hartip"]
			if(gecftip[0]=='G'):
				fatura.fattip='G'
			else:
				fatura.fattip='C'                                                                                             
			vadesay=request.form["vadesay"]
			if(vadesay==0 or vadesay==""):
				vadesay=1
			fatura.vadesay=vadesay
			fatura.tarih=request.form["fatuTarih"]
			turk_tarih=fatura.tarih
			if fatura.islem=='F':
				fatura.vadetarih=request.form["vadeTarih"]
			else:
				fatura.vadetarih=fatura.tarih
			fatura.fisno=request.form["fatuNo"]
			fatura.kaynak=kaynakkod
			fatura.hedef=hedefkod
			fatura.med='H'
			fatura.irs='H'
			if(mak.fisno_kontrol(fatura.fisno)=="var" and kayitmodu=='y'):
				return "fisno mevcut"
			if(fatura.fisno=='' and fatura.islem=='F'):
				return "fisno bos olamaz"
			if 'fkodsec' in request.form :
				fatura.fkod=request.form["fkodsec"]
				if(kayitmodu=='g' and fatura.fkod=='nev'):
					return "bir fkod seciniz!!!"
				if(kayitmodu=='y' and fatura.fkod!='nev'):
					return "fkodu nev seciniz!!!"
			if(fatura.islem=='F'):
				if "stkHarList" in request.form :
					fatura.stharlistno=request.form["stkHarList"]
					stk_onay=mak.stk_kontrol(fatura.stharlistno)
					if(stk_onay=="olumsuz"):
						return "stk listesinde sorun var."
				else:
					return 'stharlist boş olamaz'
				fatura.med=medurum
				fatura.irs=irsdurum
			fatura.kdvdurum=kdvdurum
			fatura.takipkod=request.form["fatuTakipKod"]
			fatura.aciklama=request.form["faciklama"]
			gectutar=request.form["tutar"].replace(',','.')
			if fatura.islem=='F' and gectutar=="":
				gectutar=0
			fatura.tutar=float(gectutar)
			fatisko=request.form["fatisko"]
			if(fatisko!="" and fatisko!=0):
				iskos=mak.fatisko_yap(fatura.stharlistno,fatisko,kdvdurum)
				if(iskos!='tamam'):
					return "iskonto yapilirken hata olustu"
			tutarfsb=mak.stk_fsb_al(fatura.stharlistno)
			if tutarfsb is None:
				return "stk listesinde tanimsiz stok var!"
			tutarsda=float(tutarfsb[0].split('=')[1])
			tutarsha=float(tutarfsb[1].split('=')[1])
			podmsj=""
			#KAPALI-ACIK FATURA ISLEME OLAYI
			if "odemetip" in request.form and fatura.islem=='F':
				ofatura=Fatura()
				ofatura.kaydeden=fatura.kaydeden
				odemenoktasi=request.form["odemenoktasi"]
				odekod=odemenoktasi.split('@')[1]
				ocari=mak.cari(odekod)
				if(ocari):
					ofatura.islem='K'
					ofatura.tarih=fatura.tarih
					#ofatura.vadetarih=fatura.vadetarih
					#22-03-2015 fatura trh ile ayni yapildi.
					ofatura.vadetarih=fatura.tarih
					if(fatura.kdvdurum=='E'):
						ofatura.tutar=tutarsda
					else:
						ofatura.tutar=tutarsha
						
					if(fatura.fattip=='C'):
						ofatura.fattip='G'
						ofatura.kaynak=odekod
						ofatura.hedef=hedefkod
					else:
						ofatura.fattip='C'
						ofatura.tutar=ofatura.tutar*-1
						ofatura.kaynak=odekod
						ofatura.hedef=hedefkod
					ofatura.fisno=mak.fisno_serial2(ofatura.islem+""+ofatura.fattip,ofatura.fattip)
					ofatura.med='H'
					ofatura.irs='H'
					ofatura.kdvdurum='E'
					ofatura.aciklama=fatura.aciklama+" "+("ödeme").decode('utf-8')
					oksonuc=mak.faturalama(ofatura,'y')
					l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+ofatura.islem+"-"+ofatura.fisno+" fisnolu "+ofatura.kaynak+"<-->"+ofatura.hedef+"          tutari "+str(ofatura.tutar)+" faturasini isledi.")
					if(oksonuc!='tamam'):
						podmsj="Peşin Ödeme kaydında  bir hata oluştu!"
					else:
						podmsj="pesin odeme kaydi tamamlandi."
				else:
					podmsj="odeme noktasi tanimsiz"
				app.logger.info(podmsj)
			#OTOGC FATURA ISLEME OLAYI
			if "otogc" in request.form and fatura.islem=='F':
				gcfatura=Fatura()
				odmsj=""
				otogcnok=request.form["otogcnok"]
				gckod=otogcnok.split('@')[1]
				gccari=mak.cari(gckod)
				#simdilik vadegunu. gerektikce eklenecek
				if(gccari):
					gcfatura=copy.deepcopy(fatura)
					if(fatura.fattip=='C'):
						gcfatura.fattip='G'
						gcfatura.kaynak=kaynakkod
						gcfatura.hedef=gckod
					else:
						gcfatura.fattip='C'
						gcfatura.kaynak=kaynakkod
						gcfatura.hedef=gckod
					gcfatura.fisno=mak.fisno_serial2(gcfatura.islem+""+gcfatura.fattip,gcfatura.fattip)
					gcfatura.med=fatura.med
					gcfatura.irs='H'
					#vadetarih=datetime(time.strptime(gcfatura.tarih, "%d-%m-%Y")) +datetime.timedelta(days=gccari.vadegunu)
					gcfatura.vadetarih=gcfatura.tarih
					gcfatura.kdvdurum=fatura.kdvdurum
					gcfatura.aciklama=gcfatura.aciklama+" "+fatura.fisno
					otsonuc=mak.faturalama(gcfatura,'y')
					l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+gcfatura.islem+"-"+gcfatura.fisno+" fisnolu "+gcfatura.kaynak+"<-->"+gcfatura.hedef+"          tutari "+str(gcfatura.tutar)+" faturasini isledi.")
					if(otsonuc!='tamam'):
						odmsj="otogc kaydında  bir hata oluştu!"
					else:
						odmsj="otogc kaydi tamamlandi."
				else:
					odmsj="otogce noktasi tanimsiz"
				app.logger.info(odmsj)
			l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+fatura.islem+"-"+fatura.fisno+" fisnolu "+fatura.kaynak+"<-->"+fatura.hedef+"          tutari "+str(fatura.tutar)+" faturasini isledi.")
			sonuc=mak.faturalama(fatura,kayitmodu)#+"---"+podms
			#dizaynkod=request.form["dizaynkod"]
			#if dizaynkod=="3":
			kmakbuz=request.form["kasa_makbuz_bas"]
			if kmakbuz=="1":
				term=TermalSablon()
				term.tarih=turk_tarih
				term.fisno=fatura.fisno
				term.mnot3=request.form["kasiyer"]
				term.mnot=request.form["muhatap"]
				term.tutar=fatura.tutar
				term.hedef=mak.cari(fatura.hedef).isim
				term.ack=fatura.aciklama
				term.yazdir()
			return sonuc
		else:
			return "kaynak veya hedef nokta tanimsiz"
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/ustGuncelle', methods=['GET', 'POST'])
def ustGuncelle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		gec=0
		fatura=Fatura()
		fatura.fkod=request.form["fkodsec"]
		fisno=request.form["fatuNo"]
		eskifat=mak.fatura_ustbilgi(fatura.fkod)
		eskifis=eskifat[0]
		eski_irsdurum=eskifat[11]
		if fisno==eskifis:
			gec=1
		if(mak.fisno_kontrol(fisno)=='yok' or gec==1 or eski_irsdurum=='E'):
			fatura.fisno=fisno
			fatura.tarih=request.form["fatuTarih"]
			hedef=request.form["fatuHedef"]
			fatura.hedef=hedef.split('@')[1]
			fatura.vadetarih=request.form["vadeTarih"]
			fatura.aciklama=request.form["faciklama"]
			if "med" in request.form :
				medurum="E"
			else :
				medurum="H"
			fatura.med=medurum
			if "irs" in request.form :
				irsdurum="E"
			else :
				irsdurum="H"
				if eski_irsdurum=='E':
					fatura.aciklama+=" irs:"+eskifis
			fatura.irs=irsdurum
			fatura.tutar=float(request.form["tutar"].replace(',','.'))
			return mak.ust_guncelle(fatura)
		else:
			return "fis no mevcut"
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/vadelemeKontrol', methods=['GET', 'POST'])
def vadelemeKontrol():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod = request.args.get('fkod')
		data=mak.vadeleme_kontrol(fkod)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/faturaUstbilgi', methods=['GET', 'POST'])
def faturaUstbilgi():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod = request.args.get('fkod')
		data=mak.fatura_ustbilgi(fkod)
		
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/fHareketGozlem', methods=['GET', 'POST'])
def fHareketGozlem():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kaynak=""
		tarih=""
		karsicari=""
		fisno=""
		islemturu=""
		hartip=""
		irsdurum='H'
		if('irs' in request.form):
			irsdurum='E'
		if('hartip' in request.form):
			hartip=request.form["hartip"]
		if('fatuKaynak' in request.form):
			kaynak=request.form["fatuKaynak"]
		if('merkeznokta' in request.form):
			kaynak=request.form["merkeznokta"]
		if('fatuTarih' in request.form):
			tarih=request.form["fatuTarih"]
		if('fatuNo' in request.form):
			fisno=request.form["fatuNo"]
		iscari=kaynak.split('@')[1]	
		hedef=request.form["fatuHedef"]
		if (hedef!="" and '@' in hedef):
			karsicari=hedef.split('@')[1]
		if('islemturu' in request.form):
			islemturu=request.form["islemturu"]
			islemturu=islemturu[0]
			if(islemturu!='F'):
				hartip=""
				karsicari=""
		har_rapor=mak.carihar_bilgi(iscari,karsicari,tarih,fisno,islemturu,hartip,irsdurum,sonuc='html',modul='f')
		return Response(json.dumps(har_rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
'''
23:11 30.10.2014
@app.route('/fkodListAl', methods=['GET', 'POST'])
def fkodListAl():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kaynak=""
		tarih=""
		hedef=""
		fisno=""
		islemturu=""
		if('kaynak' in request.args):
			kaynak=request.args.get('kaynak')
			if kaynak!="":
				iscari=kaynak.split('@')[1]	
			else:
				iscari=""
		if('hedef' in request.args):
			hedef=request.args.get('hedef')
			if hedef!="":
				karsicari=hedef.split('@')[1]	
			else:
				karsicari=""
		if('tarih' in request.args):
			tarih=request.args.get('tarih')
		sonuc=mak.carihar_bilgi(iscari,karsicari,tarih,fisno,islemturu,sonuc='dizi')
		fkodlar=[]
		if sonuc:
			for satir in sonuc:
				print satir[8]
				fkodlar.append(satir[8])
		return Response(json.dumps(fkodlar),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
'''		
@app.route('/sHareketGozlem', methods=['GET', 'POST'])
def sHareketGozlem():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		log_yetki=95
		yetki=mak.yetki_al(session['KULL_ID'])
		
		if('stokod' in request.args and 'kaynak' in request.args and 'shgun' in request.args):
			stkod = request.args.get('stokod')
			iscari = request.args.get('kaynak')
			gun = request.args.get('shgun')
			if(iscari==""):
				iscari=""
			else:
				iscari=iscari.split('@')[1]
		else:
			kaynak=request.form["fatuKaynak"]
			iscari=kaynak.split('@')[1]	
			stkod=request.form["stkStokKodu"]
		har_rapor=mak.sthar_bilgi(stkod,iscari,str(gun))
		if (har_rapor=="<br>"):har_rapor="hareket yok."
		if(int(yetki)<log_yetki):
			l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+mak.stok(stkod).isim+" stok hareketi izlendi.")
		return Response(json.dumps(har_rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/cHareketGozlem', methods=['GET', 'POST'])
def cHareketGozlem():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		tarih=""
		fisno=""
		kaynak=request.form["kod"]
		chgun=request.form["chgun"]
		#kaynak=kaynak.split('@')[1]	
		hedef=request.form["kod2"]
		har_rapor=mak.carihar_bilgi(kaynak,hedef,tarih,fisno,islemturu="",hartip="",irsdurum="",sonuc='html',modul="c",chgun=int(chgun))
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+mak.cari(kaynak).isim+" carisinin hareketi izlendi.")
		return Response(json.dumps(har_rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/cHareketGozlem2', methods=['GET', 'POST'])
def cHareketGozlem2():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kaynak=request.form["kod2"]
		hedef=request.form["kod"]
		bastarih=request.form["hrkBasTrh"]
		sontarih=request.form["hrkSonTrh"]
		har_rapor=mak.carihar_dokum(kaynak,hedef,bastarih,sontarih,sonuc='html')
		return Response(json.dumps(har_rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
		
@app.route('/stokModul', methods=['GET', 'POST'])	
def stokModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		poscari=mak.ayar_al(session['KULL_ID'],'pos_cari')
		pos_dizin=mak.ayar_al('999','pos_dizin')
		pdosyalar=[]
		pdosyalar = [f for f in os.listdir(pos_dizin) if re.match(r'.*\.GTF', f)]
		merkez=mak.ayar_al(session['KULL_ID'],'merkez_cari')
		if('stok' in request.args):
			stokod = request.args.get('stok')
		else:
			stokod='5555'
			
		if('harkod' in request.args):
			harkod = request.args.get('harkod')
			return "silme islem sonuc: "+mak.sthar_sil(harkod)+"<br><a href=./stokModul>GERI DON</a>"	 
			
		return render_template('stokModul.html',stok=mak.stok(stokod),pdosyalar=pdosyalar,merkez_nokta="@"+merkez,poscari="@xx")
		
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/stokSil', methods=['GET', 'POST'])
def stokSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki="99"
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			if('kod' in request.args):
				kod = request.args.get('kod')
			data=""
			stok=Stok()
			stok=mak.stok(kod)
			if(stok):
				if mak.stok_harkont(stok)=='yok':
					sonuc=mak.stok_guncelle(stok,'s')
					if(sonuc=="tamam"):
						data="stok silindi"
					else:
						data="stok silinirken veritabanli hata"
				else:
					data="hareketi olan stok silinemez."
			else:
				data="silinecek stok bulunamadi"
			return Response(json.dumps(data),mimetype='application/json')
		else: 
			return "yetkisiz erisim"
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/stokKaydet', methods=['GET', 'POST'])
def stokKaydet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		data=""
		barkod_onay="hayir"
		stok=Stok()
		kod=request.form["kod"]
		barkod3=request.form["barkod3"]
		barkod2=request.form["barkod2"]
		barkod1=request.form["barkod1"]
		barkod6=request.form["barkod6"]
		barkod5=request.form["barkod5"]
		barkod4=request.form["barkod4"]
		stok=mak.stok(kod)
		if(mak.barkod_kontrol(kod,barkod6) is None or barkod6=="" or barkod6=='NULL'):
			if(mak.barkod_kontrol(kod,barkod5) is None or barkod5=="" or barkod5=='NULL'):
				if(mak.barkod_kontrol(kod,barkod4) is None or barkod4=="" or barkod4=='NULL'):
					if(mak.barkod_kontrol(kod,barkod3) is None or barkod3=="" or barkod3=='NULL'):
						if(mak.barkod_kontrol(kod,barkod2) is None or barkod2=="" or barkod2=='NULL'):
							if(mak.barkod_kontrol(kod,barkod1) is None or barkod1=="" or barkod1=='NULL'):
								barkod_onay="tamam"
								#print "-*",barkod1,barkod2,barkod3,barkod4,barkod5,barkod6
							else:
								barkod_onay="barkod1"
						else:
							barkod_onay="barkod2"
					else:
						barkod_onay="barkod3"
				else:
					barkod_onay="barkod4"
			else:
				barkod_onay="barkod5"
		else:
			barkod_onay="barkod6"			
					
		if(barkod_onay=="tamam"):
			mod='y'
			if(stok):
				mod='g'
			else:
				stok=Stok()
			stok.isim=request.form["ad"]
			stok.alis_fiat1=request.form["al1fiat"]
			stok.alis_fiat2=request.form["al2fiat"]
			stok.alis_fiat3=request.form["al3fiat"]
			stok.satis_fiat1=request.form["satis_fiat1"]
			stok.satis_fiat2=request.form["satis_fiat2"]
			stok.satis_fiat3=request.form["satis_fiat3"]
			stok.barkod1=barkod1
			stok.barkod2=barkod2
			stok.barkod3=barkod3
			stok.barkod4=barkod4
			stok.barkod5=barkod5
			stok.barkod6=barkod6
			stok.alis_kdv_kodu=request.form["alkdv"]
			stok.kdv_orani=request.form["satkdv"]
			stok.grup_kodu=request.form["grupkod"]
			stok.kod_1=request.form["kod1"]
			stok.kod_2=request.form["kod2"]
			stok.kod_3=request.form["kod3"]
			stok.kod_4=request.form["kod4"]
			stok.kod_5=request.form["kod5"]
			stok.olcu_br1=request.form["olcubr1"]
			stok.olcu_br2=request.form["olcubr2"]
			stok.birim_agirlik=request.form["birimag"]
			stok.satici_kodu=request.form["satici_kodu"]
			stok.payda=request.form["pkadet"]
			if(mod=='g'):	
				sonuc=mak.stok_guncelle(stok,mod)
				if(sonuc=="tamam"):
					data="stok guncellendi"
				else:
					data="stok guncellenirken veritabanli hata"
			else:
				stok.kod=kod
				#yeni stok olarak eklenecek.
				sonuc=mak.stok_guncelle(stok,mod)
				if(sonuc=="tamam"):
					data="yeni stok eklendi"
				else:
					data="stok eklenirken veritabanli hata"
		else:
			data="tekrarlanan barkod: "+barkod_onay
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/cariNesneGetir', methods=['GET', 'POST'])
def cariNesneGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		cari=Cari()
		kriter = request.args.get('kriter')
		if(kriter=='kod'):
			carikod = request.args.get('kod')
			cari=mak.cari(carikod)
		else:
			cariblok = request.args.get('ad')
			if '@' in cariblok:
				carikod=cariblok.split('@')[1]	
				cari=mak.cari(carikod)
			else:
				cari=mak.cari2(cariblok)
		if(cari!=None):
			cari=cari.jsonla()
		else:
			cari=""
		
		return Response(json.dumps(cari),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/cariModul', methods=['GET', 'POST'])	
def cariModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		merkez=mak.ayar_al(session['KULL_ID'],'merkez_sube')
		mcari=mak.ayar_al(session['KULL_ID'],'merkez_cari')
		if('fkod' in request.args):
			fkod = request.args.get('fkod')
			islem_turu=mak.fatura_islemturu(fkod)
			f_bilgi=mak.fatura_ustbilgi(fkod)
			kaynak=f_bilgi[6]
			hedef=f_bilgi[7]
			if(islem_turu=='F'):
				return redirect(url_for('faturaDetay', fkod=fkod))
			else:
				return redirect(url_for('cariModul', cari=hedef))
		if('cari' in request.args):
			carikod = request.args.get('cari')
			carikod = carikod.split('@')[1]
		else:
			carikod=mcari
		cari=mak.cari(carikod)
		cari=cari.jsonla()
		return render_template('cariModul.html',cari=cari,mcari=mcari,mkod=merkez)		
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/cariSorgu', methods=['GET', 'POST'])
def cariSorgu():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kriter=request.form["kriter"]
		aranan=request.form["arama"]
		sor_rapor=mak.cari_sorgu(kriter,aranan)
		return Response(json.dumps(sor_rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
		
@app.route('/cariSorgu2', methods=['GET', 'POST'])
def cariSorgu2():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kriter=request.form["kriter"]
		aranan=request.form["arama"]
		sor=mak.cari_sorgu(kriter,aranan,'dizi')
		cariler= []
		for sorx in sor:
			cariler.append(sorx[0])
		return Response(json.dumps(cariler),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
			
@app.route('/cariSil', methods=['GET', 'POST'])
def cariSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sisim=""
		modul_yetki=["99","98"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			if('kod' in request.args):
				kod = request.args.get('kod')
			data=""
			cari=Cari()
			cari=mak.cari(kod)
			if(cari):
				sisim=mak.cari(kod).isim
				sonuc=mak.cari_guncelle(cari,'s')
				if(sonuc=="tamam"):
					data="cari silindi"
				else:
					data="cari silinirken veritabanli hata"
			else:
				data="silinecek cari bulunamadi"
			l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+sisim+" "+data)
			return Response(json.dumps(data),mimetype='application/json')
		else: 
			return "yetkisiz erisim"
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/cariKaydet', methods=['GET', 'POST'])
def cariKaydet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		
		data=""
		cari=Cari()
		kod=request.form["kod"]
		merkez=mak.ayar_al(session['KULL_ID'],'merkez_cari')
		modul_yetki="99"
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki)!=modul_yetki and kod==merkez):
			return "merkez cari guncellenemez."
		else:
			cari=mak.cari(kod)
			mod='y'
			if(cari!=None):
				mod='g'
			else:
				cari=Cari()
			cari.isim=request.form["ad"]
			cari.adres = request.form["adres"]
			cari.tel=request.form["tel"]
			cari.tel2=request.form["tel2"]
			cari.vergino=request.form["vergino"]
			cari.vergiyer=request.form["vergiyer"]
			cari.eposta=request.form["eposta"]
			cari.cari_tip=request.form["ctip"]
			cari.iban=request.form["iban"]
			cari.grupkod=request.form["grupkod"]
			cari.vade_gunu=request.form["vadegunu"]
			cari.kod1=request.form["kod1"]
	
			if(mod=='g'):	
				sonuc=mak.cari_guncelle(cari,mod)
				if(sonuc=="tamam"):
					data="cari guncellendi"
				else:
					data="cari guncellenirken veritabanli hata"
			else:
				cari.kod=kod
				#yeni cari olarak eklenecek.
				sonuc=mak.cari_guncelle(cari,mod)
				if(sonuc=="tamam"):
					data="yeni cari eklendi"
				else:
					data="cari eklenirken veritabanli hata"
			l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+mak.cari(kod).isim+" "+data)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/carikodDegis', methods=['GET', 'POST'])
def carikodDegis():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sisim=""
		modul_yetki="99"
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki)==modul_yetki):
			if('kod' in request.args):
				kod = request.form['kod']
				yenikod = request.form['cariYkod']
			data=""
			cari=Cari()
			cari=mak.cari(kod)
			if(cari):
				sonuc=mak.carikod_degistir(kod,yenikod)
				if(sonuc=="tamam"):
					data="carikod degisti"
					l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+kod+" eski cari "+yenikod+" yeni cari ile degisti.")
				else:
					data="carikod değgisirken veritabanli hata"
			else:
				data="degisecek cari bulunamadi"
			
			return Response(json.dumps(data),mimetype='application/json')
		else: 
			return "yetkisiz erisim"
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/cariYaslandir', methods=['GET', 'POST'])
def cariYaslandir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		rapor=""
		kod=request.form["kod"]
		merkez=request.form["kod2"]
		tarih=request.form["cariYasTrh"]
		rapor=mak.cari_yaslandirma(merkez,kod,tarih)
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/raporParamAl', methods=['GET', 'POST'])
def raporParamAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		dosya = request.args.get('dosya')
		paramlar=mak.rapor_paramlar(dosya)
		return Response(json.dumps(paramlar),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/cariBorcDokum', methods=['GET', 'POST'])
def cariBorcDokum():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" cari borc-dokum raporu aldi.")
		mkod=request.form["mkod"]
		rapor=mak.cari_borc_dokum(str(mkod))
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/odemePlani', methods=['GET', 'POST'])
def odemePlani():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" odeme plan raporu aldi.")
		mkod=request.form["mkod"]
		rapor=mak.cari_odeme_plani(str(mkod),"60","html")
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/kdvliSrapor', methods=['GET', 'POST'])
def kdvliSrapor():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" market satis raporu aldi.")
		bastarih=request.form["mbas_tarih"]
		sontarih=request.form["mson_tarih"]
		subekodu=request.form["subekod"]
		rapor=mak.satis_raporu_kdvli(subekodu,bastarih,sontarih)
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/pazarRapor', methods=['GET', 'POST'])
def pazarRapor():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" pazar satis raporu aldi.")
		mkod=request.form["mkod"]
		bastarih=request.form["pbas_tarih"]
		sontarih=request.form["pson_tarih"]
		subekodu=request.form["pazarkod"]
		rapor=mak.pazar_rapor(mkod,subekodu,bastarih,sontarih)
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/kontrolcariBorcDokum', methods=['GET', 'POST'])
def kontrolcariBorcDokum():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" kontrolcariBorcDokum raporu aldi.")
		mkod=request.form["mkod"]
		rapor=mak.kontrol_cari_dokum(str(mkod))
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/kontrolCariHareket', methods=['GET', 'POST'])
def kontrolCariHareket():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" kontrolcarihareket2 raporu aldi.")
		mkod=request.form["mkod"]
		rapor=mak.kontrol_cari_hareket(str(mkod))
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/ibanDokum', methods=['GET', 'POST'])
def ibanDokum():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):	
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" iban dokum raporu aldi.")
		rapor=mak.iban_dokum()
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/entegre', methods=['GET', 'POST'])
def entegre():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):	
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" entegre raporu aldi.")
		rapor=mak.entegre()
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/kasaRapor', methods=['GET', 'POST'])
def kasaRapor():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		bastarih=request.form["bas_tarih"]
		sontarih=request.form["son_tarih"]
		kasakod=request.form["kasakod"]
		kasakod=kasakod.split('@')[1]
		rapor=mak.kasa_rapor(kasakod,bastarih,sontarih)
		if 'krlm' in request.form:
			rapor=mak.kasa_rapor_kir(kasakod,bastarih,sontarih)
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/kasaBankaRapor', methods=['GET', 'POST'])
def kasaBankaRapor():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		merkez=mak.ayar_al(session['KULL_ID'],'merkez_cari')
		rapor=mak.kasabanka_rapor(merkez)
		print "ssss"
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/siparisModul', methods=['GET', 'POST'])	
def siparisModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			if('stok' in request.args):
				stokod = request.args.get('stok')
			else:
				stokod='5555'
			hardos = mak.stk_list_al()
			merkez=mak.ayar_al(session['KULL_ID'],'merkez_cari')
			fisler=mak.spr_fisler(merkez)
			if('fkod' in request.args):
				fkod = request.args.get('fkod')
				return render_template('siparisModul.html',stok=mak.stok(stokod),hardos=hardos,fkod=fkod,fisler=fisler)	
			return render_template('siparisModul.html',stok=mak.stok(stokod),hardos=hardos,fisler=fisler)		
		else: 
			return "yetkisiz erisim"	
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/sayimModul', methods=['GET', 'POST'])	
def sayimModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		hardos = mak.stk_list_al()
		
		if('fkod' in request.args):
			fkod = request.args.get('fkod')
			return render_template('sayimModul.html',hardos=hardos,fkod=fkod)	
		
		return render_template('sayimModul.html',hardos=hardos)	
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/yetkiliModul', methods=['GET', 'POST'])	
def yetkiliModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["99","98"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			return render_template('yetkiliModul.html')		
		else: 
			return "yetkisiz erisim"
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/kullanicilar', methods=['GET', 'POST'])	
def kullanicilar():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=mak.kullanicilar()
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/kullaniciGetir', methods=['GET', 'POST'])	
def kullaniciGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		no=request.args.get('no')
		data=mak.kullanici_getir(no)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/kullaniciEkle', methods=['GET', 'POST'])	
def kullaniciEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		mod='g'
		kull=Kullanici()
		if "kul_isim" in request.form:
			kull.no=request.form['kul_no']
			kull.isim=request.form['kul_isim']
			#if mak.kull_kontrol(kull.isim):
			kull.sifre=request.form['kul_sifre']
			kull.uisim=request.form['kul_uisim']
			kull.eposta=request.form['kul_eposta']
			kull.yetki=request.form['kul_yetki']
			if(kull.no=='nev'):
				mod='y'
			data=mak.kullanici_islem(kull,mod)
			#else:
			#data="bu kullanici mevcut"
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/kullaniciSil', methods=['GET', 'POST'])	
def kullaniciSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		mod='s'
		kull=Kullanici()
		if "kul_isim" in request.form:
			kull.no=request.form['kul_no']
			data=mak.kullanici_islem(kull,mod)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/bagliKul', methods=['GET', 'POST'])	
def bagliKul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		data=mak.girdi_liste()
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/bagliSil', methods=['GET', 'POST'])	
def bagliSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data='vt baglanti silinirken hata olustu.'
		id=request.form['kul_no']
		sonuc=mak.giris_sil(id)
		if sonuc=='tamam':
			data=mak.girdi_liste()
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/ayarEkle', methods=['GET', 'POST'])	
def ayarEkle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		mod='g'
		ayar=Ayar()
		if "ayar_kulno" in request.form:
			ayar.no=request.form['ayar_no']
			ayar.kulno=request.form['ayar_kulno']
			ayar.bas=request.form['ayar_bas']
			ayar.deger=request.form['ayar_deger']
			if(ayar.no=='nev'):
				mod='y'
			data=mak.ayar_islem(ayar,mod)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/ayarSil', methods=['GET', 'POST'])	
def ayarSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		mod='s'
		ayar=Ayar()
		if "ayar_kulno" in request.form:
			ayar.no=request.form['ayar_no']
			data=mak.ayar_islem(ayar,mod)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/ayarlarGetir', methods=['GET', 'POST'])	
def ayarlarGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=None
		data=mak.ayar_liste()
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/ayarGetir', methods=['GET', 'POST'])	
def ayarGetir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		no=request.args.get('no')
		data=mak.ayar_getir(no)
		#data[3]=data[3]
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/bakim', methods=['GET', 'POST'])	
def bakim():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		bakimno=request.form['bakim_no']
		data=mak.bakim1(str(bakimno))
		#print data
		#data[3]=data[3]
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/servisBaslat', methods=['GET', 'POST'])	
def servisBaslat():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="tamam.kontrol ediniz."
		arge=Arge()
		servisler=arge.servisler_al()
		for servis in servisler:
			os.system(servis)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/raporModul', methods=['GET', 'POST'])	
def raporModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		dizin='rapor'
		merkez=mak.ayar_al(session['KULL_ID'],'merkez_sube')
		raporlist=mak.dizin_cek(dizin,"rpr")
		return render_template('raporModul.html',mkod=merkez,raporlar=raporlist)		
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/altyapiModul', methods=['GET', 'POST'])	
def altyapiModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["99","98"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			dizin='rapor'
			if('mod' in request.args):
				dizin = request.args.get('mod')
			sqllist=mak.dizin_cek(dizin)
			return render_template('altyapiModul.html',sqller=sqllist,mod=dizin,kayitmodu='w')	
		else: 
			return "yetkisiz erisim"	
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/veriModul', methods=['GET', 'POST'])	
def veriModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" veri modulune girdi.")
		dosyalar=[]
		dosyalar = [f for f in os.listdir(etoku_dizin) if re.match(r'.*\.ini', f)]
		dbler = [f for f in os.listdir(db_dizin) if re.match(r'.*\.db', f)]
		tablolist=mak.dizin_cek(etodizin,"","")
		return render_template('veriModul.html',dosyalar=dosyalar,dbler=dbler,tablolar=tablolist)	
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/veriAyarAl', methods=['GET', 'POST'])	
def veriAyarAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz("veri ayarlari aliniyor.")
		dosyalar=[]
		dosyalar=os.listdir(etoku_dizin)
		ini_dosya=request.args.get('ini')
		ayar=ConfigParser()
		ayar.read(etoku_dizin+ini_dosya)
		veri_dosya=ayar.get("excel","dosya")	
		book = xlrd.open_workbook(etoku_dizin+veri_dosya)
		sayfalar=book.sheet_names()
		data=[]
		data.append(veri_dosya)
		data.append(sayfalar)
		if(sayfalar):
			return Response(json.dumps(data),mimetype='application/json')
		return render_template('veriModul.html',dosyalar=dosyalar)	
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/veriYstk', methods=['GET', 'POST'])	
def veriYstk():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		secdosya=request.args.get('dosya')
		secsayfa=request.args.get('sayfa')
		komut=etoku_komut+secdosya+" "+secsayfa+" > etoku.log"
		print komut
		komson=os.system(komut)
		
		if(komson==0):	
			data=open('etoku.log','r').read()
		else:
			data="sorun olustu."
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+secsayfa+"@"+secdosya+" veriYstk islemi yapti.")
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/vtYedekle', methods=['GET', 'POST'])	
def vtYedekle():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" vtyedek aldi.")
		vt_isim=mak.ayar_al("999","veritabani")
		data=mak.vt_yedekle(vt_isim)
		#yedek geri yukleme
		# mysql -u root -pmysql_2828 west < westyedek.sql
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/stkDbAktar', methods=['GET', 'POST'])	
def stkDbAktar():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		dbsec=request.form["dblist"]
		db_dizin=mak.ayar_al('999','db_dizin')
		data=mak.stkdb_icaktar(db_dizin+dbsec)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/stkYftr', methods=['GET', 'POST'])	
def stkYftr():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="sunucu parametre eksik"
		kdvdurum='H'
		med='H'
		if "stkno" in request.args :
			stkno=request.args.get('stkno')
			print stkno," faturalastiriliyor...."
			ax=datetime.datetime.now()
			secili=request.args.get('kdv')
			if secili=='true':
				kdvdurum='E'
			secilimed=request.args.get('med')
			if secilimed=='true':
				med='E'
			kaydeden=mak.kullanici_getir(session["KULL_ID"])[0]
			data=mak.stkYftr(stkno,kdvdurum,med,kaydeden)
			hardos = mak.stk_list_al()
			ay=datetime.datetime.now()
			print "faturalastirma bitti.",(ay-ax).total_seconds()
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/stkKopya', methods=['GET', 'POST'])	
def stkKopya():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="parametre eksik"
		if "stkno" in request.args :
			stkno=request.args.get('stkno')
			print "stk_kopyala1",stkno
			data=mak.stk_kopyala(stkno)
			print "stk_kopyala",data
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/shSifirlama', methods=['GET', 'POST'])	
def shSifirlama():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data="parametre eksik"
		if "stkno" in request.args :
			stkno=request.args.get('stkno')
			carikod=request.args.get('carikod')
			caribag=request.args.get('caribag')
			data=mak.stk_shsifirlama(stkno,"28",carikod,caribag)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/logModul', methods=['GET', 'POST'])	
def logModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			#app.logger.info(mak.girdi_isim(session['KULL_ID'])+"-log modulune girdi.")
			l.yaz(mak.girdi_isim(session['KULL_ID'])+"-log modulune girdi.")	
			#logdosya=codecs.open("log.txt",'r','utf-8').read()
			logdosya="s"
			return render_template('logModul.html',log=logdosya)	
		else:
			return "yetkisiz islem"
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/dlogModul', methods=['GET', 'POST'])	
def dlogModul():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			#app.logger.info(mak.girdi_isim(session['KULL_ID'])+"-log modulune girdi.")
			l.yaz(mak.girdi_isim(session['KULL_ID'])+"-debug log modulune girdi.")	
			#logdosya=codecs.open("log.txt",'r','utf-8').read()
			logdosya="s"
			return render_template('dlogModul.html',log=logdosya)	
		else:
			return "yetkisiz islem"
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/logAl', methods=['GET', 'POST'])	
def logAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			log=codecs.open("log//log.txt",'r').read()
			l.yaz(mak.girdi_isim(session['KULL_ID'])+"-log yeniledi.")
			return Response(json.dumps(log),mimetype='application/json')
		else:
			return "yetkisiz islem"
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/dlogAl', methods=['GET', 'POST'])	
def dlogAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki=["98","99"]
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki) in modul_yetki):
			log=codecs.open("log//sunucu.log",'r').read()
			l.yaz(mak.girdi_isim(session['KULL_ID'])+"-log yeniledi.")
			return Response(json.dumps(log),mimetype='application/json')
		else:
			return "yetkisiz islem"
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/logSil', methods=['GET', 'POST'])	
def logSil():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		modul_yetki="99"
		yetki=mak.yetki_al(session['KULL_ID'])
		if(str(yetki)==modul_yetki):
			log=""
			ylog=codecs.open("log//log.txt",'w').write(log)
			return Response(json.dumps(ylog),mimetype='application/json')	
		else: 
			return "yetkisiz erisim"
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/rprLazerbas', methods=['GET', 'POST'])
def rprLazerbas():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		dizin='./altyapi/rapor/'
		dosya = request.args.get('dosya')
		os.system("python lazermak.py yaz "+dizin+dosya+".deg")
		return Response(json.dumps("tm"),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/psqlCalistir', methods=['GET', 'POST'])
def psqlCalistir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		#l.yaz(mak.girdi_isim(session['KULL_ID'])+" "+" parametre raporu aldi.")
		rapormak=statikrapor()
		dizin='./altyapi/rapor/'
		dosya = request.args.get('dosya')
		paramlar = request.args.get('paramlar')
		orjsql=open(dizin+dosya,'r').read()
		nevsql=mak.param_guncelle(dosya,paramlar)
		codecs.open(dizin+dosya+".deg",'w',"iso-8859_9").write(nevsql)
		rapormak.sql(nevsql)
		rapor=rapormak.getHtml()
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/sqlCalistir', methods=['GET', 'POST'])
def sqlCalistir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		rapormak=statikrapor()
		sql=request.form["sqlkod"]
		rapormak.sql(sql)	
		rapor=rapormak.getHtml()
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/sqlAl', methods=['GET', 'POST'])
def sqlAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		if('mod' in request.args):
			dizin = request.args.get('mod')
		else:
			dizin='rapor'
		if('dosya' in request.args):
			dosya = request.args.get('dosya')
		else:
			dosya='test.sql'
		data=mak.sql_al(dizin,dosya)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/sqlKaydet', methods=['GET', 'POST'])
def sqlKaydet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kayitmodu = request.form['kayitmodu']
		kod = request.form['sqlkod']
		if(kayitmodu=='w'):
			dosya = request.form['yeniSql']
		else:
			dosya = request.form['sqllist']
		dizin = request.form['mod']
		sonuc=mak.sql_kaydet(dizin,dosya,kod,kayitmodu)
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/jsonAl', methods=['GET', 'POST'])
def jsonAl():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sablon = request.args.get('sablon')
		print sablon
		#sutunlar=["stok_kod","stok_isim","miktar","bf","tutar"]
		#datax=["","","","","=c2*d2"]
		#datay=["","","","","=c3*d3"]
		#data=[sutunlar,datax,datay];
		jsondata=open(etodizin+"/"+sablon,"r").read()
		data=json.loads(jsondata)
		print data
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/etoKaydet', methods=['GET', 'POST'])
def etoKaydet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sablon = request.args.get('sablon')
		try:
			sahalar = request.json[0]
		except:
			data=None
			return Response(json.dumps(data),mimetype='application/json')
		jsondata=open(etodizin+"/"+sablon,"r").read()
		data=json.loads(jsondata)
		#deismeden sonra
		yeniveri=sahalar[3]
		xkr=sahalar[0]
		ykr=sahalar[1]
		try:
			data[xkr][ykr]=yeniveri
		except:
			return Response(json.dumps("limit asimi"),mimetype='application/json')
		with open(etodizin+"/"+sablon, 'w') as yazak:
			json.dump(data, yazak)
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/etKaydet', methods=['GET', 'POST'])
def etKaydet():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sablon = request.args.get('sablon')
		data=request.json
		with open(etodizin+"/"+sablon, 'w') as yazak:
			json.dump(data, yazak)
		data="tamam"
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/etoYstk', methods=['GET', 'POST'])
def etoYstk():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		sablon = request.args.get('sablon')
		sonuc=mak.etoYstk(etodizin+"/"+sablon)
		return Response(json.dumps(sonuc),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")
	
@app.route('/caStokSorgu', methods=['GET', 'POST'])	
def caStokSorgu():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklar=[]
		if('fkod' in request.args):
			fkod = request.args.get('fkod')
			stharlar=mak.sthar_detay(fkod,sonuc='dizi')
			if stharlar:
				for sthar in stharlar:
					stoklar.append(sthar[1])
		return Response(json.dumps(stoklar),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/sprStokSorgu', methods=['GET', 'POST'])	
def sprStokSorgu():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stoklar=[]
		if('stkno' in request.args):
			stkno = request.args.get('stkno')
			stharlar=mak.stk_al(stkno)
			for sthar in stharlar:
				stoklar.append(sthar[1])
		return Response(json.dumps(stoklar),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/fiyatAktar', methods=['GET', 'POST'])
def fiyatAktar():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data='fiyat aktarmada sorun var!!!'
		if('fkod' in request.args):
			fkod = request.args.get('fkod')
			if(fkod!='nev'):
				data=mak.fiyat_guncelle(fkod)
			else:
				data='fkodlist değerini seçiniz!!!'
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")

@app.route('/stkTopbir', methods=['GET', 'POST'])
def stkTopbir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkodlar=[]
		yfisler=request.args.get('fkodlar')
		yfisler=yfisler.split(',')
		for yf in yfisler:
			if yf:
				fis=yf.split('@')[0]
				mrk=yf.split('@')[1]
				fkod=mak.fkod_al(str(fis),str(mrk))
				fkodlar.append(str(fkod))
		if(mak.cogul_stkbir(fkodlar)):
			return "tamam"
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/irsTopfat', methods=['GET', 'POST'])
def irsTopfat():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kaydeden=mak.kullanici_getir(session["KULL_ID"])[0]
		fkodlar=[]
		yfisler=request.args.get('fkodlar')
		yfisler=yfisler.split(',')
		print "--",yfisler
		if yfisler[0]!='' and 'tarih' in request.args and 'fisno' in request.args:
			tarih=request.args.get('tarih')
			fisno=request.args.get('fisno')
			if fisno!="" and tarih!="":
				for yf in yfisler:
					if yf:
						fis=yf.split('@')[0]
						mrk=yf.split('@')[1]
						fkod=mak.fkod_al(str(fis),str(mrk))
						fkodlar.append(str(fkod))
				sonuc=mak.irs_topfat(fkodlar,tarih,fisno,kaydeden)
				return sonuc
			else:
				return "tarih-fisno bos olamaz"
		else:
			return "irsaliye listesi bos olamaz"
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/zRaporla', methods=['GET', 'POST'])	
def zRaporla():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		pos_dizin=mak.ayar_al('999','pos_dizin')
		posdosya = request.form['posdosya']
		arge=Arge()
		rapor=arge.z_rapor_analiz(pos_dizin+"/"+posdosya)
		return Response(json.dumps(rapor),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/fatuGonder', methods=['GET', 'POST'])
def fatuGonder():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod=""
		kendi=mak.kullanici_posta(session['KULL_ID'])
		if('fkod' in request.args):
			fkod=request.args.get('fkod')
			harrapor=mak.sthar_detay(fkod,sonuc='html',tasarim=2)
			alici=mak.cari((mak.fatura_ustbilgi(fkod)[7]).split('@')[1]).eposta
		return render_template('postagonder.html',fkod=fkod,kposta=alici,kendi=kendi,konu='urun listesi',modul="f")+mak.sthar_detay_baslik(fkod,sonuc='html',tasarim=2)+"<br>"+harrapor
	return render_template('giris.html', error="isim ve sifre giriniz")				

@app.route('/caharGonder', methods=['GET', 'POST'])
def caharGonder():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kendi=mak.kullanici_posta(session['KULL_ID'])
		konu="CARI HAREKET DOKUM"
		l.yaz("caharGonder e girildi.")
		kaynak=request.form["kod2"]
		hedef=request.form["kod"]
		bastarih=request.form["hrkBasTrh"]
		sontarih=request.form["hrkSonTrh"]
		hedef_posta=mak.cari(hedef).eposta
		rapor=mak.carihar_dokum(kaynak,hedef,bastarih,sontarih,sonuc='html')
		codecs.open('sql_cikti/carihar_dokum.html','w','iso-8859_9').write(rapor)
		#return Response(json.dumps(rapor),mimetype='application/json')
		return render_template('postagonder.html',fkod=-1,kposta=hedef_posta,kendi=kendi,konu=konu,modul="c")+rapor
	return render_template('giris.html', error="isim ve sifre giriniz")			
# models.py icindeki nesne kaliplarina gore fatura olusturulmustur.
# kalemler de aynı dosyadaki kaliba gore olusturulmustur.

@app.route('/stkGonder', methods=['GET', 'POST'])
def stkGonder():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		kendi=mak.kullanici_posta(session['KULL_ID'])
		konu="hareket bilgilendirme"
		stkno=request.args.get('stkno')
		l.yaz(kendi+" stkGonder e girildi.")
		rapor=mak.stk_rapor_al(stkno)
		codecs.open('sql_cikti/stk_dokum.html','w','iso-8859_9').write(rapor)
		#return Response(json.dumps(rapor),mimetype='application/json')
		return render_template('postagonder.html',fkod=-1,kendi=kendi,kposta="x@x.com",konu=konu,modul="stk")+rapor
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/stkArsiv', methods=['GET', 'POST'])
def stkArsiv():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		stkno=request.args.get('stkno')
		l.yaz(" stkArsiv e girildi.-->"+stkno)
		data=mak.stk_kopyala(stkno,stkno)
		#return Response(json.dumps(rapor),mimetype='application/json')
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/lazerYazdir', methods=['GET', 'POST'])
def lazerYazdir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod=request.form['fkodsec']
		data=""
		if fkod !="nev":
			yazicikod=request.form['yazicikod']
			os.system(lazeryaz_komut+fkod+" "+yazicikod)
			data="tamam"
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/stkTermal', methods=['GET', 'POST'])
def stkTermal():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod=request.form['stkHarList']
		data=""
		if fkod !="nev":
			yazicikod=request.form['yazicikod']
			os.system(lazeryaz_komut2+fkod+" "+yazicikod)
			data="tamam"
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/etkYazdir', methods=['GET', 'POST'])
def etkYazdir():
	kod = request.form['kod']
	stok=mak.stok(kod)
	bf=stok.satis_fiat1
	#epl 2 progdilinde sablon
	#sablondos="etk.sab"
	#epl 1 prog dilinde
	sablondos="etk_sablon.dos"
	sablon=open(sablondos,"r").read()
	sablon=sablon.replace('@stok_adi@',str(stok.isim[0:29]))
	sablon=sablon.replace('@sf@',str(bf))
	mak.etk_basim_kaydet(kod,bf)
	open("etk.yaz","w").write(sablon)
	os.system(etkyazdir_komut)
	return "tamam"
	
@app.route('/etkYazdirKontrol', methods=['GET', 'POST'])
def etkYazdirKontrol():
	kod = request.form['kod']
	stok=mak.stok(kod)
	bf=stok.satis_fiat1
	onay=mak.etk_basim_kontrol(kod,bf)
	return onay
	
@app.route('/belgeTara', methods=['GET', 'POST'])
def belgeTara():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		data=""
		belge=request.form['belge_ad']
		if(belge!=""):
			os.system("dinamiko_servis.py dinamiko6060 tara "+belge)
			data= "BELGENIZ TARANDI"
		else:
			data="taranacak belge isim girin."
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	
	
@app.route('/fatuYazdir', methods=['GET', 'POST'])
def fatuYazdir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkodlar=[]
		if request.form:
			yfisler=request.form['data']
			yfisler=json.loads(yfisler)
			for yf in yfisler:
				fis=yf.split('@')[0]
				mrk=yf.split('@')[1]
				fkod=mak.fkod_al(fis,mrk)
				fkodlar.append(fkod)
			dizaynno="1"
		else:	
			fkod=""
			if('fkod' in request.args):
				fkodlar=request.args.get('fkod')
				fkodlar=fkodlar.split(',')
			else:
				yfisler=request.args.get('fkodlar')
				yfisler=yfisler.split(',')
				for yf in yfisler:
					if yf:
						fis=yf.split('@')[0]
						mrk=yf.split('@')[1]
						fkod=mak.fkod_al(str(fis),str(mrk))
						fkodlar.append(fkod)
		faturalar=[]
		for fkod in fkodlar:	
			if(mak.fatura_islemturu(fkod) is None):
				return "stkno iliskili fatura bulunamadi."
			if('dizaynno' in request.args):
				dizaynno = request.args.get('dizaynno')
			ekzaman = int(request.args.get('ekzaman'))
			saat_degeri=str((datetime.datetime.now()+ datetime.timedelta(hours=ekzaman)).time())[0:8]
			
			faturaust=mak.sthar_detay_baslik(fkod,sonuc='dizi')		
			cari=mak.cari(faturaust[13])
			stharlar=mak.sthar_detay(fkod,sonuc='dizi')
			
			fatura = None
			fatura=dizayn.faturayapi()
			fatura.hedef=cari.isim
			fatura.adres=cari.adres
			fatura.vdaire=cari.vergiyer
			fatura.vergino=cari.vergino
			fatura.tarih=faturaust[0]
			if('ek' in request.args):
				ek = request.args.get('ek')
				sql="SELECT '"+mak.tarih_format(fatura.tarih)+"' + interval "+ek+" day"
				fatura.tarih2=mak.tarih_turk(mak.calistir(sql)[0][0])
			else:
				fatura.tarih2=faturaust[0]
			fatura.saat=saat_degeri
			yaziylatutar=mak.yaziyla("{:.2f}".format(faturaust[7]))
			fatura.tutaryaziyla="#"+yaziylatutar[0]+yaziylatutar[1]+"#"
			fatura.kdvtop=faturaust[7]-faturaust[2]
			fatura.kdvtop="{:.2f}".format(fatura.kdvtop)
			fatura.kdvsiztutar="{:.2f}".format(faturaust[2])
			fatura.kdv1="{:.2f}".format(faturaust[4])
			fatura.kdv8="{:.2f}".format(faturaust[5])
			fatura.kdv18="{:.2f}".format(faturaust[6])
			fatura.gtoplam="{:.2f}".format(faturaust[7])
			fatura.merkezsicilno="MERKEZ TİC. SİCİL NO:xxxxx".decode("utf-8")
			fatura.subesicilno="ŞUBE TİC. SİCİL NO:xxxxxx".decode("utf-8")
			fatura.mersisno=""
			fatura.kaynakwebadresi="www.sirketismi.com.tr".decode("utf-8")
			fatura.kalemler=[]
			kalemsay=len(stharlar)
			for sthar in stharlar:
				kalem=dizayn.kalemyapi()
				kalem.kdv="{:.0f}".format(sthar[9])
				kalem.ad=sthar[2]
				kalem.miktar="{:.2f}".format(sthar[3])
				kalem.birim=sthar[4]
				if str(dizaynno)=="4":
					kalem.brfiyat= "{:.2f}".format(sthar[5])
					kalem.tutar="{:.2f}".format(sthar[3]*sthar[5])
				else:
					kalem.brfiyat= "{:.2f}".format(sthar[6])
					kalem.tutar="{:.2f}".format(sthar[3]*sthar[6])
				#09:19 23.02.2015
				#kalem.tutar="{:.2f}".format(sthar[7])
				fatura.kalemler.append(kalem)

			kalem_adedi=mak.ayar_al('999',"yzc_dizayn_kalem@"+dizaynno)
			kalem_adedi=int(kalem_adedi)
			print_html='yazici_dizayn'+str(dizaynno)+".html"
			dizayner=dizayn.dizaynyapi()
			fatura.sayfayaz=dizayner.sayfala(fatura,kalem_adedi)
			faturalar.append(fatura)
			del dizayner
			del fatura
			
		return render_template(print_html, faturalar=faturalar)
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/makbuzYazdir', methods=['GET', 'POST'])
def makbuzYazdir():
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		fkod=request.form["fkodsec"]
		hedef=request.form["fatuHedef"].split('@')[1]
		term=TermalSablon()
		term.tarih=request.form["fatuTarih"]
		term.fisno=mak.fisno_al(fkod)
		term.mnot3=request.form["kasiyer"]
		term.mnot=request.form["muhatap"]
		term.tutar=request.form["tutar"]
		term.hedef=mak.cari(hedef).isim
		term.ack=request.form["faciklama"]
		term.yazdir()
		data="makbuz basildi."
		return Response(json.dumps(data),mimetype='application/json')
	return render_template('giris.html', error="isim ve sifre giriniz")	

@app.route('/postagonder', methods=['GET', 'POST'])
def postagonder():	
	if("KULL_ID" in session and mak.girdi_kontrol(session['KULL_ID']) ):
		if request.method == 'POST':	
			if request.form["komut"] in ["postala","listesiz postala"] :
				#maillog=open("maillog","a")
				fkod = request.form['fkod']
				gmail_user = "obs.giom@gmail.com"  #request.form['postaad']
				gmail_pwd = "obs_giom********"  #request.form['postasfr']
				
				gonderen = gmail_user
				alan = [request.form['kime']] #must be a list
				text = (request.form['icerik'])+"</br>"
				msg = MIMEMultipart('alternative')
				msg['Subject'] = request.form['konu']
				msg['From'] = gmail_user
				msg['To'] = request.form['kime']
				cckisi =[request.form['kendi']]
				# Record the MIME types of both parts - text/plain and text/html.
				
				# Attach parts into message container.
				# According to RFC 2046, the last part of a multipart message, in this case
				# the HTML message, is best and preferred.
				if request.form["komut"] == "listesiz postala" :
					part1 = MIMEText(text+"BU POSTAYI CEVAPLAMAYINIZ!!!", 'html','iso8859_9')
					#msg.set_charset('windows-1254')
					msg.attach(part1)
				if request.form["komut"] == "postala" :
					#rapor=rapor.decode('iso8859_9')
					#part2 = MIMEText(text+rapor.decode('iso8859_9'), 'html')
					rapor=mak.sthar_detay_baslik(fkod,sonuc='html',tasarim=2)+"<br>"+mak.sthar_detay(fkod,sonuc='html',tasarim=2)
					if request.form['modul'] =="c":
						rapor=codecs.open("sql_cikti/carihar_dokum.html",'r','iso-8859_9').read()
					if request.form['modul'] =="stk":
						rapor=codecs.open("sql_cikti/stk_dokum.html",'r','iso-8859_9').read()
					part2 = MIMEText(text+rapor+"BU POSTAYI CEVAPLAMAYINIZ!!!", 'html','iso8859_9')
					msg.attach(part2)
				try:
					#server = smtplib.SMTP(SERVER) 
					server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
					print server.ehlo()
					server.starttls()
					server.login(gmail_user, gmail_pwd)
					server.sendmail(gonderen,alan+cckisi, msg.as_string())
					#server.quit()
					server.close()
					#maillog.write(gmail_user,gmail_pwd,msg['To'],msg['Subject'])
					return 'MAILINIZ BASARIYLA GONDERILDI.'
				except:
					return "MAIL GONDERME HATA."
		
		return render_template('postagonder.html')+sqlmak.faturabilgi2(fisno,fattip)
	return render_template('giris.html', error="isim ve sifre giriniz")		

@app.route('/xx', methods=['GET', 'POST'])
def xx():
	app.logger.info("xx sayfawewew")
	return "xx"
	
if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

if __name__ == '__main__':
	#logging.basicConfig(filename='.\log\\log.txt',format='%(message)s',level=logging.DEBUG)
	port_calis=6006
	#open("giom.surec",'w').write(str(os.getpid()))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1',port_calis))
	if result == 99:
		print "sunucu zaten bu portta calisiyor.!!!"
	else:
		'''
		import logging
		from logging.handlers import RotatingFileHandler
		file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
		file_handler.setLevel(logging.DEBUG)
		app.logger.setLevel(logging.DEBUG)
		app.logger.addHandler(file_handler)
		'''
		#import __init__
		#init_db()  # or whatever you need to do

		import logging
		logging.basicConfig(filename="log"+ayrac+"sunucu.log",level=logging.DEBUG)
		app.run(host="0.0.0.0",port=port_calis,debug=True,threaded=True) 
	'''	
	logger = logging.getLogger('werkzeug')
	handler = logging.FileHandler('wwlog.txt')
	logger.addHandler(handler)
	# Also add the handler to Flask's logger for cases
	#  where Werkzeug isn't used as the underlying WSGI server.
	app.logger.addHandler(handler)
	'''	
	

#debug=True  kod deise server yenilenir
# route fonks bi nevi get olunca ne dondurule.
