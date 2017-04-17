SELECT f.tarih, fno, c.cari_isim, c.vergi_numarasi, (
CASE WHEN h.kdvoran =1  THEN round(sum(h.miktar * h.nf), 2 ) ELSE 0 END ) AS k1top, kdv1top, (
CASE WHEN h.kdvoran =8  THEN round(sum(h.miktar * h.nf), 2 ) ELSE 0 END ) AS k8top, kdv8top, (
CASE WHEN h.kdvoran =18 THEN round(sum(h.miktar * h.nf), 2 ) ELSE 0 END ) AS k18top, kdv18top,(
CASE WHEN f.ftip = 'G'  THEN 'ALIS' ELSE 'SATIS' END ) AS tip,f.geneltoplam
FROM fatura AS f
INNER JOIN tblcasabit AS c ON f.hedef = c.cari_kod
INNER JOIN sthar AS h ON h.finckeyno = f.inckeyno
WHERE fno REGEXP '^[0-9]+$'
AND f.tarih between '2015-01-01' and '2015-03-01'
GROUP BY h.finckeyno, h.kdvoran