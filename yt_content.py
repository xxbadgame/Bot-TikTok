import requests
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
        'format': 'best',
        'outtmpl': 'VideosDirPath/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', 'Titre non disponible')
            video_ext = info.get('ext', 'Extension non disponible')
            print("Téléchargement terminé !")
            return video_title, video_ext
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None

if __name__ == "__main__":
    refresh_shorts_url("league of legends")
