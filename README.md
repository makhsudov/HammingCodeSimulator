# Hamming SEC-DED Code Simülatörü

Bu proje, Hamming SEC-DED algoritmasını kullanarak hata tespit ve düzeltme simülatörü geliştirmektedir. Bursa Teknik Üniversitesi BLM230 Bilgisayar Mimarisi dersi kapsamında hazırlanmıştır.

## Proje Özellikleri

- 8, 16 ve 32 bitlik veriler üzerinde Hamming SEC-DED kodlama
- Görsel kullanıcı dostu arayüz (Python Tkinter)
- Otomatik parity bit hesaplama
- Yapay hata oluşturma ve test simülasyonu
- Sendrom hesaplama ile hata tespit ve düzeltme
- Renkli bit görselleştirme sistemi

## Kurulum ve Çalıştırma

Projeyi bilgisayarınıza indirmek için:

```bash
git clone https://github.com/makhsudov/HammingCodeSimulator.git
cd HammingCodeSimulator
```

Programı çalıştırmak için:

```bash
cd src
python main.py
```

## Gereksinimler

- Python 3.x
- tkinter (genellikle Python ile birlikte gelir)

## Ekran Görüntüleri

### Ana Arayüz
![Ana Arayüz](docs/image/screenshot1.jpg)

### Başarılı Hata Düzeltme
![Başarılı Hata Düzeltme](docs/image/screenshot2.jpg)

## Dokümantasyon

Proje dokümantasyonu için:
[Proje Dokümantasyonu](docs/BLM230_Proje_EdemMakhsudov_22360859373.pdf)

## Demo Video

Simülatörün nasıl çalıştığını görmek için demo videosunu izleyebilirsiniz:
[YouTube Demo Video](https://youtu.be/DwC2nwy0Hlw)

## Dosya Yapısı

```
src/
├── main.py              # Ana çalıştırma dosyası
├── hamming_simulator.py # GUI ve kullanıcı etkileşimi
├── hamming_logic.py     # Hamming algoritma implementasyonu
└── config.py            # Renk paleti ve stil ayarları
```

## Kullanım

1. Veri boyutunu seçin (8, 16 veya 32 bit)
2. Binary veri girin veya rastgele veri oluşturun
3. "Kodla" butonuna tıklayarak Hamming kodlamasını yapın
4. Hata pozisyonu belirleyerek veya rastgele hata oluşturun
5. "Hata Tespit Et ve Düzelt" butonuyla hata düzeltme işlemini gerçekleştirin

---
