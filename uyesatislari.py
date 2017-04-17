# -*- coding: utf-8 -*-

class Urun:
    def __init__(self, urunkodu="", urunismi="", miktar="", birim="", birimfiyat="", tutar=""):
        self.urunkodu = urunkodu
        self.urunismi = urunismi
        self.miktar = miktar

        '''birim = 0 ise adet
           birim = 1 ise gram '''
        self.birim = birim
        self.birimfiyat = birimfiyat
        self.tutar = tutar
        self.kdv = 8
        
class Fis:
    def __init__(self, tarih="", saat="", toplamtutar=0, urunler=[]):
        self.tarih = tarih
        self.saat = saat
        self.toplamtutar = toplamtutar
        self.urunler = urunler