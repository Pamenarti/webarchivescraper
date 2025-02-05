import requests
import time
from datetime import datetime
from tqdm import tqdm
import os

def fetch_site_links(site):
    url = "https://web.archive.org/cdx/search/cdx?url=*.{}/*&output=txt&fl=original".format(site)
    try:
        print("Web Archive'dan veriler çekiliyor...")
        print("(Bu işlem birkaç dakika sürebilir, lütfen bekleyin...)")
        
        # Dosya adını baştan oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "{}_links_{}.txt".format(site.split('.')[0], timestamp)
        
        # Stream ile indirme yapalım ve direkt dosyaya yazalım
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = 0
            link_count = 0
            last_update = time.time()
            update_interval = 1  # Her 1 saniyede bir güncelle
            
            print("\nVeriler {} dosyasına kaydediliyor...".format(filename))
            
            # Daha büyük buffer boyutu kullanarak dosyaya yazalım
            with open(filename, "wb", buffering=8192*16) as f:
                with tqdm(desc="İndiriliyor ve kaydediliyor", unit='B', unit_scale=True) as pbar:
                    for chunk in response.iter_content(chunk_size=8192*16):  # Daha büyük chunk boyutu
                        if chunk:
                            f.write(chunk)
                            chunk_size = len(chunk)
                            total_size += chunk_size
                            pbar.update(chunk_size)
                            
                            # Yeni link sayısını hesapla
                            new_links = chunk.count(b'\n')
                            link_count += new_links
                            
                            # Her 1 saniyede bir güncelle
                            current_time = time.time()
                            if current_time - last_update >= update_interval:
                                print("\rŞu ana kadar indirilen link sayısı: {:,} | Dosya boyutu: {:.2f} MB".format(
                                    link_count, total_size/1024/1024), end="", flush=True)
                                last_update = current_time
            
            # Son durumu göster
            print("\n\nİşlem tamamlandı!")
            print("Özet:")
            print("- Toplam link sayısı: {:,}".format(link_count))
            print("- Dosya adı: {}".format(filename))
            print("- Dosya boyutu: {:.2f} MB".format(os.path.getsize(filename)/1024/1024))
            
            # İlk 5 linki göster
            print("\nÖrnek linkler (ilk 5):")
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 5:
                        print("- {}".format(line.strip()))
                    else:
                        break
                
        else:
            print("Hata: HTTP {}".format(response.status_code))
    except KeyboardInterrupt:
        print("\n\nİşlem kullanıcı tarafından durduruldu!")
        if 'link_count' in locals():
            print("Şu ana kadar indirilen link sayısı: {:,}".format(link_count))
            if 'filename' in locals():
                print("Veriler {} dosyasına kaydedildi.".format(filename))
                print("Dosya boyutu: {:.2f} MB".format(os.path.getsize(filename)/1024/1024))
    except Exception as e:
        print("Bir hata oluştu: {}".format(str(e)))

if __name__ == "__main__":
    print("Web Archive Link Arama Aracı")
    site = input("Linkleri çekilecek siteyi girin (örn: example.com): ")
    print("\n{} sitesinin linklerini çekme işlemi başlıyor...".format(site))
    start_time = time.time()
    fetch_site_links(site)
    end_time = time.time()
    print("\nToplam geçen süre: {:.2f} saniye".format(end_time - start_time)) 