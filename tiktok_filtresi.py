# TikTok tarzı filtre uygulaması
# Dört farklı alanda yüz çekimi yapıp farklı efektler uygular
# 1.üçgen parça --> Cartoon Effect (karikatür efekti)
# 2.üçgen parça --> Color Cycling Effect (renk döngüsü efekti)
# 3.üçgen parça --> Pixelate Effect (pikselleştirme efekti)
# 4.üçgen parça --> Glitch Effect (dijital bozulma efekti)

import cv2 as cv
import numpy as np
import time
from math import sin


def ucgen_maske_olustur(cerceve, noktalar):
    """Belirlenen noktalardan üçgen şeklinde bir maske oluşturur"""
    maske = np.zeros(cerceve.shape[:2], dtype=np.uint8)
    cv.fillPoly(maske, [np.array(noktalar, dtype=np.int32)], 255)
    return maske


def merkezdeki_ucgeni_goster(cerceve, ucgenler_verisi, ilerleme):
    """Yakalanan üçgenleri ekranın ortasında gösterir ve uygun kenarlık ekler"""
    yukseklik, genislik = cerceve.shape[:2]
    sonuc = cerceve.copy()

    # Hedef boyut (ekranın %60'ı)
    hedef_boyut = min(genislik, yukseklik) * 0.6

    # Merkez koordinatları
    merkez_x = genislik // 2
    merkez_y = yukseklik // 2

    if ucgenler_verisi:
        # Zoom efekti için boyut hesaplama
        baslangic_boyutu = hedef_boyut * 0.6
        bitis_boyutu = hedef_boyut
        gecerli_boyut = baslangic_boyutu + (bitis_boyutu - baslangic_boyutu) * ilerleme

        olcek = gecerli_boyut / max(genislik, yukseklik)
        yeni_genislik = int(genislik * olcek)
        yeni_yukseklik = int(yukseklik * olcek)
        x = merkez_x - yeni_genislik // 2
        y = merkez_y - yeni_yukseklik // 2

        # Tüm üçgenleri göster
        for resim, noktalar in ucgenler_verisi:
            # Üçgen maskesi oluştur
            maske = ucgen_maske_olustur(resim, noktalar)

            # Görüntüyü yeniden boyutlandır
            boyutlanmis_resim = cv.resize(resim, (yeni_genislik, yeni_yukseklik))
            boyutlanmis_maske = cv.resize(maske, (yeni_genislik, yeni_yukseklik))

            # Sadece üçgen bölgesini göster
            roi = sonuc[y:y + yeni_yukseklik, x:x + yeni_genislik]
            if roi.shape[:2] == boyutlanmis_maske.shape[:2]:  # Boyut kontrolü ekle
                roi[boyutlanmis_maske > 0] = boyutlanmis_resim[boyutlanmis_maske > 0]

        # Özel kenarlık ekle
        renk = (255, 255, 255)  # Beyaz kenarlık rengi
        kalinlik = 10  # Kenarlık kalınlığı

        # Dörtgenin köşe noktaları
        sol_ust = (x, y)
        sag_ust = (x + yeni_genislik - 1, y)
        sol_alt = (x, y + yeni_yukseklik - 1)
        sag_alt = (x + yeni_genislik - 1, y + yeni_yukseklik - 1)

        # İlgili kenarları çiz
        ucgen_sayisi = len(ucgenler_verisi)

        if ucgen_sayisi >= 1:  # Üst üçgen - üst kenar
            cv.line(sonuc, sol_ust, sag_ust, renk, kalinlik)
        if ucgen_sayisi >= 2:  # Sağ üçgen - sağ kenar
            cv.line(sonuc, sag_ust, sag_alt, renk, kalinlik)
        if ucgen_sayisi >= 3:  # Sol üçgen - sol kenar
            cv.line(sonuc, sol_ust, sol_alt, renk, kalinlik)
        if ucgen_sayisi >= 4:  # Alt üçgen - alt kenar
            cv.line(sonuc, sol_alt, sag_alt, renk, kalinlik)

    return sonuc


def karikatur_efekti_uygula(resim, zaman_degeri):
    """Resme çizgi film/karikatür tarzı bir efekt uygular"""
    gri = cv.cvtColor(resim, cv.COLOR_BGR2GRAY)
    gri = cv.medianBlur(gri, 5)  # Gürültüyü azalt
    kenarlar = cv.adaptiveThreshold(gri, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                    cv.THRESH_BINARY, 9, 9)  # Kenarları algıla
    renk = cv.bilateralFilter(resim, 9, 300, 300)  # Renkleri yumuşat ama kenarları koru
    karikatur = cv.bitwise_and(renk, renk, mask=kenarlar)  # Kenarlar üzerinde renkleri göster
    return karikatur


def renk_dongusu_uygula(resim, zaman_degeri):
    """Resmin renk tonlarını zamanla değiştirir"""
    hsv = cv.cvtColor(resim, cv.COLOR_BGR2HSV)  # BGR'den HSV'ye dönüştür
    h, s, v = cv.split(hsv)  # Hue, Saturation ve Value kanallarını ayır

    # Zamanla Hue değerini değiştir (renkleri döndür)
    h = np.mod(h + int(zaman_degeri * 10) % 180, 180).astype(np.uint8)

    # Kanalları birleştir
    hsv = cv.merge([h, s, v])
    return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)  # HSV'den BGR'ye dönüştür


def piksellestirme_uygula(resim, zaman_degeri):
    """Resmi blok pikseller halinde gösterir, piksel boyutu zamanla değişir"""
    blok_boyutu = max(2, 15 + int(10 * sin(zaman_degeri)))  # Min 2 piksel, zamanla değişen boyut
    yukseklik, genislik = resim.shape[:2]

    # Resmi küçült ve sonra eski boyutuna getir (pikselleşme efekti)
    temp = cv.resize(resim, (genislik // blok_boyutu, yukseklik // blok_boyutu))
    return cv.resize(temp, (genislik, yukseklik), interpolation=cv.INTER_NEAREST)


def glitch_efekti_uygula(resim, zaman_degeri):
    """Dijital bozulma (glitch) efekti uygular, zamanla farklılaşan"""
    sonuc = resim.copy()
    yukseklik, genislik = resim.shape[:2]

    # Rastgele yatay kaymalar için tutarlı değişim sağla
    np.random.seed(int(zaman_degeri * 10) % 1000)

    # Rastgele yatay kaymalar ekle
    for i in range(10):
        y = int(np.random.uniform(0, yukseklik))  # Rastgele y pozisyonu
        h = int(np.random.uniform(5, 20))  # Rastgele yükseklik
        kayma = int(np.random.uniform(-20, 20))  # Rastgele kayma miktarı

        if 0 <= y < yukseklik and 0 <= y + h < yukseklik:
            if kayma > 0 and kayma < genislik:
                # Sağa doğru kaydır
                sonuc[y:y + h, kayma:] = sonuc[y:y + h, :genislik - kayma]
                sonuc[y:y + h, :kayma] = 0
            elif kayma < 0 and abs(kayma) < genislik:
                # Sola doğru kaydır
                sonuc[y:y + h, :genislik + kayma] = sonuc[y:y + h, -kayma:]
                sonuc[y:y + h, genislik + kayma:] = 0
    return sonuc


def ilerleme_kenari_ciz(cerceve, noktalar, ilerleme, renk=(37, 37, 252)):
    """Üçgenin kenarlarında ilerleyen bir çizgi çizer, çekimin ilerleme durumunu gösterir"""
    noktalar = np.array(noktalar, dtype=np.int32)
    toplam_uzunluk = 0
    uzunluklar = []

    # Her bir kenar için uzunlukları hesapla
    for i in range(len(noktalar)):
        sonraki_i = (i + 1) % len(noktalar)
        uzunluk = np.sqrt(np.sum((noktalar[sonraki_i] - noktalar[i]) ** 2))
        toplam_uzunluk += uzunluk
        uzunluklar.append(uzunluk)

    gecerli_uzunluk = 0
    hedef_uzunluk = toplam_uzunluk * ilerleme

    # İlerlemeye göre kenarları çiz
    for i in range(len(noktalar)):
        sonraki_i = (i + 1) % len(noktalar)
        baslangic = noktalar[i]
        bitis = noktalar[sonraki_i]

        if gecerli_uzunluk + uzunluklar[i] <= hedef_uzunluk:
            # Kenarın tamamını çiz
            cv.line(cerceve, tuple(baslangic), tuple(bitis), renk, 5)
            gecerli_uzunluk += uzunluklar[i]
        elif gecerli_uzunluk < hedef_uzunluk:
            # Kenarın bir kısmını çiz
            oran = (hedef_uzunluk - gecerli_uzunluk) / uzunluklar[i]
            gecerli_nokta = baslangic + (bitis - baslangic) * oran
            cv.line(cerceve, tuple(baslangic), tuple(gecerli_nokta.astype(int)), renk, 5)
            break

    return cerceve


def yonlendirme_ucgenleri_ciz(cerceve, ucgenler):
    """Kullanıcıya yönlendirme için üçgenlerin içine çekim sırasını gösteren sayıları yerleştirir"""
    sonuc = cerceve.copy()

    # Tüm üçgenleri çiz
    for i, noktalar in enumerate(ucgenler):
        # Yarı saydam siyah arka plan oluştur
        overlay = sonuc.copy()
        cv.fillPoly(overlay, [np.array(noktalar, dtype=np.int32)], (0, 0, 0))

        # Saydam arka planı ekle
        alpha = 0.4  # Düşük opaklık (şeffaflık)
        cv.addWeighted(overlay, alpha, sonuc, 1 - alpha, 0, sonuc)

        # Beyaz kenarlık çiz
        cv.polylines(sonuc, [np.array(noktalar, dtype=np.int32)], True, (255, 255, 255), 4)

        # Üçgen içinde numarayı göster
        numara = str(i + 1)

        # Üçgenin merkezini hesapla
        merkez_x = sum(p[0] for p in noktalar) // len(noktalar)
        merkez_y = sum(p[1] for p in noktalar) // len(noktalar)

        # Sayının boyutunu ve kalınlığını ayarla
        font_olcegi = 5.0
        kalinlik = 8

        # Sayının metin boyutunu al
        (metin_genisligi, metin_yuksekligi), _ = cv.getTextSize(numara, cv.FONT_HERSHEY_SIMPLEX, font_olcegi, kalinlik)

        # Sayının pozisyonunu ayarla
        metin_x = merkez_x - metin_genisligi // 2
        metin_y = merkez_y + metin_yuksekligi // 2

        # Sayıyı çiz
        cv.putText(sonuc, numara, (metin_x, metin_y), cv.FONT_HERSHEY_SIMPLEX,
                   font_olcegi, (255, 255, 255), kalinlik)

    return sonuc


def main():
    """Ana fonksiyon - kamerayı başlatır ve filtreleme işlemini yürütür"""
    # Kamera ayarlarını yap
    kamera = cv.VideoCapture(0)
    kamera.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    kamera.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

    # Değişkenleri başlat
    dondurulmus_ucgenler = []  # Yakalanan üçgen görüntüleri ve koordinatları
    gecerli_ucgen = 0  # Şu anki yakalanan üçgen indeksi
    baslangic_zamani = time.time()
    yakalama_tamamlandi = [False] * 4  # 4 üçgen için yakalama durumu
    asama = "yonlendirme"  # Başlangıç aşaması - kullanıcıya yönlendirme göster
    yonlendirme_baslangici = time.time()
    geri_sayim_baslangici = 0
    geri_sayim_numara = 3
    merkez_gosterim_baslangici = 0
    son_asama = False  # Dört üçgen de yakalandıktan sonraki son aşama
    dalga_baslangici = 0

    while True:
        ret, cerceve = kamera.read()
        if not ret:
            break

        # Görüntüyü yatay olarak aynala (sağ-sol düzeltmesi için)
        cerceve = cv.flip(cerceve, 1)

        yukseklik, genislik = cerceve.shape[:2]
        merkez = (genislik // 2, yukseklik // 2)

        # Dört üçgen noktalarını tanımla
        ucgenler = [
            [(0, 0), merkez, (genislik, 0)],  # Üst üçgen
            [(genislik, 0), merkez, (genislik, yukseklik)],  # Sağ üçgen
            [(0, 0), merkez, (0, yukseklik)],  # Sol üçgen
            [(0, yukseklik), merkez, (genislik, yukseklik)]  # Alt üçgen
        ]

        gosterim_cercevesi = cerceve.copy()
        gecerli_zaman = time.time()

        if asama == "yonlendirme":
            # İlk aşama: Kullanıcıya yönlendirme göster - hangi sırayla üçgenlerin yakalanacağı
            gosterim_cercevesi = yonlendirme_ucgenleri_ciz(gosterim_cercevesi, ucgenler)

            # 5 saniye sonra geri sayım aşamasına geç
            if gecerli_zaman - yonlendirme_baslangici >= 5.0:
                asama = "geri_sayim"
                geri_sayim_baslangici = gecerli_zaman
                geri_sayim_numara = 3

        elif asama == "geri_sayim":
            # İkinci aşama: Geri sayım göster (3-2-1)
            font_olcegi = 15.0
            kalinlik = 30
            numara = str(geri_sayim_numara)

            # Sayının metin boyutunu al
            (metin_genisligi, metin_yuksekligi), _ = cv.getTextSize(numara, cv.FONT_HERSHEY_SIMPLEX, font_olcegi,
                                                                    kalinlik)

            # Sayıyı ekranın ortasına yerleştir
            metin_x = genislik // 2 - metin_genisligi // 2
            metin_y = yukseklik // 2 + metin_yuksekligi // 2

            # Sayıyı çiz
            cv.putText(gosterim_cercevesi, numara, (metin_x, metin_y), cv.FONT_HERSHEY_SIMPLEX,
                       font_olcegi, (255, 255, 255), kalinlik)

            # Her 1 saniyede bir sayıyı azalt
            if gecerli_zaman - geri_sayim_baslangici >= 1.0:
                geri_sayim_numara -= 1
                geri_sayim_baslangici = gecerli_zaman

                # Geri sayım bitince yakalama aşamasına geç
                if geri_sayim_numara < 1:
                    asama = "yakalama"
                    baslangic_zamani = gecerli_zaman

        elif not all(yakalama_tamamlandi):
            # Üçüncü aşama: Üçgenleri yakalama
            # Önceki donmuş üçgenleri göster
            for i, (dondurulmus_resim, ucgen) in enumerate(dondurulmus_ucgenler):
                maske = ucgen_maske_olustur(gosterim_cercevesi, ucgenler[i])
                gosterim_cercevesi[maske > 0] = dondurulmus_resim[maske > 0]
                if i < gecerli_ucgen:
                    # Tamamlanan üçgenlerin turuncu kenarlıklarını çiz
                    cv.polylines(gosterim_cercevesi, [np.array(ucgenler[i], dtype=np.int32)],
                                 True, (37, 37, 252), 5)

            if asama == "yakalama":
                # Yakalama işlemi - ilerleme çubuğu göster
                gecen_sure = gecerli_zaman - baslangic_zamani
                ilerleme = min(gecen_sure / 3.3, 1.0)

                # İlerleyen turuncu çizgiyi çiz
                ilerleme_kenari_ciz(gosterim_cercevesi, ucgenler[gecerli_ucgen], ilerleme)

                # Yakalama tamamlandı
                if ilerleme >= 1.0:
                    maske = ucgen_maske_olustur(cerceve, ucgenler[gecerli_ucgen])
                    dondurulmus = cerceve.copy()
                    dondurulmus_ucgenler.append((dondurulmus, ucgenler[gecerli_ucgen]))
                    asama = "merkez_goster"
                    merkez_gosterim_baslangici = gecerli_zaman

            elif asama == "merkez_goster":
                # Yakalanan üçgeni ekranın merkezinde göster
                ilerleme = min((gecerli_zaman - merkez_gosterim_baslangici) / 1.0, 1.0)
                # Ortada gösterirken kenarlık olmadan göster
                gosterim_cercevesi = merkezdeki_ucgeni_goster(gosterim_cercevesi, dondurulmus_ucgenler, ilerleme)

                # Gösterimi tamamla ve diğer üçgene geç
                if ilerleme >= 1 and gecerli_zaman - merkez_gosterim_baslangici >= 2.0:
                    asama = "yakalama"
                    yakalama_tamamlandi[gecerli_ucgen] = True
                    gecerli_ucgen += 1
                    baslangic_zamani = gecerli_zaman

        elif not son_asama:
            # Dördüncü aşama: Tüm üçgenler yakalandığında bekleme süresi
            # Tüm üçgenleri donuk halde göster
            for i, (dondurulmus_resim, ucgen) in enumerate(dondurulmus_ucgenler):
                maske = ucgen_maske_olustur(gosterim_cercevesi, ucgenler[i])
                gosterim_cercevesi[maske > 0] = dondurulmus_resim[maske > 0]
                # Turuncu kenarlıkları çiz
                cv.polylines(gosterim_cercevesi, [np.array(ucgenler[i], dtype=np.int32)],
                             True, (37, 37, 252), 5)

            # Son aşamaya geçiş için bekle
            if dalga_baslangici == 0:
                dalga_baslangici = gecerli_zaman

            if gecerli_zaman - dalga_baslangici >= 2:
                son_asama = True

        else:
            # Beşinci aşama: Her üçgene farklı efektler uygula
            # Farklı efektler uygula - her üçgen için ayrı efekt
            for i, (dondurulmus_resim, ucgen) in enumerate(dondurulmus_ucgenler):
                maske = ucgen_maske_olustur(gosterim_cercevesi, ucgenler[i])

                # Her üçgen için farklı bir efekt uygula
                if i == 0:  # Üst üçgen - Karikatür Efekti
                    efekt_resim = karikatur_efekti_uygula(dondurulmus_resim, gecerli_zaman)
                elif i == 1:  # Sağ üçgen - Renk Döngüsü Efekti
                    efekt_resim = renk_dongusu_uygula(dondurulmus_resim, gecerli_zaman + i)
                elif i == 2:  # Sol üçgen - Pikselleştirme Efekti
                    efekt_resim = piksellestirme_uygula(dondurulmus_resim, gecerli_zaman + i)
                elif i == 3:  # Alt üçgen - Glitch Efekti
                    efekt_resim = glitch_efekti_uygula(dondurulmus_resim, gecerli_zaman + i)

                gosterim_cercevesi[maske > 0] = efekt_resim[maske > 0]

                # Turuncu kenarlıkları çiz
                cv.polylines(gosterim_cercevesi, [np.array(ucgenler[i], dtype=np.int32)],
                             True, (37, 37, 252), 5)

        # Sonucu göster
        cv.imshow('TikTok Filtresi', gosterim_cercevesi)

        # 'q' tuşuna basılınca çık
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Temizle
    kamera.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()