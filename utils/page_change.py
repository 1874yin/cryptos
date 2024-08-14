
import requests
from bs4 import BeautifulSoup
import time
import re
import notify_wechat

url = "https://www.okx.com/cn/help/section/announcements-latest-announcements"
prefix = "https://www.okx.com"

REFRESH_TIME = 5 * 60
# REFRESH_TIME = 5

old_content = ''
old_article_titles = ''
old_link = ''

proxy = {
    'http':'http://localhost:7078',
    'https':'http://localhost:7078'
}

def get_newer_announcements():
    global old_content, old_article_titles
    while True:
   
        try:
            response = requests.get(url, proxies=proxy)
            if response.status_code == 200:
                new_content = response.text
                if new_content != old_content:
                    soup = BeautifulSoup(new_content, "html.parser")
                    article_titles = soup.find_all(attrs={'class': re.compile(r'index_article*')})
                    if article_titles != old_article_titles:
                        length = min(len(article_titles), len(old_article_titles))
                        for i in range(length):
                            if article_titles[i] != old_article_titles[i]:
                                article_title = article_titles[i].text.strip()
                                a_tag = article_titles[i].find('a')
                                link = ''
                                if a_tag != -1:
                                    link = a_tag.get('href')
                                    link = prefix + link
                                    parse_link(link)
                                notify_new_article(article_title, link)
                                break
                        old_article_titles = article_titles

                        old_content = new_content    
        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            time.sleep(REFRESH_TIME)


def parse_link(link):
    response = requests.get(link, proxies=proxy)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser", preserve_whitespace_tags=['p'])
        article_content_tag = soup.find(attrs={'class': re.compile(r'index_richTextContent*')})
        if article_content_tag:
            tag_content = article_content_tag.getText(separator="\n")
            print(tag_content)


def notify_new_article(article_title, link):
    print("New article:", article_title)
    content = article_title + ' 原文：' + link
    notify_wechat.sc_send("新公告", desp=content)


if __name__ == '__main__':
    get_newer_announcements()
