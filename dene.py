#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime
import os
import decimal
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
from genelfonks import *
from termalsab import *
import xlwt
import xlrd
from stdnum import ean

mak=mysqlmak()
tb=time.clock()
ax = datetime.datetime.now()
arge=Arge()


mak.stk_birlestir("639.stk","314.stk")

ay = datetime.datetime.now()
krono=ay-ax
print "dosya yazma islem hizi:",krono.total_seconds(),"  saniye"
print "islem adedi"#,len(row)
print "hiz-adet oran"#,(ts-tb)/len(row)


	
	
