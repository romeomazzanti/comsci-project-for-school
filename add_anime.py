# -*- coding: utf-8 -*-
import json
import requests
import traceback
import logging
import unittest
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)
#importing all the modules that are needed
class Add_anime():# this section is part of the "ADDING an anime to a listani"

    def __init__(self, anime = ""):
        self.api_host = "https://api.jikan.moe"
        self.api_version = "v3"
        self.anime_list = []
        self.anime = anime
        self.anime_status_true = "true"
        self.anime_status_false = "false"

    def is_text_valid(self, text: str):
        if text and isinstance(text, str):
            if not text.isspace():
                return True
        return False   #this function will be used later to check if the text/ anime title the user has input is valid

    def call_jikan_api(self, url: str, params = None):
        r = requests.get(url = url, params = params)
        results = r.json()
        logger.debug(results)
        return results #requesting data from the API

    def fetch_anime_id(self):
        logger.info("FETCHING ANIME ID")
        url = f"{self.api_host}/{self.api_version}/search/anime"
        params = {
            "q": self.anime
        }
        results = self.call_jikan_api(url, params)
        anime_id = results["results"][0]["mal_id"]
        logger.debug(f"ANIME ID: {anime_id}")
        return anime_id # getting rid of the useless information by looing for the useful data (in this case the anime id)

    def fetch_episode_status(self, anime_id: str):
        logger.info("FETCHING EPISODE STATUS")
        url = f"{self.api_host}/{self.api_version}/anime/{anime_id}"
        results = self.call_jikan_api(url)
        anime_is_airing = results["airing"]
        logger.debug(f"IS ANIME AIRING: {anime_is_airing}")
        return anime_is_airing # searching for the status of the anime (if it is an airing anime or if it's already finished)

    def fetch_anime_episodes(self, anime_id: str):
        logger.info(f"FETCHING ANIME EPISODES")
        #TODO Support Multiple Pages
        url = f"{self.api_host}/{self.api_version}/anime/{anime_id}/episodes/1"
        results = self.call_jikan_api(url)
        anime_episodes = results["episodes"]
        logger.debug(f"ANIME EPISODES: {anime_episodes}")
        return anime_episodes #searching for every episode of the given anime

    def add_anime_to_list(self): # this function will add anime and its episodes into a list 
        if self.is_text_valid(self.anime):
            anime_id = self.fetch_anime_id()
            anime_is_airing = self.fetch_episode_status(anime_id)
            if anime_is_airing:
                self.anime_status_true = "true" #gives status of the anime
                anime_episodes = self.fetch_anime_episodes(anime_id)
                self.anime_list.append(self.anime)
                self.anime_list.append(anime_episodes)
            else:
                self.anime_status_false = "false" #gives the status of the anime
                self.anime_list.append(self.anime)
                self.anime_list.append(anime_episodes)    
        else:
            return "ANIME INALID, PLEASE TRY AGAIN"   

class Episode_reminder():
    
    def __init__(self,anime_id = ""):
        self.api_host = "https://api.jikan.moe"
        self.api_version = "v3"
        self.anime_list = []
        self.anime_list_airing =[]
        self.anime = anime
    
    def is_text_valid(self, text: str):
        if text and isinstance(text, str):
            if not text.isspace():
                return True
        return False

    def call_jikan_api(self, url: str, params = None):
        r = requests.get(url = url, params = params)
        results = r.json()
        logger.debug(results)
        return results

    def fetch_anime_id(self):
        logger.info("FETCHING ANIME ID")
        url = f"{self.api_host}/{self.api_version}/search/anime"
        params = {
            "q": self.anime
        }
        results = self.call_jikan_api(url, params)
        anime_id = results["results"][0]["mal_id"]
        logger.debug(f"ANIME ID: {anime_id}")
        return anime_id

    def fetch_episode_status(self, anime_id: str):
        logger.info("FETCHING EPISODE STATUS")
        url = f"{self.api_host}/{self.api_version}/anime/{anime_id}"
        results = self.call_jikan_api(url)
        anime_is_airing = results["airing"]
        logger.debug(f"IS ANIME AIRING: {anime_is_airing}")
        return anime_is_airing

    def get_aired_date(self, anime_id: str):
        url = f"{self.api_host}/{self.api_version}/anime{anime_id}"
        results = self.call_jikan_api(url)
        anime_day = results["aired"]["prop"]["from"]["day"]
        anime_month = results["aired"]["prop"]["from"]["month"]
        return anime_day, anime_month
        

    def fetch_anime_episodes(self, anime_id: str):
        logger.info(f"FETCHING TOTAL PAGES")
        url = f"{self.api_host}/{self.api_version}/anime/{anime_id}/episodes"
        results = self.call_jikan_api(url)
        episode_page = results["episodes_last_page"]
        page = str(episode_page)#some anime have more than one page filled with episodes, for this reason it is needed to check for the max number of pages which will then be used to get the last episode aired in the next function
        logger.debug(f"LAST PAGE : {episode_page}")
        anime_episode_number = 0
        anime_episodes = ""
        total_episodes = ""
        if int(page) > 1 :
            url = f"{self.api_host}/{self.api_version}/anime{anime_id}/episodes/{page}"
            while True:
                try:#this try function lets me search through every one of the episodes there ubtil there are no episodes
                    total_episodes = anime["episodes"][anime_episode_number]["episode_id"]
                    anime_episode_number = anime_episode_number + 1
                except Exception:
                    break
            return total_episodes
        anime_episodes = total_episodes
        logger.debug(f"ANIME EPISODES: {anime_episodes}")
        return page, anime_episodes

        

    def add_anime_to_list(self):
        if self.is_text_valid(self.anime):
            anime_id = self.fetch_anime_id()
            anime_is_airing = self.fetch_episode_status(anime_id)
            if anime_is_airing: 
                anime_episodes = self.fetch_anime_episodes(anime_id)
                self.anime_list_airing.append(self.anime)
                self.anime_list_airing.append(anime_episodes)
                return "EPISODES FOUND"
            else:        
                self.anime_list.append(self.anime)
                return "ANIME IS NOT AIRING AT THE MOMENT"
        else:
            return "ANIME INALID, PLEASE TRY AGAIN" 



class Test_case(unittest.TestCase):

    def setUp(self):
       
        pass
        
    def tearDown(self):
        pass

    def test_quick(self):
        pass


if __name__ == "__main__":
    #unittest.main()
    anime = input("PLEASE ENTER THE ANIME YOU WOULD LIEK TO ADD TO A LIST: ")
    list_type = input("WHICH LIST WOULD YOU LIKE TO ADD THAT ANIME TO? ")
    callClass = Episode_reminder(anime)
    animeID = callClass.fetch_anime_id()
    get_da_date = callClass.get_aired_date(animeID)
    print(get_da_date)


    
    

