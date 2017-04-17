set @iscari := '02';
set @yon='c';
set @cari_tip='d';
select t.tarih,t.fi�no,t.cari_kod,(select cari_isim from tblcasabit where cari_kod=t.cari_kod) as cari,t.a��klama,t.fatura_tipi,t.kimlik from (
SELECT date(tarih) as tarih,fno as fi�no,c.cari_isim as cari_isim,f.aciklama as a��klama,f.inckeyno as kimlik,
(case 
when ftip='C' and kaynak=@iscari then "sat��"
when ftip='G' and kaynak=@iscari then "kar�� al�m"
when ftip='G' and hedef=@iscari then "al�m"
when ftip='C' and hedef=@iscari then "kar�� sat��"
end
) as fatura_tipi,
(case 
when @yon='c' and kaynak=@iscari then 'c'
when @yon='g' and hedef=@iscari then 'g'
end) as durum,
(case 
when @yon='c' and kaynak=@iscari then hedef
when @yon='g' and hedef=@iscari then kaynak
end) as cari_kod 
from fatura as f
inner join tblcasabit as c
where c.cari_tip=@cari_tip group by f.inckeyno
) as t
where t.durum=@yon