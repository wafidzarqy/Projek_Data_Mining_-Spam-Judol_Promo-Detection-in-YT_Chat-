# import pandas as pd
# import pytchat
# from datetime import datetime

# # Link Video yang mau diambil chat na
# video_id = "TEMPEL_SINI_BEB"

# def main():
#     chats = []
#     chat = pytchat.create(video_id)
    
#     print(f"====== Mengambil live chat dari video: {video_id} ======")
    
#     try:
#         for c in chat.get().sync_items():
#             if len(chats) >= 500:
#                 break
                
#             try:
#                 chats.append({
#                     'datetime': c.datetime,
#                     'label': '',
#                     'author_name': c.author.name if c.author else 'Unknown',
#                     'message': c.message or '',
#                     # 'cleaned_message': '' ====> Mending pke kolom message saja bru di preprocess
#                 })
                
#                 if len(chats) % 50 == 0:
#                     print(f"==== Terkumpul: {len(chats)}/500 ====")
                    
#             except AttributeError:
#                 continue  
                
            
#         if chats:
#             df = pd.DataFrame(chats)
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f'{video_id}_inferences_{timestamp}.csv'
#             df.to_csv(filename, index=False, encoding='utf-8-sig')
#             print(f"Data berhasil disimpan ke {filename}")
#         else:
#             print("===!Tidak ada data yang terkumpul!===")
            
#     except Exception as e:
#         print(f" Error: {e}")
#     finally:
#         chat.terminate()

# if __name__ == "__main__":
#     main()

import pandas as pd
import re
import os
from datetime import datetime
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

# --- KONFIGURASI ---
TIKTOK_USERNAME = "@naurfaa2_" # Ganti dengan username target
OUTPUT_FILE = "infer_live.csv"
TARGET_DATA = 500  # Target jumlah baris data

# Variabel Global
data_list = []
total_saved = 0

def clean_text(text):
    if not text: return ""
    text = text.lower()
    # Menghapus karakter non-alphanumeric agar bersih
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

def save_to_csv():
    global data_list, total_saved
    if not data_list:
        return
        
    df_new = pd.DataFrame(data_list)
    
    # Cek apakah file sudah ada untuk menentukan header
    file_exists = os.path.isfile(OUTPUT_FILE)
    
    # Simpan ke CSV (mode 'a' untuk append)
    df_new.to_csv(OUTPUT_FILE, mode='a', index=False, header=not file_exists)
    
    total_saved += len(data_list)
    print(f">>> Berhasil menyimpan {len(data_list)} baris. Total saat ini: {total_saved}/{TARGET_DATA}")
    
    # Kosongkan list RAM setelah disimpan
    data_list = []

# 1. Inisialisasi Client
client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    global data_list, total_saved
    
    # 2. Ambil Data
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "datetime": now,
        "author_name": event.user.unique_id,
        "message": event.comment,
        # "cleaned_message": clean_text(event.comment),
        "label": "" # Dikosongkan sesuai format infer.csv
    }
    
    data_list.append(row)
    
    # Log ke console agar kita tahu program jalan
    print(f"[{total_saved + len(data_list)}] {event.user.unique_id}: {event.comment}")

    # 3. Cek apakah target 500 sudah tercapai
    if (total_saved + len(data_list)) >= TARGET_DATA:
        print("\nTarget 500 data tercapai! Menyimpan dan menutup koneksi...")
        save_to_csv()
        client.stop() # Berhenti dari Live TikTok

    # Simpan berkala setiap 20 komentar agar aman jika koneksi putus
    elif len(data_list) >= 20:
        save_to_csv()

if __name__ == "__main__":
    try:
        if os.path.isfile(OUTPUT_FILE):
            print(f"File {OUTPUT_FILE} sudah ada. Data baru akan ditambahkan di bawahnya.")
        
        print(f"Menghubungkan ke Live {TIKTOK_USERNAME}...")
        print(f"Target: {TARGET_DATA} komentar.")
        client.run()
        
    except KeyboardInterrupt:
        save_to_csv()
        print("\nProgram dihentikan manual. Data tersimpan.")
    except Exception as e:
        save_to_csv()
        print(f"\nTerjadi kesalahan: {e}")