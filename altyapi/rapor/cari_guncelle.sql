UPDATE tblcasabit SET 
cari_isim = '@isim@',
cari_adres='@adres@',
cari_tel='@tel@',
grup_kodu='@grupkod@',
cari_tip='@cari_tip@',
vergi_dairesi='@vergiyer@',
vergi_numarasi='@vergino@',
cari_tel2='@tel2@',
email='@eposta@',
vade_gunu='@vade_gunu@',
iban='@iban@',
rapor_kodu1='@kod1@'
where cari_kod='@kod@';
