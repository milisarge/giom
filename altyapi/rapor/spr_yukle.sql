set @sprno:='@sprno@';
select stok_kodu,stok_adi,
round(sprmik,2),
round(satis_fiat3,3),
round(satis_fiat3*sprmik,3) 
from dp_otospr where osn=@sprno