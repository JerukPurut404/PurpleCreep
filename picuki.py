import cloudscraper
from bs4 import BeautifulSoup
import json
import re

class PicukiScraper:
    def __init__(self, delay=10, browser="chrome"):
        self.scraper = cloudscraper.create_scraper(delay=delay, browser=browser)

    def get_posts_info(self, username):
        try:
            page = self.scraper.get(f"https://www.picuki.com/profile/{username}")
            soup = BeautifulSoup(page.content, "html.parser")
            posts = soup.find_all("div", class_="photo")
            likes = soup.find_all("div", class_="likes_photo")
            comments = soup.find_all("div", class_="comments_photo")
            times = [div.find('span').text for div in soup.find_all("div", class_='time')]
            data = []
            for post, like, comment, time in zip(posts, likes, comments, times):
                link = post.find("a")
                post_link = link["href"]
                img = link.find("img")
                title = img["alt"]
                thumbnail = img["src"]
                likes_text = like.get_text().strip()
                clean_likes_text = re.sub(r'favorite_border', '', likes_text)
                comments_count = comment.get_text().strip()
                comments_count_clean = re.sub(r'chat_bubble_outline', '', comments_count)
                post_data = {
                    "post_link": post_link,
                    "title": title,
                    "thumbnail": thumbnail,
                    "likes": clean_likes_text,
                    "comments": comments_count_clean,
                    "time": time
                }
                data.append(post_data)
            return json.dumps(data)
        except Exception as e:
            return str(e)


    def get_post(self, post_link):
        page = self.scraper.get(post_link)
        soup = BeautifulSoup(page.content, "html.parser")
        data = []
        try:            
            posts = soup.find_all("div", class_=["item", "single-photo"])
            for post in posts:
                img = post.find("img")
                video = post.find("video")
                img_src = img["src"] if img else None
                video_src = video['src'] if video else None
                post_data = {
                    "image": img_src,
                    "video": video_src
                }
                data.append(post_data)
            return json.dumps(data)
        except Exception as e:
            return str(e)

