import numpy as np
import matplotlib.pyplot as plt

class Kural:
    def __init__(self,norm,kosullar,cikarim_sistemi):
        self.norm=norm
        self.kosullar=kosullar#'ozellik_ad':'','uf_ad':'' #uf=uyelik fonksiyonu
        self.cikarim_sistemi=cikarim_sistemi

class CikarimSistemi:
    def __init__(self,tur="Tsk"):
        self.tur=tur#ad olarak kaliyor

    def fonksiyon(self,girdi):#bulanik cikis fonksiyonu #disardan duzenlenecek
        return 10

class UyelikFonksiyonu:
    def __init__(self,ad):
        self.ad = ad

    def fonksiyon(self,girdi):#disardan duzenlenecek
        return 1

class Ozellik:
    def __init__(self,ad):
        self.ad = ad
        self._uyelik_fonksiyonlari=[]

    def uyelik_fonksiyonu_ekle(self,uyelik_fonksiyonu):
        self._uyelik_fonksiyonlari.append(uyelik_fonksiyonu)

    def _uf_indexleri_belirle(self):
        self._indexler={}
        for i in range(len(self._uyelik_fonksiyonlari)):
            self._indexler[self._uyelik_fonksiyonlari[i].ad]=i

    def uf_don(self,ad):
        self._uf_indexleri_belirle()#yeri optimum degil !!!
        return self._uyelik_fonksiyonlari[self._indexler[ad]]

class Durulastirma:
    #her fonk.nun girdisi farkli bulanik cikisa gore degisiyor
    def _agirlikli_ortalama(self,girdi):
        #girdi =agirliklar,degerler bulanik cikistan gelecek
        agirliklar=girdi[0]
        degerler=girdi[1]
        t=0
        c=1
        for i in range(len(agirliklar)):
            t+=agirliklar[i]*degerler[i]
            c*=agirliklar[i]
        return t/c

    def _agirlik_merkezi(self,girdi):
        return 1
    def _en_buyuk_uyelik(self,girdi):
        return 1
    def _en_buyuklerin_kucugu(self,girdi):
        return 1
    def _en_kucuklerin_buyugu(self,girdi):
        return 1
    def uygula(self,yontem_adi,girdi):
        if yontem_adi == "agirlikli_ortalama":
            return self._agirlikli_ortalama(girdi)

        elif yontem_adi == "agirlik_merkezi":
            return self._agirlik_merkezi(girdi)

        elif yontem_adi == "en_buyuk_uyelik":
            return self._en_buyuk_uyelik(girdi)

        elif yontem_adi == "en_buyuklerin_kucugu":
            return self._en_buyuklerin_kucugu(girdi)

        elif yontem_adi == "en_kucuklerin_buyugu(":
            return self._en_kucuklerin_buyugu(girdi)

class Model:
    def __init__(self,durulastirma_yontemi_adi):
        self.kurallar=[]
        self.ozellikler=[]
        self.dya=durulastirma_yontemi_adi

    def kural_ekle(self,kural):
        self.kurallar.append(kural)

    def ozellik_ekle(self,ozellik):
        self.ozellikler.append(ozellik)

    def _ozellik_indexleri_belirle(self):
        indexler={}
        for i in range(len(self.ozellikler)):
            indexler[self.ozellikler[i].ad]=i
        return indexler

    def kurallari_islet(self,girdi):
        #kurallari islet bulaniklastir durulastir

        ozellikler = [i for i in girdi.keys()]
        degerler = [i for i in girdi.values()]
        ozellik_indexleri=self._ozellik_indexleri_belirle()

        w = []
        kural_sonuclari=[]
        for i in range(len(self.kurallar)):#kurallar uygulaniyor
            ciktilar=[]
            for j in range(len(ozellikler)):
                #bulaniklastirma
                oz=ozellikler[j]
                uyelik_fonk_adi=self.kurallar[i].kosullar[oz]#'ozellik'
                ozellik=self.ozellikler[ozellik_indexleri[oz]]
                uf=ozellik.uf_don(uyelik_fonk_adi)
                x=uf.fonksiyon(degerler[j])#model ozelligi icin normal uf unu islet
                ciktilar.append(x)

            #cikarim sistemi
            if self.kurallar[i].norm=="ve":#w seçiliyor
                ek=np.min(np.array(ciktilar))
                w.append(ek)
                bulanik_cikis=self.kurallar[i].cikarim_sistemi.fonksiyon([girdi,ek])
            else:#"veya"
                eb=np.max(np.array(ciktilar))
                w.append(eb)
                bulanik_cikis =self.kurallar[i].cikarim_sistemi.fonksiyon([girdi,eb])

            kural_sonuclari.append(bulanik_cikis)
            print(str(self.kurallar[i].kosullar), " uygulandi")

        # durulastirma
        if self.dya=="agirlikli_ortalama":
            giris=[w,kural_sonuclari]
            return Durulastirma().uygula("agirlikli_ortalama",giris)

        return 1

m=Model("agirlikli_ortalama")
x=Ozellik("x")

def x_buyuk(girdi):
    if girdi <= 4 and girdi >= -4:
        return 0.125*girdi+0.5
    return 0
x_buyuk_uf=UyelikFonksiyonu("buyuk")
x_buyuk_uf.fonksiyon=x_buyuk
x.uyelik_fonksiyonu_ekle(x_buyuk_uf)

def x_kucuk(girdi):
    if girdi <= 4 and girdi >= -4:
        return -0.125*girdi+0.5
    return 0

x_kucuk_uf=UyelikFonksiyonu("kucuk")
x_kucuk_uf.fonksiyon=x_kucuk
x.uyelik_fonksiyonu_ekle(x_kucuk_uf)
m.ozellik_ekle(x)

y=Ozellik("y")

def y_buyuk(girdi):
    if girdi <= 2 and girdi >= -2:
        return 0.25*girdi+0.5
    return 0
y_buyuk_uf=UyelikFonksiyonu("buyuk")
y_buyuk_uf.fonksiyon=y_buyuk
y.uyelik_fonksiyonu_ekle(y_buyuk_uf)

def y_kucuk(girdi):
    if girdi <= 2 and girdi >= -2:
        return -0.25*girdi+0.5
    return 0

y_kucuk_uf=UyelikFonksiyonu("kucuk")
y_kucuk_uf.fonksiyon=y_kucuk
y.uyelik_fonksiyonu_ekle(y_kucuk_uf)
m.ozellik_ekle(y)

tsk_cs1=CikarimSistemi("Tsk")
def bulanik_tsk_cs1(girdi):
    girdi,w=girdi
    x,y=girdi['x'],girdi['y']
    return -x+y+1
tsk_cs1.fonksiyon=bulanik_tsk_cs1

tsk_cs2=CikarimSistemi("Tsk")
def bulanik_tsk_cs2(girdi):
    girdi, w = girdi
    x, y = girdi['x'], girdi['y']
    return -y+3
tsk_cs2.fonksiyon=bulanik_tsk_cs2

tsk_cs3=CikarimSistemi("Tsk")
def bulanik_tsk_cs3(girdi):
    girdi, w = girdi
    x, y = girdi['x'], girdi['y']
    return -x+3
tsk_cs3.fonksiyon=bulanik_tsk_cs3

tsk_cs4=CikarimSistemi("Tsk")
def bulanik_tsk_cs4(girdi):
    girdi, w = girdi
    x, y = girdi['x'], girdi['y']
    return x+y+2
tsk_cs4.fonksiyon=bulanik_tsk_cs4

m.kural_ekle(Kural('ve',{'x':'kucuk','y':'kucuk'},tsk_cs1))
m.kural_ekle(Kural('ve',{'x':'kucuk','y':'buyuk'},tsk_cs2))
m.kural_ekle(Kural('ve',{'x':'buyuk','y':'kucuk'},tsk_cs3))
m.kural_ekle(Kural('ve',{'x':'buyuk','y':'buyuk'},tsk_cs4))
print(m.kurallari_islet({'x':-3,'y':1}))
