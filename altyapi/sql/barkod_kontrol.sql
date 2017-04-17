select stok_kodu from tblstsabit 
where stok_kodu <> '@kod@' 
and( barkod1='@barkod@' or barkod2='@barkod@' or barkod3='@barkod@' or
barkod4='@barkod@' or barkod5='@barkod@' or barkod6='@barkod@'  
or stok_kodu='@barkod@') group by stok_kodu