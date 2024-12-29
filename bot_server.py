"""
  _______  _____  _  __ _______  ____   _  __       ____    ____  _______ 
 |__   __||_   _|| |/ /|__   __|/ __ \ | |/ /      |  _ \  / __ \|__   __|
    | |     | |  | ' /    | |  | |  | || ' /______ | |_) || |  | |  | |   
    | |     | |  |  <     | |  | |  | ||  <|______||  _ < | |  | |  | |   
    | |    _| |_ | . \    | |  | |__| || . \       | |_) || |__| |  | |   
    |_|   |_____||_|\_\   |_|   \____/ |_|\_\      |____/  \____/   |_|       

	@xxbadgame.42student

"""

import os, time
from tiktok_uploader.Config import Config
from tiktok_uploader import tiktok
from yt_content import *
from datetime import datetime

if __name__ == '__main__':
    
    theme = "league of legends"
    theme_yt = theme.replace(" ", "+")
  
    while True:
        publish = False
        time_now = datetime.now().strftime("%H:%M:%S")
        print(f"Time : {time_now}")
        time.sleep(1)

        if time_now == "00:00:00" or time_now == "6:00:00" or time_now == "12:00:00" or time_now == "18:00:00":
            refresh_shorts_url(theme)

        if time_now == "07:00:00" or time_now == "12:00:00" or time_now == "18:00:00":
            with open(f"yt_urls/urls-shorts-{theme_yt}.txt", "r") as f1:
                for l1 in f1:
                    if publish == True:
                        break
                    with open("yt_urls/shorts_used.txt", "r") as f2:
                        for l2 in f2:
                            if l1.strip() == l2.strip() :
                                print("Url Already use.")
                                break
                        else:
                            print("Url not used")
                            print(l1)
                            video_title, video_ext = yt_dl(l1.strip())
                            upload_name = f"{video_title}.{video_ext}"
                            tiktok.upload_video("legend", os.path.join(os.getcwd(), Config.get().videos_dir, upload_name), video_title)
                            with open("yt_urls/shorts_used.txt", "a", encoding="utf-8") as f:
                                f.write(l1)
                            publish = True
                            break