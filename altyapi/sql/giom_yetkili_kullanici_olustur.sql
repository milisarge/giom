
INSERT INTO `kullanici` (`ID`, `isim`, `sifre`, `uzun_isim`, `eposta`, `kayit_tarihi`, `yetki_duzey`) VALUES (1,'yetkili','giom*123','yetkili kullanıcı','yetkili@test.com','2017-01-01 01:00:00',99);

INSERT INTO `kul_ayar` (`ayar_no`, `kul_no`, `ayar_bas`, `ayar_deger`, `kayit_tarihi`) VALUES
(1001,999,'prog_anadizin','/opt//giom','2017-01-01 01:01:01'),
(1002,999,'stoklist_db','stoklist.db','2017-01-01 01:01:02'),
(1003,999,'db_dizin','/opt/giom/stk_yedek/','2017-01-01 01:01:03'),
(1004,999,'veritabani','giom','2017-01-01 01:01:04'),
(1005,999,'kayan_yazilar','*** GİOM ***#HIZLI KAYIT->VERİMLİ RAPORLAR->SÜREKLİ GELİŞEN SİSTEM#MİLLİ YAZILIM GÜÇLÜ DEVLET','2017-01-01 01:01:05'),
(1006,999,'yzc_dizayn_kalem@1','14','2017-01-01 01:01:06'),
(1007,999,'yzc_dizayn_kalem@2','36','2017-01-01 01:01:07'),
(1008,999,'yzc_dizayn_kalem@3','36','2017-01-01 01:01:08'),
(1009,999,'yzc_dizayn_kalem@4','35','2017-01-01 01:01:09'),
(1010,999,'arkaplan_renk','#669999','2017-01-01 01:01:10'),
(1011,999,'pos_sifre','posaktar123456789','2017-01-01 01:01:11'),
(1012,999,'pos_dizin','pos','2017-01-01 01:01:12'),
(1013,999,'pos_dizin_sablon','pos\\sablon\\','2017-01-01 01:01:13'),
(1014,1,'etoku_dizin','/opt/giom/etoku','2017-01-01 01:01:14'),
(1015,1,'merkez_cari','10','2017-01-01 01:01:15'),
(1016,1,'merkez_sube','merkez','2017-01-01 01:01:16'),
(1017,1,'f_noktasi','10','2017-01-01 01:01:17'),
(1018,1,'k_noktasi','K10','2017-01-01 01:01:18'),
(1019,1,'b_noktasi','B10','2017-01-01 01:01:19'),
(1020,1,'pos_cari','@101','2017-01-01 01:01:20');

INSERT INTO `tblcasabit` (`SUBE_KODU`, `ISLETME_KODU`, `CARI_KOD`, `CARI_TEL`, `CARI_IL`, `ULKE_KODU`, `CARI_ISIM`, `CARI_TIP`, `GRUP_KODU`, 
`RAPOR_KODU1`, `RAPOR_KODU2`, `RAPOR_KODU3`, `RAPOR_KODU4`, `IBAN`, `CARI_ADRES`, `CARI_ILCE`, `VERGI_DAIRESI`, `VERGI_NUMARASI`, `FAX`, `POSTAKODU`, 
`DETAY_KODU`, `NAKLIYE_KATSAYISI`, `RISK_SINIRI`, `TEMINATI`, `CARISK`, `CCRISK`, `SARISK`, `SCRISK`, `CM_BORCT`, `CM_ALACT`, `CM_RAP_TARIH`, 
`KOSULKODU`, `ISKONTO_ORANI`, `VADE_GUNU`, `LISTE_FIATI`, `ACIK1`, `ACIK2`, `ACIK3`, `M_KOD`, `DOVIZ_TIPI`, `DOVIZ_TURU`, `HESAPTUTMASEKLI`, 
`DOVIZLIMI`, `UPDATE_KODU`, `PLASIYER_KODU`, `LOKALDEPO`, `EMAIL`, `WEB`, `KURFARKIBORC`, `KURFARKIALAC`, `S_YEDEK1`, `S_YEDEK2`, `F_YEDEK1`, 
`F_YEDEK2`, `C_YEDEK1`, `C_YEDEK2`, `B_YEDEK1`, `I_YEDEK1`, `L_YEDEK1`, `FIYATGRUBU`, `KAYITYAPANKUL`, `KAYITTARIHI`, `DUZELTMEYAPANKUL`, 
`DUZELTMETARIHI`, `ODEMETIPI`, `ONAYTIPI`, `ONAYNUM`, `MUSTERIBAZIKDV`, `AGIRLIK_ISK`, `CARI_TEL2`, `CARI_TEL3`, `FAX2`, `GSM1`, `GSM2`) 
VALUES 
(0,0,'10','',NULL,NULL,'DENEME SIRKET MERKEZ','F','merkez','rapor_kodu_degeri',NULL,NULL,NULL,'','',NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,
NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL);
