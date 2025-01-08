import requests, moviepy
import yt_dlp
import re
from utils import *

def refresh_shorts_url(theme, username):
    theme_yt = theme.replace(" ", "+")

    response = requests.get(f"https://www.youtube.com/results?search_query=%23shorts+%2B+{theme_yt}")

    if response.status_code == 200:
        html_content = response.text

        shorts_urls = re.findall(r"/shorts/([a-zA-Z0-9_-]{11})", html_content)

        try:
            with open(f"yt_urls/{username}/{theme_yt}/urls-shorts-{theme_yt}.txt", "r", encoding="utf-8") as file:
                existing_urls = file.readlines()
                existing_urls = [url.strip() for url in existing_urls]
        except FileNotFoundError:
            existing_urls = []

        with open(f"yt_urls/{username}/{theme_yt}/urls-shorts-{theme_yt}.txt", "a", encoding="utf-8") as file:
            for video_id in shorts_urls:
                complete_url = f"https://youtube.com/shorts/{video_id}"

                if complete_url not in existing_urls:
                    file.write(complete_url + "\n")
                    print(f"Ajouté : {complete_url}")
                    existing_urls.append(complete_url)
                else:
                    print(f"URL déjà présente : {complete_url}")
    else:
        print(f"Erreur lors de la récupération de la page, code : {response.status_code}")

def clean_title(title):
    return clean_str(title)

def yt_dl(video_url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f"VideosDirPath/now_video.mp4",
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', 'Titre non disponible')
            video_ext = info.get('ext', 'Extension non disponible')
            print("Download mp4 !")
            return video_title, video_ext
    except Exception as e:
        print(f"Error : {e}")
        return None
    
def edit_satisfaying(video1_path, video2_path):
    clip1 = moviepy.VideoFileClip(video1_path)
    clip2 = moviepy.VideoFileClip(video2_path)

    min_duration = min(clip1.duration, clip2.duration)

    clip1 = clip1.subclipped(0, min_duration)
    clip2 = clip2.subclipped(0, min_duration)
    
    clip1 = clip1.resized(new_size=(540,1200))
    clip2 = clip2.resized(new_size=(540,1200))

    final_clip = moviepy.clips_array([[clip1, clip2]])
    final_clip.write_videofile("VideosDirPath/content_create.mp4", codec="libx264")
    

if __name__ == "__main__":
    pass