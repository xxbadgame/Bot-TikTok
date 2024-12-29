import os
import pickle
from .Config import Config

def save_cookies_to_file(cookies, filename: str, cookies_path=None):
    if not cookies_path:
        cookies_path = os.path.join(os.getcwd(), Config.get().cookies_dir, filename + ".cookie")
    else:
        cookies_path = os.path.join(cookies_path, filename + '.cookies')
    print("Saving cookies to file:", cookies_path)
    with open(cookies_path, "wb") as f:
        pickle.dump(cookies, f)
        f.close()

def load_cookies_from_file(filename, cookies_path=None):
    if not cookies_path:
        cookies_path = os.path.join(os.getcwd(), Config.get().cookies_dir, filename + ".cookie")
    else:
        cookies_path = os.path.join(cookies_path, filename + '.cookies')
    if not os.path.exists(cookies_path):
        print("user not found on system.")
        return []
    
    cookie_data = pickle.load(open(cookies_path, "rb"))
    cookies = []
    for cookie in cookie_data:
        cookies.append(cookie)
    return cookies

def delete_cookies_file(filename: str, cookies_path=None):
    if not cookies_path:
        cookies_path = os.path.join(os.getcwd(), Config.get().cookies_dir, filename + ".cookie")
    else:
        cookies_path = os.path.join(cookies_path, filename + '.cookies')
    
    if os.path.exists(cookies_path):
        os.remove(cookies_path)
        print("Deleted cookies file: ", cookies_path)
    else:
        print("No cookies file to delete: ", cookies_path)

def delete_all_cookies_files(cookies_path=None):
    if not cookies_path:
        cookie_dir = os.path.join(os.getcwd(), Config.get().cookies_dir)
    else:
        cookie_dir = cookies_path
    
    for filename in os.listdir(cookie_dir):
        if filename.endswith(".cookie"):
            os.remove(os.path.join(cookie_dir, filename))
            print("Deleted cookies file: ", filename)
    print("Deleted all cookies file. ")