# TikTok-Tarzı Filtre Uygulaması

Bu proje, Python ve OpenCV kullanarak gerçek zamanlı video akışında dört farklı TikTok stili filtreyi (Karikatür, Renk Döngüsü, Pikselleştirme ve Glitch) ekranı dört üçgen bölgeye ayırarak sırayla uygular. Kullanıcı her bir üçgeni yakalar, merkezde kısa bir önizleme sonrası son aşamada her üçgen bölgesine ayrı bir efekt işler. `q` tuşuna basıldığında uygulama sonlanır.

---

## 📌 İçindekiler

1. [Genel Bakış](#genel-bakış)  
2. [Özellikler](#özellikler)  
3. [Gereksinimler](#gereksinimler)  
4. [Kurulum](#kurulum)  
5. [Kullanım](#kullanım)  
6. [Proje Yapısı](#proje-yapısı)  
7. [Fonksiyon Açıklamaları](#fonksiyon-açıklamaları)  
8. [Yeni Filtre Ekleme](#yeni-filtre-ekleme)  

---

## 🔍 1. Genel Bakış

Bu uygulama, web kamerasından alınan gerçek zamanlı görüntü üzerinde aşağıdaki aşamaları gerçekleştirir:

1. **Yönlendirme (5 saniye)**  
   - Ekran dört büyük üçgene bölünür ve her üçgenin içine sırasıyla 1’den 4’e kadar numaralar eklenerek kullanıcı hangi sırayla çekim yapacağını görür.

2. **Geri Sayım (3-2-1)**  
   - 5 saniyelik yönlendirme sonrası ekranda “3-2-1” geri sayımı görüntülenir.

3. **Üçgen Yakalama (Her biri 3.3 saniye)**  
   - Her üçgen, turuncu kenarlıkta ilerleyen bir çizgiyle yakalanır. İlerleme çubuğu tamamlandığında o bölge “dondurulur” (sabitlenir).  
   - Dondurulan üçgen, orijinal video akışından koparılıp hafızaya alınır.

4. **Merkezde Önizleme (1 saniye)**  
   - Yakalanan üçgen, ekranın ortasında zoom animasyonuyla gösterilir ve beyaz kenarlık eklenir.

5. **Son Aşama – Filtre Uygulama**  
   - Tüm dört üçgen yakalandıktan ve 2 saniyelik bekleme tamamlandıktan sonra, dört bölgeye sırayla şu filtreler uygulanır:  
     1. **Üst Üçgen → Karikatür (Cartoon) Efekti**  
     2. **Sağ Üçgen → Renk Döngüsü (Color Cycling) Efekti**  
     3. **Sol Üçgen → Pikselleştirme (Pixelate) Efekti**  
     4. **Alt Üçgen → Glitch (Dijital Bozulma) Efekti**

6. **Çıkış**  
   - Kullanıcı `q` tuşuna bastığında video akışı durdurulur ve tüm pencereler kapatılarak uygulama sonlanır.

---

## ✨ 2. Özellikler

- **Gerçek Zamanlı Video İşleme**: Web kamerasından alınan canlı görüntü üzerinde filtre uygulama.  
- **Üçgen Bölgelere Göre Yakalama**: Ekranı “üst”, “sağ”, “sol” ve “alt” üçgenlere bölerek her bölgeyi ayrı ayrı yakalama.  
- **Merkezde Zoom Önizleme**: Yakalanan her üçgen, ekranın ortasında büyüyerek kısa bir süre (1 saniye) gösterilir.  
- **Dört Farklı Filtre**:  
  1. **Karikatür (Cartoon) Efekti**  
  2. **Renk Döngüsü (Color Cycling) Efekti**  
  3. **Pikselleştirme (Pixelate) Efekti**  
  4. **Glitch (Dijital Bozulma) Efekti**  
- **Animasyonlu İlerleme Çizgisi**: Her üçgen yakalama aşamasında turuncu kenarlarda dolanarak ilerleyen bir çizgi animasyonu.  
- **Kolay Çıkış**: `q` tuşu ile uygulamayı anında durdurma.

---

## 🛠 3. Gereksinimler

- Python 3.6 veya üzeri  
- OpenCV (cv2)  
- NumPy

### Gerekli Python Paketleri

```bash
pip install opencv-python numpy
```

---

## 🚀 4. Kurulum

1. **Projeyi Klonlayın**  
   ```bash
   git clone https://github.com/kullanici-adi/tiktok-filter-image-processing.git
   cd tiktok-filter-image-processing
   ```

2. **Python Sanal Ortam Oluşturun (Tercihli)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   venv\Scripts\activate.bat    # Windows
   ```

3. **Gerekli Paketleri Yükleyin**  
   ```bash
   pip install -r requirements.txt
   ```
   > `requirements.txt` içeriği:  
   > ```
   > opencv-python
   > numpy
   > ```

---

## 🎬 5. Kullanım

Terminal/komut satırından projenin kök dizininde aşağıdaki komutu çalıştırarak uygulamayı başlatın:

```bash
python main.py
```

- Uygulama açıldığında ekran dört üçgene bölünecek ve numaralandırma gösterilecektir.  
- Ardından “3-2-1” geri sayımı başlayıp her üçgen sırasıyla 3.3 saniye boyunca “dondurulacak”.  
- Dördüncü üçgen de yakalandıktan sonra her bölgeye sırasıyla Karikatür, Renk Döngüsü, Pikselleştirme ve Glitch filtreleri uygulanacaktır.  
- Çıkmak için pencere aktifken `q` tuşuna basmanız yeterlidir.

---

## 📁 6. Proje Yapısı

```
tiktok-filter-image-processing/
│
├── main.py                    # Uygulama giriş noktası ve ana akış
├── requirements.txt           # Projede kullanılan Python paketleri
├── filters/                   # Ek filtre modülleri ekleyebileceğiniz klasör (opsiyonel)
│   ├── yok                    # Yeni filtre script’leri ekleyebilirsiniz
│   └── ...
└── README.md                  # Proje dokümantasyonu (bu dosya)
```

- **main.py**:  
  - Web kamerasını başlatır, ekranı dört üçgene böler, aşamaları (yönlendirme, geri sayım, yakalama, merkezde gösterim, filtre uygulama) kontrol eder.  
  - `cv.imshow('TikTok Filtresi', gosterim_cercevesi)` ile sonuçları ekrana yansıtır.  
  - `q` tuşu ile çıkılır (`cv.waitKey(1) & 0xFF == ord('q')`).

- **filters/**:  
  - İleride projeye eklemek istediğiniz yeni efekt/modülleri bu klasöre yerleştirebilirsiniz.

---

## 📝 7. Fonksiyon Açıklamaları

Aşağıda `main.py` içindeki başlıca fonksiyonların kısa açıklamaları yer almaktadır:

1. **`ucgen_maske_olustur(cerceve, noktalar)`**  
   Belirlenen 3 nokta koordinatına göre ikili maske (binary mask) oluşturur. Üçgen bölgesini beyaz (255), geri kalanını siyah (0) yapar.  
   - `cerceve`: Girdi görüntüsü (frame)  
   - `noktalar`: Üçgenin köşe koordinat listesi ([(x1,y1), (x2,y2), (x3,y3)])

2. **`merkezdeki_ucgeni_goster(cerceve, ucgenler_verisi, ilerleme)`**  
   Yakalanmış üçgen görüntülerini ekranın ortasında gösterir ve beyaz kenarlık çizer.  
   - `ucgenler_verisi`: Daha önce dondurulmuş görüntüler ve üçgen noktaları içeren liste  
   - `ilerleme`: 0.0–1.0 arasında bir değer; zoom-in animasyonunu kontrol eder

3. **`karikatur_efekti_uygula(resim, zaman_degeri)`**  
   Girdi görüntüsüne “medyan blur + adaptif threshold + bilateral filter” kombinasyonu uygulayarak çizgi film/karikatür görüntüsü oluşturur.  
   - `resim`: Üçgen bölgesinin dondurulmuş orijinal hali  
   - `zaman_degeri`: Animasyon veya zaman parametresi (kenar detaylarının dinamik olması için kullanılabilir)

4. **`renk_dongusu_uygula(resim, zaman_degeri)`**  
   HSV renk uzayında Hue değerini zamanla kaydırarak renk döngüsü efekti oluşturur.  
   - HSV’ye çevirir, Hue kanalı `np.mod(h + int(zaman_degeri * 10) % 180, 180)` ile kaydırılır.

5. **`piksellestirme_uygula(resim, zaman_degeri)`**  
   Sinüs fonksiyonuyla kontrol edilen blok boyutu kadar görüntüyü önce küçültür, sonra tekrar büyüterek pikselleştirme efekti verir.  
   - `blok_boyutu = max(2, 15 + int(10 * sin(zaman_degeri)))`

6. **`glitch_efekti_uygula(resim, zaman_degeri)`**  
   Rastgele yatay bant kaydırmalarıyla dijital bozulma efekti (glitch) uygular.  
   - 10 rastgele bant seçilir, her birine rastgele sağa/sola kaydırma uygulanır.

7. **`ilerleme_kenari_ciz(cerceve, noktalar, ilerleme, renk=(37,37,252))`**  
   Belirlenmiş üçgen köşeleri boyunca, ilerlemeye göre (0.0–1.0 arası) kenar çizgisi oluşturur.  
   - Her bir kenar uzunluğu hesaplanır ve toplam uzunluğa göre hangi kısma çizgi çizileceği belirlenir.  
   - `renk=(37,37,252)`: Turuncumsu mavi ton.

8. **`yonlendirme_ucgenleri_ciz(cerceve, ucgenler)`**  
   Ekrandaki dört üçgeni yarı saydam siyah arka planla gölgelendirir, kenarlarını beyaz çizer ve her üçgenin ortasına 1–4 arası numaralar ekler.  
   - Kullanıcıya hangi üçgene hangi sırayla bakacağını gösterir (5 saniyelik aşama).

9. **`main()`**  
   - Video akışını başlatır, pencereyi 1920×1080 olarak ayarlar.  
   - Aşamaları kontrollü şekilde uygular:  
     1. **yonlendirme** → Triangülasyonun ekranda gösterimi (5 sn).  
     2. **geri_sayim** → “3-2-1” geri sayımı.  
     3. **yakalama / merkez_goster** → Her üçgeni yakalama (3.3 sn ilerleme animasyonu) ve merkezde zoom animasyonu (1 sn).  
     4. **son_asama** → Tüm üçgenler sabitlendikten sonra 2 sn bekleme.  
     5. **Efekt Uygulama** → Her üçgene Karikatür, Renk Döngüsü, Pikselleştirme, Glitch filtreleri.  
   - `while True:` döngüsü içinde her frame işlenir ve `cv.imshow('TikTok Filtresi', gosterim_cercevesi)` ile yansıtılır.  
   - `q` tuşu ile döngüden çıkılır, kamera ve pencereler kapatılarak kaynaklar serbest bırakılır.

---

## 💡 8. Yeni Filtre Ekleme

1. `filters/` klasörüne yeni bir Python dosyası ekleyin (örneğin `sepia.py`).
2. Yeni dosyanın içinde aşağıdaki şablona benzer bir fonksiyon tanımlayın:
   ```python
   import cv2 as cv
   import numpy as np

   def sepia_efekti_uygula(resim, zaman_degeri):
       kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
       sepia = cv.transform(resim, kernel)
       sepia = np.clip(sepia, 0, 255).astype(np.uint8)
       return sepia
   ```
3. `main.py` içinde, filtre uygulama aşamasında yeni efekti uygun indekste çalıştıracak şekilde kod ekleyin:
   ```python
   elif i == 4:  # Beşinci bölge veya isteğe bağlı yeni sıra
       efekt_resim = sepia_efekti_uygula(dondurulmus_resim, gecerli_zaman + i)
   ```
4. `README.md` ve/veya `filter_registry.py` dosyalarında yeni filtre hakkında bilgi ekleyin.

