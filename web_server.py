from flask import Flask, request, render_template, send_file
from picuki import PicukiScraper
from anonyig import AnonyScrape
import rfeed
import datetime
import json
import requests
import os
import re
from tqdm import tqdm

app = Flask(__name__)
anony_scrape = AnonyScrape()
picuki_scrape = PicukiScraper()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    delete_existing_thumbnails()

    username = request.form['username']  
    info = anony_scrape.get_info(username)
    req = picuki_scrape.get_posts_info(username)
    story = anony_scrape.get_stories(username)
    posts = json.loads(req)
    feed_items = []
    stories_items = []
    info_items = []
    image_urls = []
    video_urls = []

    full_name = info['result']['user']['full_name']
    bio = info['result']['user']['biography']
    username = info['result']['user']['username']
    follower = str(info['result']['user']['follower_count'])
    following = str(info['result']['user']['following_count'])
    posts_count = str(info['result']['user']['media_count'])
    profile_pic = info['result']['user']['hd_profile_pic_url_info']['url']
    profile_path = os.path.join(app.root_path, 'static', 'thumbnails', 'profile.jpg')
    download_thumbnail(profile_pic, profile_path)
    info_items.append({'full_name': full_name, 'bio': bio, 'username': username, 'follower': follower, 'following': following, 'posts_count': posts_count, 'profile_pic': 'thumbnails/profile.jpg'})
    
    for post in posts:
        post_link = post['post_link']
        title = post['title']
        thumbnail_url = post['thumbnail']
        likes = post['likes']
        comments = post['comments']
        timestamp = post['time']
        clean_title = re.sub(r'\W+', '', title)
        truncated_title = clean_title[:20]
        thumbnail_path = os.path.join(app.root_path, 'static', 'thumbnails', f'{truncated_title}.jpeg')
        download_thumbnail(thumbnail_url, thumbnail_path)
        feed_items.append({'post_link': post_link, 'title': title, 'thumbnail': f'thumbnails/{truncated_title}.jpeg', 'likes': likes, 'comments': comments, 'timestamp': timestamp})
        
    try:
        for i in range(len(story['result'])):
            image_url = story['result'][i]['image_versions2']['candidates'][0]['url']
            image_sign = story['result'][i]['image_versions2']['candidates'][0]['url_signature']['signature']
            truncated_title = title[:20] 
            thumbnail_stories_path = os.path.join(app.root_path, 'static', 'thumbnails', f'story_{image_sign}.jpeg')
            download_thumbnail(image_url, thumbnail_stories_path)
            image_urls.append(f'thumbnails/story_{image_sign}.jpeg')
    except Exception:
        image_urls = []

    try:
        for i in range(len(story['result'])):
            video_url = story['result'][i]['video_versions'][0]['url']
            video_sign = str(story['result'][i]['video_versions'][0]['url_signature']['signature'])
            thumbnail_stories_video_path = os.path.join(app.root_path, 'static', 'thumbnails', f'story_{video_sign}.mp4')
            download_thumbnail(video_url, thumbnail_stories_video_path)
            video_urls.append(f'thumbnails/story_{video_sign}.mp4')
    except Exception:
        video_urls = []

    stories_items.append({'image_urls': image_urls, 'video_urls': video_urls})
    print(stories_items)
    return render_template('profile.html', feed_items=feed_items, stories_items=stories_items, info_items=info_items)

def download_thumbnail(url, file_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(file_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

def delete_existing_thumbnails():
    directory = os.path.join(app.root_path, 'static', 'thumbnails')
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))

if __name__ == "__main__":
    app.run(port=8000, debug=True)
