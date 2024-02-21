import requests 
from bs4 import BeautifulSoup 
import re
import json
username = " "
r = requests.get(f"https://instanavigation.com/user-profile/{username}")
soup = BeautifulSoup(r.content, 'html.parser') 
content = str(soup.find_all('profile-page'))

# Define regex patterns to extract data
user_info_pattern = r'"username":"(.*?)","fullName":"(.*?)","profilePicUrl":"(.*?)","biography":"(.*?)","followsCount":(.*?),"followedByCount":(.*?),"mediaCount":(.*?),"isPrivate":(.*?)'
highlights_pattern = r'"id":"(.*?)","title":"(.*?)","imageThumbnail":"(.*?)"'
posts_pattern = r'"id":"(.?)","type":"(.?)","isVideo":(.?),"caption":"(.?),"likesCount":(.?),"commentsCount":(.?),"createdTime":"(.?),"thumbnailUrl":"(.?),"sidecarItems":\[\]'
stories_pattern = r'"createdTime":"([^"]+)","type":"([^"]+)","thumbnailUrl":"([^"]+)","videoUrl":"([^"]+)"'

# Extract user info using regex
user_info_match = re.search(user_info_pattern, content)
user_info = {
    "username": user_info_match.group(1),
    "fullName": user_info_match.group(2),
    "profilePicUrl": user_info_match.group(3),
    "biography": user_info_match.group(4),
    "followsCount": int(user_info_match.group(5)),
    "followedByCount": int(user_info_match.group(6)),
    "mediaCount": int(user_info_match.group(7)),
    "isPrivate": user_info_match.group(8)
}

# Extract posts using regex
posts = []
for post_match in re.finditer(posts_pattern, content):
    post = {
        "type": post_match.group(1),
        "isVideo": bool(post_match.group(2)),
        "caption": post_match.group(3),
        "likesCount": int(post_match.group(4)),
        "commentsCount": int(post_match.group(5)),
        "createdTime": post_match.group(6),
        "thumbnailUrl": post_match.group(7)
    }
    posts.append(post)

highlights = []
for highlight_match in re.finditer(highlights_pattern, content):
  highlight = {
    "id": highlight_match.group(1),
    "title": highlight_match.group(2),
    "imageThumbnail": highlight_match.group(3)  
  }
  highlights.append(highlight)

stories = []
for story_match in re.finditer(stories_pattern, content):
  story = {
    "createdTime": story_match.group(1),
    "type": story_match.group(2),
    "thumbnailUrl": story_match.group(3),
    "videoUrl": story_match.group(4)
  }
  stories.append(story)

# Create JSON object
result = {
    "user_info": user_info,
    "posts": posts,
    "highlights": highlights,
    "stories": stories
}

# Convert JSON object to string
result_json = json.dumps(result, indent=4)
print(result_json)