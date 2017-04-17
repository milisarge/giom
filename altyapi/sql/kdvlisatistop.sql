SELECT g.grupkodu,g.grupadi,round(sum(b.miktar*bf),2) as tutar,DATE_FORMAT(tarih,'%d/%m/%Y') AS tarih from sthar as b
inner join tblstsabit as a on b.stok_kodu=a.stok_kodu
inner join grup_kodlari as g on a.grup_kodu=g.grupkodu
where b.kaynak='@subekod@' and hedef='pos' and b.ftip='C'
and tarih between ('@bastarih@') and ('@sontarih@')
group by b.tarih,g.grupkodu,g.grupadi