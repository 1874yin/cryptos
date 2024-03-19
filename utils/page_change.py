import requests
from bs4 import BeautifulSoup
import time
import re

url = "https://www.okx.com/cn/help/section/announcements-latest-announcements"

old_content = ''

proxy = {
    'http':'http://localhost:7078',
    'https':'http://localhost:7078'
}

while True:
    try:
        response = requests.get(url, proxies=proxy)
        if response.status_code == 200:
            new_content = response.text
            if new_content != old_content:
                soup = BeautifulSoup(new_content, "html.parser")
                article_title_tag = soup.find_all(attrs={'class': re.compile(r'index_article*')})
                if article_title_tag:
                    article_title = article_title_tag[0].text.strip()
                    print("New Article Title:", article_title)

                    old_content = new_content
        time.sleep(60)
    except Exception as e:
        print("An error occurred:", str(e))