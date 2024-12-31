import requests, moviepy
import yt_dlp
import re

def refresh_shorts_url(theme):
    theme_yt = theme.replace(" ", "+")

    response = requests.get(f"https://www.youtube.com/results?search_query=%23shorts+%2B+{theme_yt}")

    if response.status_code == 200:
        html_content = response.text

        shorts_urls = re.findall(r"/shorts/([a-zA-Z0-9_-]{11})", html_content)

        try:
            with open(f"urls-shorts-{theme_yt}.txt", "r", encoding="utf-8") as file:
                existing_urls = file.readlines()
                existing_urls = [url.strip() for url in existing_urls]
        except FileNotFoundError:
            existing_urls = []

        with open(f"urls-shorts-{theme_yt}.txt", "a", encoding="utf-8") as file:
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


def yt_dl(video_url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'VideosDirPath/%(title)s.%(ext)s',
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
    # if not use
    # edit with satisfying video
    video_top = moviepy.VideoFileClip(video1_path)
    video_bottom = moviepy.VideoFileClip(video2_path)

    max_width = max(video_top.w, video_bottom.w)

    video_top = video_top.resized(width=max_width)
    video_bottom = video_bottom.resized(width=max_width)

    total_height = 1920

    video_top = video_top.with_position(("center", -50))
    video_bottom = video_bottom.with_position(("center", video_top.h))

    final_clip = moviepy.CompositeVideoClip([video_top, video_bottom], size=(max_width, total_height))
    final_clip.write_videofile("VideosDirPath/edit.mp4", codec="libx264")
    

if __name__ == "__main__":
    edit_satisfaying("VideosDirPath/The 1 BRAND MECHANIC that NOBODY USES! - League of Legends #shorts.mp4", "SatisfyingVideos/satis3.mp4")