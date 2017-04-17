set @onek := '@onek@';
set @caritip := '@caritip@';
select max(fno) from fatura where fno like concat(@onek,'0%') and cari_tip=@caritip