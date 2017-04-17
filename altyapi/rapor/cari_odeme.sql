select sum(geneltoplam) from fatura as f inner join tblcasabit as cx on cx.cari_kod=f.kaynak
where  cx.grup_kodu='merkez' and f.ftip='C' and hedef='@carikod@'