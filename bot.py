"""
  _______  _____  _  __ _______  ____   _  __       ____    ____  _______ 
 |__   __||_   _|| |/ /|__   __|/ __ \ | |/ /      |  _ \  / __ \|__   __|
    | |     | |  | ' /    | |  | |  | || ' /______ | |_) || |  | |  | |   
    | |     | |  |  <     | |  | |  | ||  <|______||  _ < | |  | |  | |   
    | |    _| |_ | . \    | |  | |__| || . \       | |_) || |__| |  | |   
    |_|   |_____||_|\_\   |_|   \____/ |_|\_\      |____/  \____/   |_|       

	@xxbadgame.42student

"""
import os
from tiktok_manager.Config import Config
from tiktok_manager import tiktok

if __name__ == '__main__':
    tiktok.upload_video("legend", os.path.join(os.getcwd(), Config.get().videos_dir, "sqz.mp4"),  "test-my-algo")