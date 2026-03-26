import pandas as pd
import pytchat
from datetime import datetime

# Link Video yang mau diambil chat na
video_id = "TEMPEL_SINI_BEB"

def main():
    chats = []
    chat = pytchat.create(video_id)
    
    print(f"====== Mengambil live chat dari video: {video_id} ======")
    
    try:
        for c in chat.get().sync_items():
            if len(chats) >= 500:
                break
                
            try:
                chats.append({
                    'datetime': c.datetime,
                    'label': '',
                    'author_name': c.author.name if c.author else 'Unknown',
                    'message': c.message or '',
                    # 'cleaned_message': '' ====> Mending pke kolom message saja bru di preprocess
                })
                
                if len(chats) % 50 == 0:
                    print(f"==== Terkumpul: {len(chats)}/500 ====")
                    
            except AttributeError:
                continue  
                
            
        if chats:
            df = pd.DataFrame(chats)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'{video_id}_inferences_{timestamp}.csv'
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Data berhasil disimpan ke {filename}")
        else:
            print("===!Tidak ada data yang terkumpul!===")
            
    except Exception as e:
        print(f" Error: {e}")
    finally:
        chat.terminate()

if __name__ == "__main__":
    main()