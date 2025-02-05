import requests
import time
from datetime import datetime
from tqdm import tqdm
import os

def fetch_okx_links():
    url = "https://web.archive.org/cdx/search/cdx?url=*.okx.com/*&output=txt&fl=original"
    try:
        print("Web Archive'dan veriler çekiliyor...")
        print("(Bu işlem birkaç dakika sürebilir, lütfen bekleyin...)")
        
        # Dosya adını baştan oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"okx_links_{timestamp}.txt"
        
        # Stream ile indirme yapalım ve direkt dosyaya yazalım
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = 0
            link_count = 0
            last_update = time.time()
            update_interval = 2  # Her 2 saniyede bir güncelle
            
            print(f"\nVeriler {filename} dosyasına kaydediliyor...")
            
            with open(filename, "w", encoding="utf-8") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192), desc="İndiriliyor ve kaydediliyor"):
                    if chunk:
                        chunk_content = chunk.decode('utf-8')
                        f.write(chunk_content)
                        total_size += len(chunk)
                        
                        # Yeni link sayısını hesapla
                        new_links = chunk_content.count('\n')
                        link_count += new_links
                        
                        # Her 2 saniyede bir güncelle
                        current_time = time.time()
                        if current_time - last_update >= update_interval:
                            print(f"\rŞu ana kadar indirilen link sayısı: {link_count:,} | Dosya boyutu: {total_size/1024/1024:.2f} MB", end="", flush=True)
                            last_update = current_time
            
            # Son durumu göster
            print(f"\n\nİşlem tamamlandı!")
            print(f"Özet:")
            print(f"- Toplam link sayısı: {link_count:,}")
            print(f"- Dosya adı: {filename}")
            print(f"- Dosya boyutu: {os.path.getsize(filename)/1024/1024:.2f} MB")
            
            # İlk 5 linki göster
            print("\nÖrnek linkler (ilk 5):")
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 5:
                        print(f"- {line.strip()}")
                    else:
                        break
                
        else:
            print(f"Hata: HTTP {response.status_code}")
    except KeyboardInterrupt:
        print("\n\nİşlem kullanıcı tarafından durduruldu!")
        if 'link_count' in locals():
            print(f"Şu ana kadar indirilen link sayısı: {link_count:,}")
            if 'filename' in locals():
                print(f"Veriler {filename} dosyasına kaydedildi.")
                print(f"Dosya boyutu: {os.path.getsize(filename)/1024/1024:.2f} MB")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    print("OKX linklerini çekme işlemi başlıyor...")
    start_time = time.time()
    fetch_okx_links()
    end_time = time.time()
    print(f"\nToplam geçen süre: {end_time - start_time:.2f} saniye") 