import cloudscraper
from bs4 import BeautifulSoup
import json
class PicukiScraper:
    def __init__(self, delay=10, browser="chrome"):
        self.scraper = cloudscraper.create_scraper(delay=delay, browser=browser)

    def get_posts_info(self, username):
        page = self.scraper.get(f"https://www.picuki.com/profile/{username}")
        soup = BeautifulSoup(page.content, "html.parser")
        posts = soup.find_all("div", class_="photo")
        data = []
        for post in posts:
            link = post.find("a")
            post_link = link["href"]
            img = link.find("img")
            title = img["alt"]
            thumbnail = img["src"]
            post_data = {
                "post_link": post_link,
                "title": title,
                "thumbnail": thumbnail
            }
            data.append(post_data)
        return json.dumps(data)

    def get_post(self, post_link):
        page = self.scraper.get(post_link)
        soup = BeautifulSoup(page.content, "html.parser")
        posts = soup.find_all("div", class_="item")
        data = []
        for post in posts:
            img = post.find("img")
            src = img["src"]
            post_data = {
              "image": src
            }
            data.append(post_data)
        return json.dumps(data)