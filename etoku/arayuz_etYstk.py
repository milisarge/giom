from easygui import *
import xlrd
import os

datayol='/opt/giom/etoku/DATA/'
msg ="EXCEL DOSYANIZI SECIN"
title = "XLS DOSYALARI"
dosyalar=[]
doslar= os.listdir(datayol)
for dos in doslar:
	if(os.path.splitext(dos)[-1]=='.xls'):
		if(os.path.isfile(datayol+dos.split('.')[0]+".ini")):
			dosyalar.append(dos.split('.')[0])
secdos = choicebox(msg, title, dosyalar)
book = xlrd.open_workbook(datayol+secdos+".xls")
sayfalar=book.sheet_names()
secsayfa = choicebox("SAYFANIZI SECIN",dos+" SAYFALARI", sayfalar)
komut="etYstk.py "+secdos+".ini "+secsayfa
komson=os.system(komut)
if(komson==0):	
	msgbox("stklar olusturuldu.")
else:
	msgbox("sorun olustu.")
