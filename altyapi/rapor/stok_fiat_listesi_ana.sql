set @kodbenzer='kasap%';
select stok_kodu,stok_adi,round(satis_fiat1,2) from tblstsabit where stok_kodu like @kodbenzer order by stok_adi 