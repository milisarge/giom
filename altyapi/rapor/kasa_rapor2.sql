set @dbakiye := 0;
select t.tarih,t.isim,t.ack,round(t.giris,2)+round(t.girisx,2) as giriþ,round(t.cikis,2)+round(t.cikisx,2) as çýkýþ, 
round((@dbakiye := @dbakiye + (giris+girisx)-(cikis+cikisx)),2) as bakiye,t.med from
(SELECT date(fatura.TARIH) as tarih, 
case when fatura.KAYNAK = '@kaynak@' then tblcasabit.CARI_ISIM else cx.cari_isim end  as isim,
fatura.ACIKLAMA as ack,
case when (ftip='G' and kaynak in ('@kaynak@') ) then round(geneltoplam,2) else 0 end AS giris,
case when (ftip='C' and kaynak in ('@kaynak@') ) then round(geneltoplam,2) else 0 end AS cikis,
case when (ftip='C' and hedef in ('@kaynak@') ) then round(geneltoplam,2) else 0 end AS girisx,
case when (ftip='G' and hedef in ('@kaynak@') ) then round(geneltoplam,2) else 0 end AS cikisx,
fatura.med as med
FROM fatura
INNER JOIN tblcasabit ON fatura.HEDEF = tblcasabit.CARI_KOD
INNER JOIN tblcasabit as cx ON fatura.kaynak = cx.CARI_KOD
WHERE (fatura.KAYNAK = '@kaynak@' OR fatura.HEDEF='@kaynak@')
AND (fatura.TARIH BETWEEN '@bastarih@' AND '@sontarih@')
ORDER BY tarih
)as t;