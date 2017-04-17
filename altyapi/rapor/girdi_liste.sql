select l.id,k.isim,l.durum,l.zaman from giris_liste as l
inner join kullanici as k
on k.id=l.id