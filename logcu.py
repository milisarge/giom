# -*- coding: utf-8 -*-
import datetime
import codecs

class Logcu:
	
	global log
	
	def __init__(self):
			
		log=""
		
	def hata(self,mesaj):
		print "HATA:",mesaj
	
	def uyari(self,mesaj):
		print "UYARI:",mesaj
		
	def bilgi(self,mesaj):
		print "BILGI:",mesaj
	
	def yaz(self,kull="sistem",ack="",tip="BILGI"):
		
		codecs.open("log//log.txt",'a').write(str(datetime.datetime.now())[0:19]+"--->"+tip+":  "+str(kull)+"@"+str(ack)+"\n")