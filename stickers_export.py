import os
import sys
import time
import requests

# pip install requests

# 请在这里替换成你的 Telegram Bot Token
TOKEN = "6793176592:AAFDkzeSYxOuW7HS8mZkMP9EmfKUo9wGesQ"

def download_sticker_set(sticker_set_name):
    base_url = "https://api.telegram.org/bot" + TOKEN
    sticker_set_dir = os.path.join(os.getcwd(), sticker_set_name)
    os.makedirs(sticker_set_dir, exist_ok=True)

    # 获取 sticker set 信息
    response = requests.get(f"{base_url}/getStickerSet", params={"name": sticker_set_name})
    sticker_set = response.json()["result"]["stickers"]

    for sticker in sticker_set:
        file_id = sticker["file_id"]
        emoji = sticker.get("emoji", file_id)
        print(f"获取文件路径 for {file_id}...")

        # 获取文件路径
        file_path_response = requests.get(f"{base_url}/getFile", params={"file_id": file_id})
        file_path = file_path_response.json()["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        print(f"download_url => {download_url}")

        # 下载文件
        response = requests.get(download_url)
        original_file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(original_file_name)[1]

        new_file_name = emoji + file_extension
        new_file_path = os.path.join(sticker_set_dir, new_file_name)

        with open(new_file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"下载并重命名完成: {new_file_name}")
        time.sleep(0.2)  # 为了避免过于频繁的请求

    print(f"Sticker pack 保存在 {sticker_set_dir}.")

if __name__ == "__main__":
    sticker_set_name = "HotCherry"

    if len(sys.argv) == 2:
        sticker_set_name = sys.argv[1]
    
    download_sticker_set(sticker_set_name)
