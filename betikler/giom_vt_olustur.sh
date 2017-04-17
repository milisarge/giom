echo "giom veritabanı oluşturuluyor..."
mysql -u root -p < altyapi/sql/giom_vt_olustur.sql
echo "giom veritabanı oluşturuldu."
echo "giom veritabanı yükleniyor..."
mysql -u root -p giom < altyapi/sql/giom.sql
echo "giom veritabanı hazır."
echo "giom yetkili kullanıcı oluşturuluyor..."
mysql -u root -p giom < altyapi/sql/giom_yetkili_kullanici_olustur.sql
echo "giom yetkili kullanıcı oluşturuldu."
