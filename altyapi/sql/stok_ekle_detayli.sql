insert into tblstsabit (stok_kodu,stok_adi, barkod1,barkod2,barkod3,barkod4,barkod5,barkod6,alis_kdv_kodu,kdv_orani,satis_fiat1,satis_fiat2,satis_fiat3,
alis_fiat1,alis_fiat2,alis_fiat3,grup_kodu,sube_kodu,isletme_kodu,satici_kodu,olcu_br1,olcu_br2,kod_1,kod_2,kod_3,kod_4,kod_5,birim_agirlik,payda_1)
values ('@kod@','@isim@','@barkod1@','@barkod2@','@barkod3@','@barkod4@','@barkod5@','@barkod6@','@alkdv@','@satkdv@','@satis_fiat1@','@satis_fiat2@','@satis_fiat3@',
'@alis_fiat1@','@alis_fiat2@','@alis_fiat3@','@grupkod@',-1,-1,'@satici_kodu@','@olcu_br1@','@olcu_br2@','@kod_1@','@kod_2@','@kod_3@','@kod_4@','@kod_5@','@birim_agirlik@','@payda@');