import requests
import json

class InstagramAPI:
    def __init__(self, username, ts=None, _ts=None, _s=None):
        self.base_url = "https://gramsnap.com/api"
        self.username = username
        self.ts = ts
        self._ts = _ts
        self._s = _s

    def user_info(self, username):
        url = f"{self.base_url}/ig/userInfoByUsername/{username}"
        response = requests.get(url).json()
        user = response['result']['user']
        username_ig = user['username']
        full_name = user['full_name']
        is_private = str(user['is_private'])
        biography = user['biography']
        hd_profile_pic = user['hd_profile_pic_url_info']['url']
        pk = user['pk']
        return username_ig, full_name, is_private, biography, hd_profile_pic, pk

    def retrieve_posts(self):
        url = "https://gramsnap.com/api/convert"
        payload = {
            "url": f"https://www.instagram.com/{self.username}/",
            "ts": self.ts,
            "_ts": self._ts,
            "_tsc": 0,
            "_s": self._s
        }

        r = requests.post(url, params=payload)
        response = r.text
        data = json.loads(response)

        if 'error' in data:
            error_code = data['error_code']
            error_message = data['error_message']
            return f"Error: {error_code} - {error_message}"

        urls = [item['url'][0]['url'] for item in data]
        thumbnails = [item['thumb'] for item in data]
        titles = [item['meta']['title'] for item in data]
        return urls, thumbnails, titles

    def get_stories(self, username):
      url = f"{self.base_url}/ig/story?url=https://www.instagram.com/stories/{username}"
      response = requests.get(url).json()
      if response.get('result'):
          video_links = []
          timestamp = response['result'][0]['taken_at']
          for result in response['result']:
              video_versions = result.get('video_versions')
              if video_versions:
                  video_link = video_versions[0].get('url')
                  if video_link:
                      video_links.append(video_link)
          return video_links, timestamp
      else:
          return "It seems that there are no stories for the last 24 hours. Please try again later."


    def get_all_highlights(self, username):
        pk = self.user_info(username)[5]
        url = f"{self.base_url}/ig/highlights/{pk}"
        response = requests.get(url).json()
        highlights = []
        if 'result' in response and isinstance(response['result'], list):
            for result in response['result']:
                id = result['id']
                title = result['title']
                thumbnail = result['cover_media']['cropped_image_version']['url']
                highlights.append({'id': id, 'title': title, 'thumbnail': thumbnail})
        return highlights

    def get_highlights(self, username, selector):
        highlights = self.get_all_highlights(username)
        id = highlights[int(selector)]['id']
        url = f'https://gramsnap.com/api/ig/highlightStories/{id}'
        response = requests.get(url).json()
        if response.get('result'):
          video_links = []
          timestamp = response['result'][0]['taken_at']
          for result in response['result']:
              video_versions = result.get('video_versions')
              if video_versions:
                  video_link = video_versions[0].get('url')
                  if video_link:
                      video_links.append(video_link)
        return video_link