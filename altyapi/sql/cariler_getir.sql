select cari_kod,cari_isim from tblcasabit 
where (cari_isim like '%@aranan@%' or cari_kod like '%@aranan@%') @tip@ order by cari_isim;