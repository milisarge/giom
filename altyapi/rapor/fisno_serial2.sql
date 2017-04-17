set @onek := '@onek@';
set @gctur := '@gctur@';
select max(fno) from fatura where fno like concat(@onek,'0%') and ftip=@gctur