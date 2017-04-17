#!/usr/bin/env python
import os
import time
from mysql_ayar import *

baglanti=MysqlBaglanti()

username = baglanti.kullanici
password = baglanti.sifre
hostname = baglanti.host
database=baglanti.vt

filestamp = time.strftime('%Y-%m-%d')

# butun vtlerin yedegini almak icin
'''
database_list_command="mysql -u %s -p%s -h %s --silent -N -e 'show databases'" % (username, password, hostname)
for database in os.popen(database_list_command).readlines():
    database = database.strip()
    if database == 'information_schema':
        continue
    if database == 'performance_schema':
        continue
    
'''
filename = "sql_yedek/%s-%s.sql" % (database, filestamp)
os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz" % (username, password, hostname, database, filename))

