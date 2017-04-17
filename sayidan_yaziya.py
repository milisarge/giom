# -*- coding: utf-8 -*-

def ucluyuVer(sayi):
    birler = ["","Bir","Iki","Uc","Dort","Bes","Alti","Yedi","Sekiz","Dokuz"]
    onlar = ["","On","Yirmi","Otuz","Kirk","Elli","Altmis","Yetmis","Seksen","Doksan"]
    yuzler = [i+"Yuz" for i in birler]
    yuzler[1] = "Yuz"

    basamaklar = [birler,onlar,yuzler]
    
    sayi = sayi[::-1]
    yazi,bs = [],0
    for i in sayi:
        rakam = sayi[bs]
        bs += 1
        if rakam != "0":
            yazi.append(basamaklar[bs-1][int(rakam)])
    return "".join(reversed(yazi))

ucluler=["","Bin","Milyon","Milyar","Trilyon","Katrilyon","Kentilyon",
         "Sekstilyon","Oktilyon","Nonilyon","Desilyon"]

def cevir(sayi):
    sayi = '{:,}'.format(int(sayi))
    haneler = reversed(sayi.split(","))
    uclus,sonuc = 0,[]
    for hane in haneler:
        uclu = ucluyuVer(hane)
        if uclu != "":
            if uclus == 1 and uclu == "Bir" :
                sonuc.append(ucluler[uclus])
            else :
                sonuc.append(uclu+""+ucluler[uclus])
        uclus+=1
    son = "".join(reversed(sonuc))
    return son
