select round(sum(t.dundc+t.dundg+t.dundc2+t.dundg2),2) as devreden,round(sum(t.yardc+t.yardg+t.yardc2+t.yardg2),2) as devredecek
from(
select
case when (ftip='C' and kaynak in ('@kaynak@') and tarih < '@tarih@') then geneltoplam*-1 else 0 end as dundc,
case when (ftip='G' and kaynak in ('@kaynak@') and tarih < '@tarih@') then geneltoplam else 0 end as dundg,
case when (ftip='G' and hedef in ('@kaynak@') and tarih < '@tarih@') then geneltoplam*-1 else 0 end as dundc2,
case when (ftip='C' and hedef in ('@kaynak@') and tarih < '@tarih@') then geneltoplam else 0 end as dundg2,
case when (ftip='C' and kaynak in ('@kaynak@') and tarih < DATE_ADD('@tarih@', INTERVAL 1 DAY)) then geneltoplam*-1 else 0 end as yardc,
case when (ftip='G' and kaynak in ('@kaynak@') and tarih < DATE_ADD('@tarih@', INTERVAL 1 DAY)) then geneltoplam else 0 end as yardg,
case when (ftip='G' and hedef in ('@kaynak@') and tarih < DATE_ADD('@tarih@', INTERVAL 1 DAY)) then geneltoplam*-1 else 0 end as yardc2,
case when (ftip='C' and hedef in ('@kaynak@') and tarih < DATE_ADD('@tarih@', INTERVAL 1 DAY)) then geneltoplam else 0 end as yardg2
from fatura
) as t

