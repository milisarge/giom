select t.kaynak,round(sum(t.yardc+t.yardg+t.yardc2+t.yardg2),2) as devredecek
from(
select
kaynak,
case when (ftip='C' and kaynak in ('@kaynak@') and tarih < now()) then geneltoplam*-1 else 0 end as yardc,
case when (ftip='G' and kaynak in ('@kaynak@') and tarih < now()) then geneltoplam else 0 end as yardg,
case when (ftip='G' and hedef in ('@kaynak@') and tarih < now())  then geneltoplam*-1 else 0 end as yardc2,
case when (ftip='C' and hedef in ('@kaynak@') and tarih < now())  then geneltoplam else 0 end as yardg2
from fatura
) as t