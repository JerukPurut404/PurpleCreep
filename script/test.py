from picuki import PicukiScraper
from anonyig import AnonyScrape
import rfeed
import datetime
import requests
import time
import json

anony_scrape = AnonyScrape()
picuki_scrape = PicukiScraper()
req = picuki_scrape.get_posts_info(" ")
posts = json.loads(req)
stories = anony_scrape.get_stories(" ")

def create_feed(username):
    feed_items = []
    
    for story in stories['result']:
        video = rfeed.Item(
            title="NEW STORY",
            link=story['video_versions'][0]['url'],
            pubDate=datetime.datetime.fromtimestamp(story['taken_at'])
        )
        feed_items.append(video)
    
    for post in posts:
        feed_item = rfeed.Item(
            title=post['title'],
            link=post['thumbnail'],
            pubDate=datetime.datetime.now()
        )
        feed_items.append(feed_item)
    
    feed = rfeed.Feed(
        title=f"Instagram Info from {username}",
        description="Latest Instagram info",
        language="en-US",
        items=feed_items,
        link="https://instagram.com",
        lastBuildDate=datetime.datetime.now(),
    )
    
    rss = feed.rss()
    with open("instagram_feed2.xml", "w", encoding="utf-8") as f:
        f.write(rss)

create_feed(" ")
