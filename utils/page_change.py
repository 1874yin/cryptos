import requests
from bs4 import BeautifulSoup
import time
import re
from config import Config as config
import notify_wechat

url = "https://www.okx.com/cn/help/section/announcements-latest-announcements"
prefix = "https://www.okx.com"

old_content = ''
old_title = ''
old_link = ''

proxy = config.PROXY


def get_newer_announcements():
    global old_content, old_title
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
                        if article_title != old_title:
                            notify_new_article(article_title)
                            old_title = article_title
                            a_tag = article_title_tag[0].find('a')
                            if a_tag:
                                link = a_tag.get('href')
                                link = prefix + link
                                parse_link(link)
                        old_content = new_content
            time.sleep(config.REFRESH_TIME)
        except Exception as e:
            print("An error occurred:", str(e))


def parse_link(link):
    response = requests.get(link, proxies=proxy)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser", preserve_whitespace_tags=['p'])
        article_content_tag = soup.find(attrs={'class': re.compile(r'index_richTextContent*')})
        if article_content_tag:
            tag_content = article_content_tag.getText(separator="\n")
            print(tag_content)


def notify_new_article(article_title):
    print("New article:", article_title)
    notify_wechat.sc_send("新公告", desp=article_title)


if __name__ == '__main__':
    get_newer_announcements()
