import requests

class AnonyScrape:
    def __init__(self):
        self.session = requests.Session()
        self.session.get("https://anonyig.com")
        self.payload = self.session.cookies.get_dict()

    def get_info(self, username):
        url = f'https://anonyig.com/api/ig/userInfoByUsername/{username}'
        params = {
            'anonyig_session': self.payload['anonyig_session'], 
            'XSRF-TOKEN': self.payload['XSRF-TOKEN']  
        }
        r = self.session.get(url=url, params=params)
        return r.json()

    def get_stories(self, username):
        url = f'https://anonyig.com/api/ig/story?url=https://www.instagram.com/stories/{username}'
        params = {
            'anonyig_session': self.payload['anonyig_session'], 
            'XSRF-TOKEN': self.payload['XSRF-TOKEN']  
        }
        r = self.session.get(url=url, params=params)
        return r.json()