class Config:

    _DEFAULT_OPTIONS = {
        "COOKIES_DIR": "./CookiesDir",
        "VIDEOS_DIR": "./VideosDirPath",
        "LANG": "fr",
    } 

    _instance = None

    @staticmethod
    def get():
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance

    def __init__(self, path=None) -> None:
        if not Config._instance:
            Config._instance = self
            if not path :
                self._options = Config._DEFAULT_OPTIONS
                self.path = None
            else:
                self.path = path
                self._options = {}

    def get_option_by_name(self, opt_name: str):
        return self._options.get(opt_name)

    @property
    def cookies_dir(self):
        return self.get_option_by_name("COOKIES_DIR")

                