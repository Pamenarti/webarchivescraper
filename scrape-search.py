import os
from datetime import datetime
import re
from tqdm import tqdm

def search_in_links(input_file, search_term, output_filename, case_sensitive=False):
    try:
        if not os.path.exists(input_file):
            print("Hata: {} dosyası bulunamadı!".format(input_file))
            return
            
        if not input_file.endswith('.txt'):
            print("Hata: Sadece .txt uzantılı dosyalarda arama yapılabilir!")
            return
        
        # Çıktı dosyası adını oluştur
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = "search_results_{}.txt".format(timestamp)
        else:
            # Eğer kullanıcı .txt uzantısı eklemediyse otomatik ekle
            output_file = output_filename if output_filename.endswith('.txt') else output_filename + '.txt'
        
        print("\nArama başlıyor...")
        print("Aranan terim: {}".format(search_term))
        print("Büyük/küçük harf duyarlı: {}\n".format("Evet" if case_sensitive else "Hayır"))
        
        # Dosya boyutunu al
        total_size = os.path.getsize(input_file)
        
        found_count = 0
        processed_lines = 0
        
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            # Başlık bilgisini yaz
            outfile.write("Arama Sonuçları\n")
            outfile.write("=" * 50 + "\n")
            outfile.write("Aranan terim: {}\n".format(search_term))
            outfile.write("Kaynak dosya: {}\n".format(input_file))
            outfile.write("Tarih: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            outfile.write("=" * 50 + "\n\n")
            
            # Progress bar ile dosyayı oku
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Aranıyor") as pbar:
                for line in infile:
                    processed_lines += 1
                    
                    # Arama terimini kontrol et
                    if case_sensitive:
                        if search_term in line:
                            outfile.write(line)
                            found_count += 1
                    else:
                        if search_term.lower() in line.lower():
                            outfile.write(line)
                            found_count += 1
                    
                    pbar.update(len(line.encode('utf-8')))
        
        # Sonuçları göster
        print("\nArama tamamlandı!")
        print("\nÖzet:")
        print("- Taranan satır sayısı: {:,}".format(processed_lines))
        print("- Bulunan sonuç sayısı: {:,}".format(found_count))
        print("- Sonuçlar {} dosyasına kaydedildi".format(output_file))
        
        # İlk 5 sonucu göster
        if found_count > 0:
            print("\nÖrnek sonuçlar (ilk 5):")
            with open(output_file, 'r', encoding='utf-8') as f:
                # Başlık kısmını atla
                for _ in range(6):
                    next(f)
                # İlk 5 sonucu göster
                for i, line in enumerate(f):
                    if i < 5:
                        print("- {}".format(line.strip()))
                    else:
                        break
        
    except Exception as e:
        print("Bir hata oluştu: {}".format(str(e)))

def get_search_type():
    while True:
        print("\nArama türünü seçin:")
        print("1. Dosya uzantısı araması (.pdf, .jpg, .html vb.)")
        print("2. Kelime araması (login, admin, download vb.)")
        print("3. Özel kod araması (?id=, /api/, /v1/ vb.)")
        print("4. Özel arama (kendi teriminizi girin)")
        
        try:
            choice = int(input("\nSeçiminiz (1-4): "))
            if choice < 1 or choice > 4:
                print("Lütfen 1-4 arasında bir sayı girin!")
                continue
            
            if choice == 1:
                print("\nYaygın dosya uzantıları:")
                extensions = [".pdf", ".jpg", ".jpeg", ".png", ".gif", ".html", ".php", ".asp", ".js", ".css"]
                for i, ext in enumerate(extensions, 1):
                    print("{}. {}".format(i, ext))
                print("11. Diğer (kendi girin)")
                
                ext_choice = int(input("\nUzantı seçin (1-11): "))
                if ext_choice == 11:
                    return input("Aramak istediğiniz uzantıyı girin (örn: .xml): ")
                elif 1 <= ext_choice <= len(extensions):
                    return extensions[ext_choice-1]
                
            elif choice == 2:
                print("\nYaygın arama kelimeleri:")
                keywords = ["login", "admin", "download", "upload", "user", "password", "config", "backup", "api", "test"]
                for i, keyword in enumerate(keywords, 1):
                    print("{}. {}".format(i, keyword))
                print("11. Diğer (kendi girin)")
                
                keyword_choice = int(input("\nKelime seçin (1-11): "))
                if keyword_choice == 11:
                    return input("Aramak istediğiniz kelimeyi girin: ")
                elif 1 <= keyword_choice <= len(keywords):
                    return keywords[keyword_choice-1]
                
            elif choice == 3:
                print("\nYaygın kod örnekleri:")
                codes = ["?id=", "/api/", "/v1/", "/admin/", "?page=", "?file=", "/upload/", "/download/", "/config/", "/backup/"]
                for i, code in enumerate(codes, 1):
                    print("{}. {}".format(i, code))
                print("11. Diğer (kendi girin)")
                
                code_choice = int(input("\nKod seçin (1-11): "))
                if code_choice == 11:
                    return input("Aramak istediğiniz kodu girin: ")
                elif 1 <= code_choice <= len(codes):
                    return codes[code_choice-1]
                
            else:  # choice == 4
                return input("\nAramak istediğiniz terimi girin: ")
                
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı girin.")
        except Exception as e:
            print("Bir hata oluştu: {}".format(str(e)))

def main():
    print("Web Archive Link Arama Aracı")
    print("=" * 30)
    
    # Mevcut link dosyalarını listele (sadece .txt dosyaları)
    link_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    if not link_files:
        print("\nHata: Hiç .txt dosyası bulunamadı!")
        print("Önce main.py ile link dosyası oluşturun.")
        return
    
    print("\nMevcut .txt dosyaları:")
    for i, file in enumerate(link_files, 1):
        print("{}. {}".format(i, file))
    
    try:
        file_index = int(input("\nHangi dosyada arama yapmak istiyorsunuz? (1-{}): ".format(len(link_files)))) - 1
        if file_index < 0 or file_index >= len(link_files):
            print("Geçersiz dosya numarası!")
            return
        
        search_term = get_search_type()
        if not search_term:
            print("Arama terimi boş olamaz!")
            return
            
        # Kullanıcıdan çıktı dosyası adını iste
        print("\nSonuçların kaydedileceği dosya adını belirleyin:")
        print("1. Otomatik oluştur (search_results_[tarih].txt)")
        print("2. Kendim belirleyeceğim")
        filename_choice = input("\nSeçiminiz (1-2): ")
        
        output_filename = ""
        if filename_choice == "2":
            output_filename = input("Dosya adını girin (örn: sonuclar.txt): ")
        
        case_sensitive = input("\nBüyük/küçük harf duyarlı arama yapılsın mı? (e/h): ").lower() == 'e'
        
        search_in_links(link_files[file_index], search_term, output_filename, case_sensitive)
        
    except ValueError:
        print("Geçersiz giriş!")
    except KeyboardInterrupt:
        print("\n\nİşlem kullanıcı tarafından durduruldu!")

if __name__ == "__main__":
    main() 