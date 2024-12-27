import os, sys, requests, json, uuid
from .Config import Config
from dotenv import load_dotenv
from tiktok_manager.Browser import Browser
from tiktok_manager.cookies import load_cookies_from_file
from .eprint import eprint
import bot_utils
from requests_auth_aws_sigv4 import AWSSigV4
from fake_useragent import FakeUserAgentError, UserAgent

load_dotenv()

# User Agent par défault
_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

# retourne toujours la valeur du cookie sessionid
def login(login_name: str):
    cookies = load_cookies_from_file(f"tiktok_session-{login_name}")
    session_cookie = next((c for c in cookies if c["name"] == 'sessionid'), None)

    if session_cookie is not None:
        print("Unnecessary login: session already saved!")
        return session_cookie["value"]

    browser = Browser.get()
    browser.driver.get(os.getenv("TIKTOK_LOGIN_URL"))

    session_cookies = []
    while not session_cookies :
        for cookie in browser.driver.get_cookies():
            if cookie["name"] in ["sessionid", "tt-target-idc"]:
                if cookie["name"] == "sessionid":
                    cookie_name = cookie
                session_cookies.append(cookie)

    print("Account successfully saved.")
    browser.save_cookies(f"tiktok_session-{login_name}", session_cookies)
    browser.driver.quit()

    return cookie_name.get('value', '') if cookie_name else ''


# Préparation de la session
def upload_video(session_user, video, title):
    # worth it ?
    try:
        user_agent = UserAgent().random
    except FakeUserAgentError as e:
        user_agent = _UA
        print("[-] Could not get random user agent, using default")

    # Create whole session to request TikTok server
    cookies = load_cookies_from_file(f"tiktok_session-{session_user}")
    session_id = next((c for c in cookies if c["name"] == 'sessionid'), None)
    dc_id = next((c for c in cookies if c["name"] == 'tt-target-idc'), None)
    
    if not session_id:
        eprint("No cookie with Tiktok session id found: use login to save session id")
        sys.exit(1)
    if not dc_id:
        print("[WARNING]: Please login, tiktok datacenter id must be allocated, or may fail")
        dc_id = "useast2a"

    print("User successfully logged in.")
    print(f"Tiktok Datacenter Assigned: {dc_id}")
    print("Uploading video...")
    if len(title) > 2200:
        print("[-] The title has to be less than 2200 characters")
        return False
    
    session = requests.Session()
    session.cookies.set("sessionid", session_id, domain=".tiktok")
    session.cookies.set("tt-target-idc", session_id, domain=".tiktok")
    session.verify = True

    headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
    }
    session.headers.update(headers)


    # create project
    creation_id = bot_utils.generate_random_string(21, True)
    project_url = f"https://www.tiktok.com/api/v1/web/project/create/?creation_id={creation_id}&type=1&aid=1988"
    r = session.post(project_url)

    if bot_utils.assert_success(project_url, r):
        return False

    # get project id
    project_id = r.json()["project"]["project_id"]
    video_id, session_key, upload_id, crcs, upload_host, store_uri, video_auth, aws_auth = upload_to_tiktok(video, session)

    url = f"https://{upload_host}/{store_uri}?uploadID={upload_id}&phase=finish&uploadmode=part"

    headers = {
        "Authorization": video_auth,
        "Content-Type": "text/plain;charset=UTF-8",
    }

    # ApplyUploadInner
    url = f"https://www.tiktok.com/top/v1?Action=CommitUploadInner&Version=2020-11-19&SpaceName=tiktok"
    data = '{"SessionKey":"' + session_key + '","Functions":[{"name":"GetMeta"}]}'

    r = session.post(url, auth=aws_auth, data=data)
    if not bot_utils.assert_success(url, r):
        return False


    # publish video
    url = "https://www.tiktok.com"
    headers = {
     "user-agent": user_agent
    }

    r = session.head(url, headers=headers)
    if not bot_utils.assert_success(url, r):
        return False
    headers = {
     "content-type": "application/json",
     "user-agent": user_agent
    }
    brand = ""
    if brand and brand[-1] == ",":
        brand = brand[:-1]
    markup_text, text_extra = bot_utils.convert_tags(title, session)

    data = {
        "post_common_info": {
            "creation_id": creation_id,
            "enter_post_page_from": 1,
            "post_type": 3,
        },
        "feature_common_info_list": [
            {
                "geofencing_regions": [],
                "playlist_name": "",
                "playlist_id": "",
                "tcm_params": '{"commerce_toggle_info":{}}',
                "sound_exemption": 0,
                "anchors": [],
                "vedit_common_info": {"draft": "", "video_id": video_id},
                "privacy_setting_info": {
                    "visibility_type": 0,
                    "allow_duet": 1,
                    "allow_stitch": 1,
                    "allow_comment": 1,
                },
                "content_check_id": "",
            }
        ],
        "single_post_req_list": [
            {
                "batch_index": 0,
                "video_id": video_id,
                "is_long_video": 0,
                "single_post_feature_info": {
                    "text": title,
                    "text_extra": text_extra,
                    "markup_text": markup_text,
                    "music_info": {},
                    "poster_delay": 0,
                    "cloud_edit_video_height": 2160,
                    "cloud_edit_video_width": 1920,
                    "cloud_edit_is_use_video_canvas": False,
                },
            }
        ],
    }

    # signature and post
    uploaded = False
    while True:
        mstoken = session.cookies.get("msToken")
        js_path = os.path.join(os.getcwd(), "tiktok_manager", "tiktok-signature", "browser.js")
        sig_url = f"https://www.tiktok.com/api/v1/web/project/post/?app_name=tiktok_web&channel=tiktok_web&device_platform=web&aid=1988&msToken={mstoken}"
        # to create signature (_signature & X-Bogus) with js script we need : url project to sign, js script path and user agent
        signatures = bot_utils.subprocess_jsvmp(js_path, user_agent, sig_url)
        if signatures is None:
            print("[-] Failed to generate signatures")
            return False
        
        try:
            tt_output = json.loads(signatures)["data"]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[-] Failed to parse signature data: {str(e)}")
            return False

        project_post_dict = {
            "app_name": "tiktok_web",
            "channel": "tiktok_web",
            "device_platform": "web",
            "aid": 1988,
            "msToken": mstoken,
            "X-Bogus": tt_output["x-bogus"],
            "_signature": tt_output["signature"],
        }

        url = f"https://www.tiktok.com/tiktok/web/project/post/v1/"
        r = session.request("POST", url, params=project_post_dict, data=json.dumps(data), headers=headers)
        
        if not bot_utils.assert_success(url, r):
            print("[-] Published failed, try later again")
            bot_utils.print_error(url, r)
            return False
        
        if r.json()["status_code"] == 0:
            print(f"Published successfully")
            uploaded = True
            break
        else:
            print("[-] Publish failed to Tiktok, trying again...")
            bot_utils.print_error(url, r)
            return False
    
    if not uploaded:
        print("[-] Could not upload video")
        return False

def upload_to_tiktok(video_file, session):
    url = "https://www.tiktok.com/api/v1/video/upload/auth/?aid=1988"
    r = session.get(url)
    if not bot_utils.assert_success(url, r):
        return False
    
    aws_auth = AWSSigV4(
        "vod",
        region="ap-singapore-1",
        aws_access_key_id=r.json()["video_token_v5"]["access_key_id"],
        aws_secret_access_key=r.json()["video_token_v5"]["secret_acess_key"],
        aws_session_token=r.json()["video_token_v5"]["session_token"],
    )

    with open(os.path.join(os.getcwd(), Config.get().videos_dir, video_file), "rb") as f:
        video_content = f.read()
        file_size = len(video_content)
        url = f"https://www.tiktok.com/top/v1?Action=ApplyUploadInner&Version=2020-11-19&SpaceName=tiktok&FileType=video&IsInner=1&FileSize={file_size}&s=g158iqx8434"

    r = session.get(url, auth=aws_auth)
    if not bot_utils.assert_success(url, r):
        return False

    # chunks upload
    upload_node = r.json()["Result"]["InnerUploadAddress"]["UploadNodes"][0]
    video_id = upload_node["Vid"]
    store_uri = upload_node["StoreInfos"][0]["StoreUri"]
    video_auth = upload_node["StoreInfos"][0]["Auth"]
    upload_host = upload_node["UploadHost"]
    session_key = upload_node["SessionKey"]
    chunk_size = 5242880
    chunks = []
    i = 0
    while i < file_size:
        chunks.append(video_content[i: i + chunk_size])
        i += chunk_size
    crcs = []
    upload_id = str(uuid.uuid4())
    for i in range(len(chunks)):
        chunk = chunks[i]
        crc = bot_utils.crc32(chunk)
        crcs.append(crc)
        url = f"https://{upload_host}/{store_uri}?partNumber={i + 1}&uploadID={upload_id}&phase=transfer"
        headers = {
            "Authorization": video_auth,
            "Content-Type": "application/octet-stream",
            "Content-Disposition": 'attachment; filename="undefined"',
            "Content-Crc32": crc,
        }

        r = session.post(url, headers=headers, data=chunk)

    return video_id, session_key, upload_id, crcs, upload_host, store_uri, video_auth, aws_auth

if __name__ == 'main':
    login("test")
    