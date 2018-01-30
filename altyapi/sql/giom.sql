-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 17, 2017 at 04:03 AM
-- Server version: 10.1.11-MariaDB
-- PHP Version: 5.6.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `giom`
--
-- --------------------------------------------------------

--
-- Table structure for table `etiket_basilan`
--

CREATE TABLE `etiket_basilan` (
  `stok_kodu` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `bf` decimal(28,8) NOT NULL,
  `basim_tarihi` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `fatura`
--

CREATE TABLE `fatura` (
  `KAYNAK` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `FTIP` char(1) COLLATE utf8_unicode_ci NOT NULL,
  `FNO` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `HEDEF` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `TARIH` datetime NOT NULL,
  `KHTUTAR` decimal(28,8) DEFAULT '0.00000000',
  `SAT_ISKT_TOP` decimal(28,8) DEFAULT '0.00000000',
  `MFAZ_ISKT_TOP` decimal(28,8) DEFAULT '0.00000000',
  `GEN_ISK1T` decimal(28,8) DEFAULT '0.00000000',
  `GEN_ISK2T` decimal(28,8) DEFAULT '0.00000000',
  `GEN_ISK3T` decimal(28,8) DEFAULT '0.00000000',
  `GEN_ISK1O` decimal(28,8) DEFAULT '0.00000000',
  `GEN_ISK2O` decimal(28,8) DEFAULT '0.00000000',
  `GEN_ISK3O` decimal(28,8) DEFAULT '0.00000000',
  `KDVTOPLAM` decimal(28,8) DEFAULT '0.00000000',
  `FAT_ALTISK` decimal(28,8) DEFAULT '0.00000000',
  `FAT_ALTISK2` decimal(28,8) DEFAULT '0.00000000',
  `ACIKLAMA` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KDVDURUM` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `FATKALEM_ADEDI` smallint(6) DEFAULT NULL,
  `TOPLAM_MIK` decimal(15,5) DEFAULT NULL,
  `KDTUTAR` decimal(28,8) DEFAULT '0.00000000',
  `GENELTOPLAM` decimal(28,8) DEFAULT '0.00000000',
  `IRS` varchar(1) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'H',
  `TAKIPKOD` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KAYITYAPANKUL` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KAYITTARIHI` datetime DEFAULT NULL,
  `DUZELTMEYAPANKUL` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DUZELTMETARIHI` datetime DEFAULT NULL,
  `KDV1TOP` decimal(28,8) DEFAULT '0.00000000',
  `KDV8TOP` decimal(28,8) DEFAULT '0.00000000',
  `KDV18TOP` decimal(28,8) DEFAULT '0.00000000',
  `VADE_TARIHI` datetime DEFAULT NULL,
  `INCKEYNO` int(8) NOT NULL DEFAULT '1',
  `CARI_TIP` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ISLEM_TURU` char(1) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Z',
  `MED` char(1) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'H'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `giris_liste`
--

CREATE TABLE `giris_liste` (
  `id` int(11) NOT NULL,
  `durum` varchar(1) NOT NULL,
  `zaman` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `grup_kodlari`
--

CREATE TABLE `grup_kodlari` (
  `grupkodu` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `grupadi` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `islem_turleri`
--

CREATE TABLE `islem_turleri` (
  `mcari` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `kcari` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `gcmod` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `tur` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kullanici`
--

CREATE TABLE `kullanici` (
  `ID` int(20) UNSIGNED NOT NULL,
  `isim` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `sifre` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `uzun_isim` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `eposta` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `kayit_tarihi` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `yetki_duzey` int(11) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `kul_ayar`
--

CREATE TABLE `kul_ayar` (
  `ayar_no` int(20) UNSIGNED NOT NULL,
  `kul_no` int(20) UNSIGNED NOT NULL DEFAULT '0',
  `ayar_bas` varchar(255) DEFAULT NULL,
  `ayar_deger` varchar(255) DEFAULT NULL,
  `kayit_tarihi` datetime NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sthar`
--

CREATE TABLE `sthar` (
  `STOK_KODU` varchar(35) COLLATE utf8_unicode_ci NOT NULL,
  `FISNO` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `MIKTAR` decimal(28,8) DEFAULT '0.00000000',
  `TARIH` datetime NOT NULL,
  `NF` decimal(28,8) DEFAULT '0.00000000',
  `BF` decimal(28,8) DEFAULT '0.00000000',
  `KDVORAN` decimal(5,2) DEFAULT '0.00',
  `ACIKLAMA` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SATISK` decimal(28,8) DEFAULT '0.00000000',
  `MALFISK` decimal(28,8) DEFAULT '0.00000000',
  `FTIP` char(1) COLLATE utf8_unicode_ci NOT NULL,
  `SATISK2` decimal(28,8) DEFAULT '0.00000000',
  `SATISK3` decimal(28,8) DEFAULT '0.00000000',
  `HEDEF` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `PLASIYER_KODU` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TAKIPKOD` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TAKIPKOD2` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SIRA` smallint(6) DEFAULT NULL,
  `IRSALIYE_NO` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `IRSALIYE_TARIH` datetime DEFAULT NULL,
  `OLCUBR` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `INCKEYNO` int(11) NOT NULL,
  `VADE_TARIHI` datetime DEFAULT NULL,
  `KAYNAK` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `DUZELTMETARIHI` datetime NOT NULL,
  `KAYITTARIHI` datetime NOT NULL,
  `FINCKEYNO` int(6) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblcasabit`
--

CREATE TABLE `tblcasabit` (
  `SUBE_KODU` smallint(6) NOT NULL,
  `ISLETME_KODU` smallint(6) NOT NULL,
  `CARI_KOD` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `CARI_TEL` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CARI_IL` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ULKE_KODU` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CARI_ISIM` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CARI_TIP` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `GRUP_KODU` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `RAPOR_KODU1` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `RAPOR_KODU2` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `RAPOR_KODU3` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `RAPOR_KODU4` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `IBAN` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CARI_ADRES` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CARI_ILCE` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `VERGI_DAIRESI` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `VERGI_NUMARASI` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `FAX` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `POSTAKODU` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DETAY_KODU` smallint(6) DEFAULT NULL,
  `NAKLIYE_KATSAYISI` decimal(28,8) DEFAULT NULL,
  `RISK_SINIRI` decimal(28,8) DEFAULT NULL,
  `TEMINATI` decimal(28,8) DEFAULT NULL,
  `CARISK` decimal(28,8) DEFAULT NULL,
  `CCRISK` decimal(28,8) DEFAULT NULL,
  `SARISK` decimal(28,8) DEFAULT NULL,
  `SCRISK` decimal(28,8) DEFAULT NULL,
  `CM_BORCT` decimal(28,8) DEFAULT NULL,
  `CM_ALACT` decimal(28,8) DEFAULT NULL,
  `CM_RAP_TARIH` datetime DEFAULT NULL,
  `KOSULKODU` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ISKONTO_ORANI` decimal(28,2) DEFAULT NULL,
  `VADE_GUNU` smallint(6) DEFAULT NULL,
  `LISTE_FIATI` tinyint(4) DEFAULT NULL,
  `ACIK1` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ACIK2` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ACIK3` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `M_KOD` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DOVIZ_TIPI` tinyint(4) DEFAULT NULL,
  `DOVIZ_TURU` tinyint(4) DEFAULT NULL,
  `HESAPTUTMASEKLI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DOVIZLIMI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `UPDATE_KODU` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `PLASIYER_KODU` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `LOKALDEPO` smallint(6) DEFAULT NULL,
  `EMAIL` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `WEB` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KURFARKIBORC` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KURFARKIALAC` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `S_YEDEK1` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `S_YEDEK2` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `F_YEDEK1` decimal(28,8) DEFAULT NULL,
  `F_YEDEK2` decimal(28,8) DEFAULT NULL,
  `C_YEDEK1` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `C_YEDEK2` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `B_YEDEK1` tinyint(4) DEFAULT NULL,
  `I_YEDEK1` smallint(6) DEFAULT NULL,
  `L_YEDEK1` int(11) DEFAULT NULL,
  `FIYATGRUBU` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KAYITYAPANKUL` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KAYITTARIHI` datetime DEFAULT NULL,
  `DUZELTMEYAPANKUL` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DUZELTMETARIHI` datetime DEFAULT NULL,
  `ODEMETIPI` tinyint(4) DEFAULT NULL,
  `ONAYTIPI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ONAYNUM` int(11) DEFAULT NULL,
  `MUSTERIBAZIKDV` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `AGIRLIK_ISK` decimal(28,8) DEFAULT NULL,
  `CARI_TEL2` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CARI_TEL3` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `FAX2` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `GSM1` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `GSM2` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblstsabit`
--

CREATE TABLE `tblstsabit` (
  `SUBE_KODU` smallint(6) NOT NULL,
  `ISLETME_KODU` smallint(6) NOT NULL,
  `STOK_KODU` varchar(35) COLLATE utf8_unicode_ci NOT NULL,
  `URETICI_KODU` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `STOK_ADI` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `GRUP_KODU` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KOD_1` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KOD_2` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KOD_3` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KOD_4` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KOD_5` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SATICI_KODU` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `OLCU_BR1` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `OLCU_BR2` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `PAY_1` decimal(28,8) DEFAULT NULL,
  `PAYDA_1` decimal(28,8) DEFAULT NULL,
  `OLCU_BR3` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `PAY2` decimal(28,8) DEFAULT NULL,
  `PAYDA2` decimal(28,8) DEFAULT NULL,
  `FIAT_BIRIMI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `AZAMI_STOK` decimal(28,8) DEFAULT NULL,
  `ASGARI_STOK` decimal(28,8) DEFAULT NULL,
  `TEMIN_SURESI` decimal(28,8) DEFAULT NULL,
  `KUL_MIK` decimal(28,8) DEFAULT NULL,
  `RISK_SURESI` smallint(6) DEFAULT NULL,
  `ZAMAN_BIRIMI` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SATIS_FIAT1` decimal(28,8) DEFAULT NULL,
  `SATIS_FIAT2` decimal(28,8) DEFAULT NULL,
  `SATIS_FIAT3` decimal(28,8) DEFAULT NULL,
  `SATIS_FIAT4` decimal(28,8) DEFAULT NULL,
  `SAT_DOV_TIP` tinyint(4) DEFAULT NULL,
  `DOV_ALIS_FIAT` decimal(28,8) DEFAULT NULL,
  `DOV_MAL_FIAT` decimal(28,8) DEFAULT NULL,
  `DOV_SATIS_FIAT` decimal(28,8) DEFAULT NULL,
  `MUH_DETAYKODU` smallint(6) DEFAULT NULL,
  `BIRIM_AGIRLIK` decimal(28,8) DEFAULT NULL,
  `NAKLIYET_TUT` decimal(28,8) DEFAULT NULL,
  `KDV_ORANI` decimal(5,2) DEFAULT NULL,
  `ALIS_DOV_TIP` tinyint(4) DEFAULT NULL,
  `DEPO_KODU` smallint(6) DEFAULT NULL,
  `DOV_TUR` tinyint(4) DEFAULT NULL,
  `URET_OLCU_BR` tinyint(4) DEFAULT NULL,
  `BILESENMI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `MAMULMU` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `FORMUL_TOPLAMI` decimal(28,8) DEFAULT NULL,
  `UPDATE_KODU` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `MAX_ISKONTO` decimal(28,8) DEFAULT NULL,
  `ECZACI_KARI` decimal(28,8) DEFAULT NULL,
  `MIKTAR` decimal(28,8) DEFAULT NULL,
  `MAL_FAZLASI` decimal(28,8) DEFAULT NULL,
  `KDV_TENZIL_ORAN` decimal(28,8) DEFAULT NULL,
  `KILIT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ONCEKI_KOD` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SONRAKI_KOD` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BARKOD1` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BARKOD2` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BARKOD3` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ALIS_KDV_KODU` decimal(5,2) DEFAULT NULL,
  `ALIS_FIAT1` decimal(28,8) DEFAULT NULL,
  `ALIS_FIAT2` decimal(28,8) DEFAULT NULL,
  `ALIS_FIAT3` decimal(28,8) DEFAULT NULL,
  `ALIS_FIAT4` decimal(28,8) DEFAULT NULL,
  `LOT_SIZE` decimal(28,8) DEFAULT NULL,
  `MIN_SIP_MIKTAR` decimal(28,8) DEFAULT NULL,
  `SABIT_SIP_ARALIK` smallint(6) DEFAULT NULL,
  `SIP_POLITIKASI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `OZELLIK_KODU1` tinyint(4) DEFAULT NULL,
  `OZELLIK_KODU2` tinyint(4) DEFAULT NULL,
  `OZELLIK_KODU3` tinyint(4) DEFAULT NULL,
  `OZELLIK_KODU4` tinyint(4) DEFAULT NULL,
  `OZELLIK_KODU5` tinyint(4) DEFAULT NULL,
  `OPSIYON_KODU1` tinyint(4) DEFAULT NULL,
  `OPSIYON_KODU2` tinyint(4) DEFAULT NULL,
  `OPSIYON_KODU3` tinyint(4) DEFAULT NULL,
  `OPSIYON_KODU4` tinyint(4) DEFAULT NULL,
  `OPSIYON_KODU5` tinyint(4) DEFAULT NULL,
  `BILESEN_OP_KODU` tinyint(4) DEFAULT NULL,
  `SIP_VER_MAL` decimal(28,8) DEFAULT NULL,
  `ELDE_BUL_MAL` decimal(28,8) DEFAULT NULL,
  `YIL_TAH_KUL_MIK` decimal(28,8) DEFAULT NULL,
  `EKON_SIP_MIKTAR` decimal(28,8) DEFAULT NULL,
  `ESKI_RECETE` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `OTOMATIK_URETIM` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ALFKOD` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SAFKOD` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `KODTURU` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `S_YEDEK1` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `S_YEDEK2` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `F_YEDEK3` decimal(28,8) DEFAULT NULL,
  `F_YEDEK4` decimal(28,8) DEFAULT NULL,
  `C_YEDEK5` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `C_YEDEK6` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `B_YEDEK7` tinyint(4) DEFAULT NULL,
  `I_YEDEK8` smallint(6) DEFAULT NULL,
  `L_YEDEK9` int(11) DEFAULT NULL,
  `D_YEDEK10` datetime DEFAULT NULL,
  `GIRIS_SERI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CIKIS_SERI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SERI_BAK` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SERI_MIK` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SERI_GIR_OT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SERI_CIK_OT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SERI_BASLANGIC` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `FIYATKODU` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `FIYATSIRASI` int(11) DEFAULT NULL,
  `PLANLANACAK` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `LOT_SIZECUSTOMER` decimal(28,8) DEFAULT NULL,
  `MIN_SIP_MIKTARCUSTOMER` decimal(28,8) DEFAULT NULL,
  `GUMRUKTARIFEKODU` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SON_ALIMYER` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `PERFORMANSKODU` varchar(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SATICISIPKILIT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `MUSTERISIPKILIT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SATINALMAKILIT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SATISKILIT` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `EN` decimal(28,8) DEFAULT NULL,
  `BOY` decimal(28,8) DEFAULT NULL,
  `GENISLIK` decimal(28,8) DEFAULT NULL,
  `SIPLIMITVAR` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SONSTOKKODU` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ONAYTIPI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ONAYNUM` int(11) DEFAULT NULL,
  `FIKTIF_MAM` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `YAPILANDIR` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `SBOMVARMI` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BAGLISTOKKOD` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `YAPKOD` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BARKOD4` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BARKOD5` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `BARKOD6` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `etiket_basilan`
--
ALTER TABLE `etiket_basilan`
  ADD KEY `stok_kodu` (`stok_kodu`);

--
-- Indexes for table `fatura`
--
ALTER TABLE `fatura`
  ADD KEY `INCKEYNO` (`INCKEYNO`);

--
-- Indexes for table `giris_liste`
--
ALTER TABLE `giris_liste`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `grup_kodlari`
--
ALTER TABLE `grup_kodlari`
  ADD KEY `grupkodu` (`grupkodu`);

--
-- Indexes for table `islem_turleri`
--
ALTER TABLE `islem_turleri`
  ADD PRIMARY KEY (`mcari`,`kcari`,`gcmod`);

--
-- Indexes for table `kullanici`
--
ALTER TABLE `kullanici`
  ADD UNIQUE KEY `isim` (`isim`),
  ADD KEY `ID` (`ID`);

--
-- Indexes for table `kul_ayar`
--
ALTER TABLE `kul_ayar`
  ADD KEY `ayar_no` (`ayar_no`);

--
-- Indexes for table `sthar`
--
ALTER TABLE `sthar`
  ADD KEY `INCKEYNO` (`INCKEYNO`);

--
-- Indexes for table `tblcasabit`
--
ALTER TABLE `tblcasabit`
  ADD KEY `CARI_KOD` (`CARI_KOD`);

--
-- Indexes for table `tblstsabit`
--
ALTER TABLE `tblstsabit`
  ADD UNIQUE KEY `STOK_KODU` (`STOK_KODU`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kullanici`
--
ALTER TABLE `kullanici`
  MODIFY `ID` int(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `kul_ayar`
--
ALTER TABLE `kul_ayar`
  MODIFY `ayar_no` int(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1053;
--
-- AUTO_INCREMENT for table `sthar`
--
ALTER TABLE `sthar`
  MODIFY `INCKEYNO` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=286593;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

LOCK TABLES `islem_turleri` WRITE;
/*!40000 ALTER TABLE `islem_turleri` DISABLE KEYS */;
INSERT INTO `islem_turleri` (`mcari`, `kcari`, `gcmod`, `tur`) VALUES ('K','K','G','KASA VİRMANI'),('K','K','C','KASA VİRMANI'),('F','K','G','NAKİT TAHSİLAT'),('K','F','G','NAKİT TAHSİLAT'),('K','F','C','NAKİT TEDİYE'),('B','F','G','HAVALE'),('B','F','C','HAVALE'),('B','B','G','BANKA VİRMANI'),('B','B','C','BANKA VİRMANI'),('M','F','C','KREDİ KARTI ÖDEMESİ'),('M','F','G','KREDİ TAHSİLAT'),('F','F','G','ALIŞ F.'),('F','F','C','SATIŞ F.'),('A','F','G','-'),('A','F','C','-'),('A','K','G','-'),('A','K','C','-'),('A','B','G','-'),('A','B','C','-'),('K','B','G','BANKADAN CEKıLEN'),('K','B','C','BANKAYA YATAN'),('B','A','G','DEVİR BANK GİRİŞ'),('B','A','C','DEVİR BANK ÇIKIŞ'),('B','K','G','BANKAYA YATAN'),('B','K','C','BANKADAN ÇEKİLEN'),('F','K','C','NAKIT TEDIYE'),('B','M','C','KREDİ KARTINA ÖDENEN'),('B','M','G','KREDİ ÖDEME');
/*!40000 ALTER TABLE `islem_turleri` ENABLE KEYS */;
UNLOCK TABLES;
