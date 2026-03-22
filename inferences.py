import pandas as pd # not yet being used dumbass (belum kepake)
import pytchat
import json

# https://www.youtube.com/watch?v=AUE5iHINUIw
"""
    Marapthon live
"""
video_id = "AUE5iHINUIw"
def main():
    chats = []
    chat = pytchat.create(video_id)

    try:
        while chat.is_alive():
            for c in chat.get().sync_items():
                livechat_obj = c.json()
                live_chat = json.loads(livechat_obj)
                
                print(live_chat['datetime'] + " : " + live_chat['author']['name'] + " : " + live_chat['message'])

                # Custom Structures
                chats.append({
                    'datetime' : c.datetime,
                    'label' : '',
                    'author_name' : c.author.name,
                    'message' : c.message,
                    'cleaned_message' : ''
                })

                 # Stop collecting once we hit 500 rows
                if len(chats) >= 500:
                    break
            
            if len(chats) >= 500:
                break

        # Membuat Dataframe pandas
        df = pd.DataFrame(chats)

        # Convert to csv
        df.to_csv(f'/Dataset_infer/{video_id}_inferences.csv', index=False)
        print("Data disimpan ke dir Dataset_infer")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    print(f"Youtube Inferences dimulai")
    print("===========Harap tunggu sampai selesai===========")
    main()
    exit()

# Maumi bree
# Iyakah :)
