set @dbakiye := 0;
select t.tarih,t.fiþno,t.hareket_tipi,t.ack,round(t.giris+t.girisx,2) as giriþ,round(t.cikis+t.cikisx,2) as çýkýþ, 
round((@dbakiye := @dbakiye + (giris+girisx)-(cikis+cikisx)),2) as bakiye,t.fkod from
(SELECT date(f.TARIH) as tarih,fno as fiþno,
case when f.KAYNAK = '@iscari@' then concat(b.tur,"(",c.cari_isim,")") else concat(b.tur,"(",cx.cari_isim,")") end  as hareket_tipi,
f.ACIKLAMA as ack,inckeyno as fkod,
case when (ftip='G' and kaynak in ('@iscari@') ) then round(geneltoplam,2) else 0 end AS giris,
case when (ftip='C' and kaynak in ('@iscari@') ) then round(geneltoplam,2) else 0 end AS cikis,
case when (ftip='C' and hedef in ('@iscari@') ) then round(geneltoplam,2) else 0 end AS girisx,
case when (ftip='G' and hedef in ('@iscari@') ) then round(geneltoplam,2) else 0 end AS cikisx
from fatura as f inner join islem_turleri as b
on (f.cari_tip=b.kcari and f.islem_turu=b.mcari) 
INNER JOIN tblcasabit as c ON f.hedef = c.CARI_KOD
INNER JOIN tblcasabit as cx ON f.kaynak = cx.CARI_KOD
WHERE
@tarih_kriter@
@fisno_kriter@
@hartip_kriter@
@irs_kriter@
(f.KAYNAK = '@iscari@' OR f.HEDEF='@iscari@')
group by inckeyno
ORDER BY tarih
)as t;

