import sys
from random import randint
from mysqlmak import *

if(len(sys.argv)>1):
	stkno=sys.argv[1]+"_sym"
else:
	stkno="konsolstk_"+str(randint(1000,9999))

i=1
mak=mysqlmak()
print "stkno: ",stkno,'\n'
while i:
	barkod=raw_input("barkod:")
	if(barkod=="-c"):
		break
	stok=mak.stok(barkod)
	if(stok):
		print stok.isim,'\n'
		j=1
		while j:
			miktar=raw_input("miktar:")
			miktar=miktar.replace(',','.')
			if(miktar=='-u'):
				break
			try:
				miktar=float(miktar)
				if(miktar!="" and miktar!=0):
					tutar=round(stok.satis_fiat3*miktar,2)
					stokhar=(stok.kod,stok.isim,miktar,stok.satis_fiat3,tutar,stkno)
					mak.stk_ekle(stokhar)
					print stokhar,'\n'
					j=0
				else:
					print "miktar gecersiz",'\n'
			except:
				print "miktar gecersiz",'\n'
	else:
		print "stok yok",'\n'