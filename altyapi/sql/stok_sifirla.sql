select sb.stok_kodu from tblstsabit as sb
inner join sthar as sh on sb.stok_kodu=sh.stok_kodu 
where  sh.tarih<='@tarih@' and (sh.kaynak='@carikod@' or sh.hedef='@carikod@') @eksorgu@ group by sb.stok_kodu