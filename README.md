# Web Archive URL Scraper ve Arama Aracı

Bu proje, Web Archive üzerinden herhangi bir web sitesinin tüm arşivlenmiş URL'lerini çekmenizi ve bu URL'ler içinde arama yapmanızı sağlar.

## Özellikler

### URL Scraper (`main.py`)
- Herhangi bir web sitesinin Web Archive'daki tüm URL'lerini çeker
- Gerçek zamanlı ilerleme göstergesi
- İndirme hızı ve boyut bilgisi
- Otomatik dosya adlandırma
- Kesintiye uğrama durumunda bile kısmi sonuçları kaydeder

### URL Arama Aracı (`scrape-search.py`)
- İndirilen URL'ler içinde gelişmiş arama yapma
- Farklı arama türleri:
  1. Dosya uzantısı araması (.pdf, .jpg, .html vb.)
  2. Kelime araması (login, admin, download vb.)
  3. Özel kod araması (?id=, /api/, /v1/ vb.)
  4. Özel arama (kullanıcı tanımlı)
- Büyük/küçük harf duyarlılığı seçeneği
- Özelleştirilebilir sonuç dosyası adı
- İlerleme göstergesi ve istatistikler

## Kurulum

1. Python 3.x gereklidir
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

### URL'leri Çekme
1. `main.py` dosyasını çalıştırın:
```bash
python main.py
```
2. İstenen web sitesi adını girin (örn: example.com)
3. Program otomatik olarak URL'leri çekip bir .txt dosyasına kaydedecektir

### URL'lerde Arama Yapma
1. `scrape-search.py` dosyasını çalıştırın:
```bash
python scrape-search.py
```
2. Arama yapmak istediğiniz .txt dosyasını seçin
3. Arama türünü seçin:
   - Dosya uzantısı araması
   - Kelime araması
   - Özel kod araması
   - Özel arama
4. Arama terimini seçin veya girin
5. Sonuç dosyası adını belirleyin
6. Büyük/küçük harf duyarlılığını seçin

## Teknik Detaylar

### Performans Optimizasyonları
- Chunk-based indirme (8192*16 byte chunk boyutu)
- Buffer optimizasyonu
- Streaming veri transferi
- Bellek dostu işleme

### Dosya Formatları
- Çıktı dosyaları: UTF-8 encoding
- Tarih formatı: YYYYMMDD_HHMMSS
- Varsayılan dosya adı formatı: {site_name}_links_{timestamp}.txt

### Hata Yönetimi
- Bağlantı hataları için otomatik raporlama
- KeyboardInterrupt yönetimi
- Kısmi sonuçları koruma
- Dosya işlemleri için güvenli kapanış

## Güvenlik Notları
- Sadece .txt dosyalarında arama yapılabilir
- Dosya işlemleri için güvenli encoding
- Kullanıcı girişi doğrulama
- Hata durumlarında güvenli çıkış

## Sınırlamalar
- Web Archive API limitlerine tabidir
- Büyük dosyalarda RAM kullanımı artabilir
- İnternet bağlantı hızına bağımlıdır

## Katkıda Bulunma
1. Bu depoyu fork edin
2. Yeni bir branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull request oluşturun

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim
Sorunlar ve öneriler için Issues bölümünü kullanabilirsiniz. 