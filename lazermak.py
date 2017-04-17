# -*- coding: utf-8 -*-
from mysqlmak import *
import os
import sys
import datetime
import platform
import codecs


bas="I8,A,001"+"\n"+"D3"+"\n"+"R0,0"+"\n"+"q600"+"\n"+"I8,E,001"+"\n"+"N"+"\n"
son="P1"
liko=""
liko+=bas
aralik=22
basno=20

mak=mysqlmak()
sql=codecs.open(sys.argv[2],'r','iso-8859_9').read()#"select stok_kodu,stok_adi from tblstsabit where stok_kodu like '60204%'"
rows=mak.calistir(sql)
veriler=[]
#ornek format
formatlar=['{:6s}','{:11s}','{:15s}','{:7.2f}']
for row in rows:
	satir=""
	#i=0
	eud=5
	for ro in row:
		if type(ro)==str:
			#belli karakter kadar almak
			if len(ro)>eud:
				eud=20
			if len(ro)>19:
				ro=ro[0:20]
				eud=20	
			otoformat='{:'+str(eud+2)+'s}'
		else:
			otoformat='{:7.2f}'
		#satir+=formatlar[i].format(ro)
		satir+=otoformat.format(ro)
		#i+=1
	#satir=formatsab.format(row[0],row[1],row[2],row[3])
	veriler.append(satir)
#ornek veriler
#veriler=["t1","t2","t3","t4"]


veriler.reverse()
satno=basno+aralik*2
orta=""

for veri in veriler:
	orta+="A600,"+str(satno)+",2,2,1,1,N,"+'"'+veri.decode("latin5")+'"'+"\n"
	satno+=aralik
liko+=orta+"\n"

liko+="A600,"+str(basno)+",2,2,1,1,N,"+'"'+"giom zebra@lazer.py yazdirma modulu"+'"'+"\n"

liko+=son+"\n"
#open("gcc.prn","w").write(liko)
codecs.open("gcc.prn", "w","latin5").write(liko)

if str(sys.argv[1])=="yaz":
	os.system("./yazdir.sh gcc.prn")
#print sys.argv
print liko



#print '{:10s} {:3d}  {:7.2f}'.format('xxx', 123, 98)
