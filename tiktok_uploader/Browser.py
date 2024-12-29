import undetected_chromedriver as uc
from .cookies import save_cookies_to_file, load_cookies_from_file

# Design Pattern Singleton
class Browser:
    __instance = None

    # Appelle sans instance le get pour vérifier que c'est l'unique appelle du programme
    @staticmethod
    def get():
        if Browser.__instance is None:  
            Browser.__instance = Browser()
        return Browser.__instance
        
    # On vérifie dans le constructeur si le Browser n'est pas crée
    def __init__(self):
        if Browser.__instance is not None:
            raise Exception("This class is a Singleton !")
        else :
            Browser.__instance = self

        # Création du browser avec selenium
        options = uc.ChromeOptions()
        self._driver = uc.Chrome(options=options)
            
    def save_cookies(self, filename: str, cookies:list=None):
        save_cookies_to_file(cookies, filename)

    def load_cookies(self, filename: str):
        cookies = load_cookies_from_file(filename)
        for cookie in cookies:
            self._driver.add_cookie(cookie)
        self._driver.refresh()

    @property
    def driver(self):
        return self._driver

if __name__ == "__main__":
    import os
    print(os.path.dirname(os.path.abspath(__file__)))