import csv
import requests
from bs4 import BeautifulSoup
from lxml import html
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 添加反爬机制
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 设置重试机制
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def fetch_article_details(url):
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 获取新闻标题
    title_tag = soup.find('h1', {'id': 'articleTitle'})
    title = title_tag.text if title_tag else '标题未找到'
    
    # 获取发布时间
    tree = html.fromstring(response.content)
    publish_time_tag = tree.xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/span/text()[2]')
    publish_time = publish_time_tag[0].strip() if publish_time_tag else '发布时间未找到'
    
    # 获取文章内容
    article_content_tags = tree.xpath('//*[@id="article"]/div/p')
    article_content = ''.join([tag.text_content().strip() for tag in article_content_tags]) if article_content_tags else '文章内容未找到'
    
    return {
        'title': title,
        'publish_time': publish_time,
        'content': article_content
    }

def main():
    with open('news.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row['链接']
            article_details = fetch_article_details(url)
            print(f"标题: {article_details['title']}")
            print(f"发布时间: {article_details['publish_time']}")
            print(f"文章内容: {article_details['content']}")
            print('-' * 80)

if __name__ == "__main__":
    main()
