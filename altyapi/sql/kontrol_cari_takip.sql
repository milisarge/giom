SELECT date(tarih) as tarih,KAYNAK,FTIP,HEDEF,FNO,aciklama,geneltoplam 	 FROM fatura as f inner join tblcasabit c on f.hedef=c.cari_kod 
where (c.rapor_kodu1='takip' and f.ftip='C' and islem_turu='F' and aciklama not like '%iade%') 
or (c.rapor_kodu1='takip' and f.ftip='G' and islem_turu in ('K','B') and aciklama not like '%iade%' and hedef not in ('7010','9999'))