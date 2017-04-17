# -*- coding: utf-8 -*-

class Stokhareket:
	def __init__(self):
		
		self.sira=""
		self.stkod=""
		self.stokad=""
		self.miktar=0.00
		self.bf=0.00
		self.tutar=self.miktar*self.bf
		self.stoklistno=""
	def goster(self):
		print self.sira,self.stkod,self.stokad,self.miktar,self.bf,self.tutar,self.stoklistno