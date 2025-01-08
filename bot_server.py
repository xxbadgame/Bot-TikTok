
#   _______  _____  _  __ _______  ____   _  __       ____    ____  _______ 
#  |__   __||_   _|| |/ /|__   __|/ __ \ | |/ /      |  _ \  / __ \|__   __|
#     | |     | |  | ' /    | |  | |  | || ' /______ | |_) || |  | |  | |   
#     | |     | |  |  <     | |  | |  | ||  <|______||  _ < | |  | |  | |   
#     | |    _| |_ | . \    | |  | |__| || . \       | |_) || |__| |  | |   
#     |_|   |_____||_|\_\   |_|   \____/ |_|\_\      |____/  \____/   |_|       

# 	@xxbadgame.42student



import os, time, random
from tiktok_uploader.Config import Config
from tiktok_uploader import tiktok
from create_content import *
from datetime import datetime
from utils import *

def create_files_data(theme, username):
    theme_yt = theme.replace(" ", "+")
    directory_path = f"yt_urls/{username}/{theme_yt}/"
    path_urls = f"yt_urls/{username}/{theme_yt}/urls-shorts-{theme_yt}.txt"
    path_used = f"yt_urls/{username}/{theme_yt}/shorts_used.txt"

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"{directory_path} a été crée")
    else:
        print(f"{directory_path} existe déjà")

    if not os.path.exists(path_urls):
        with open(path_urls, "w") as f:
            f.write("")
        print(f"{path_urls} a été créé.")
    else:
        print(f"{path_urls} existe déjà.")

    if not os.path.exists(path_used):
        with open(path_used, "w") as f:
            f.write("")
        print(f"{path_used} a été créé.")
    else:
        print(f"{path_used} existe déjà.")

def edit_and_post_videos(theme, username, satisfying):

    theme_yt = theme.replace(" ", "+")
    publish = False

    with open(f"yt_urls/{username}/{theme_yt}/urls-shorts-{theme_yt}.txt", "r") as f1:
        for l1 in f1:
            if publish == True:
                break
            with open(f"yt_urls/{username}/{theme_yt}/shorts_used.txt", "r") as f2:
                for l2 in f2:
                    if l1.strip() == l2.strip() :
                        print("Url Already use.")
                        break
                else:
                    print("Url not used")
                    print(l1)
                    video_title, _ = yt_dl(l1.strip())
                    video_title = clean_str(video_title); 

                    if satisfying:
                        files = [f for f in os.listdir("SatisfyingVideos") if os.path.isfile(os.path.join("SatisfyingVideos", f))]
                        edit_satisfaying(f"VideosDirPath/now_video.mp4", f"SatisfyingVideos/{random.choice(files)}")
                        video_to_upload = f"content_create.mp4"
                    else:
                        video_to_upload = f"now_video.mp4"

                    
                    tiktok.upload_video(username, os.path.join(os.getcwd(), Config.get().videos_dir, video_to_upload), video_title)


                    with open(f"yt_urls/{username}/{theme_yt}/shorts_used.txt", "a", encoding="utf-8") as f:
                        f.write(l1)
                    publish = True

                    if os.path.exists("VideosDirPath/now_video.mp4"):
                        os.remove("VideosDirPath/now_video.mp4")
                        print(f"VideosDirPath/now_video.mp4 a été supprimer")
                    else:
                        print("VideosDirPath/now_video.mp4 n'existe pas.")
                    
                    break


if __name__ == '__main__':

    tiktok.login("crypto_challenger")

    theme = "crypto"
    username = "crypto_challenger"
    
    create_files_data(theme, username)

    while True:
        publish = False
        time_now = datetime.now().strftime("%H:%M:%S")
        print(f"Time : {time_now}")
        time.sleep(1)

        if time_now == "00:00:00" or time_now == "6:00:00" or time_now == "11:00:00" or time_now == "17:00:00":
            refresh_shorts_url(theme, username)

        if time_now == "07:00:00" or time_now == "12:00:00" or time_now == "18:00:00":
            edit_and_post_videos(theme, username, True)