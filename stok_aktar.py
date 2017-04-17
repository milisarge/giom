#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import sys
import datetime
import os
import decimal
import pyodbc
import time
import codecs
from logcu import *
from iniparse import INIConfig
from iniparse import ConfigParser
import random
import re
import sqlite3 as lite
import sys
import urllib2, urllib
import MultipartPostHandler
from random import randint
import datetime
from mysqlmak import *
from cari import *
from stok import *
from fatura import *
from htmlrapor import *
#from mysqllab import *
	
sqlmak=sqlmak()
mak=mysqlmak()
rapor=statikrapor()
logla=Logcu()

#mak.test()
stoklar=sqlmak.calistirtum("select * from tblstsabit")  #  WHERE STOK_KODU='BAKLIYAT-6015'

i=0
gec=""
for stok in stoklar:
	j=0
	for sto in stok:
		if sto is None:
			stok[j]=""
		j=j+1
	sql=open('./altyapi/stok/stok_ekle_detayli.sql','r').read()
	sql=sql.replace('@kod@',stok[2])
	sql=sql.replace('@isim@',stok[4])	
	sql=sql.replace('@barkod1@',str(stok[54]))	
	sql=sql.replace('@barkod2@',str(stok[55]))
	sql=sql.replace('@barkod3@',str(stok[56]))	
	sql=sql.replace('@barkod4@',"")	
	sql=sql.replace('@barkod5@',"")	
	sql=sql.replace('@barkod6@',"")	
	sql=sql.replace('@alkdv@',str(stok[57]))	
	sql=sql.replace('@satkdv@',str(stok[37]))
	sql=sql.replace('@satis_fiat3@',str(stok[28]))	
	sql=sql.replace('@satis_fiat2@',str(stok[27]))	
	sql=sql.replace('@satis_fiat1@',str(stok[26]))
	sql=sql.replace('@alis_fiat1@',str(stok[58]))
	sql=sql.replace('@alis_fiat2@',"0")
	sql=sql.replace('@alis_fiat3@',"0")
	sql=sql.replace('@satici_kodu@',str(stok[11]))
	sql=sql.replace('@olcu_br1@',str(stok[12]))
	sql=sql.replace('@olcu_br2@',str(stok[13]))
	sql=sql.replace('@pay_1@',str(stok[14]))
	sql=sql.replace('@payda_1@',str(stok[15]))
	sql=sql.replace('@pay_2@',str(stok[17]))
	sql=sql.replace('@payda_2@',str(stok[18]))
	sql=sql.replace('@grupkod@',str(stok[5]))
	sql=sql.replace('@kod_1@',str(stok[6]))
	sql=sql.replace('@kod_2@',str(stok[7]))
	sql=sql.replace('@kod_3@',str(stok[8]))
	sql=sql.replace('@kod_4@',str(stok[9]))
	sql=sql.replace('@kod_5@',str(stok[10]))
	sql=sql.replace('@birim_agirlik@',"0")
	gec+=sql+"\n"
open("stok_kart_data.sql",'w').write(gec)
	
	
#mak.calistir(sql)
