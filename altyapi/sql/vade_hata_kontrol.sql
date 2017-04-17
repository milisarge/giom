select t.fis,t.gt-t.kt from (
SELECT kayityapankul as kyd, fno as fis, sum(geneltoplam) as gt, kdtutar as kt
FROM fatura
GROUP BY fno) as t
where t.gt-t.kt<>0 and t.kyd<>"giom14"
