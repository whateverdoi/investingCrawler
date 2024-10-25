import csv
import requests
from bs4 import BeautifulSoup
from lxml import html

# 添加反爬机制
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def fetch_article_details(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 获取新闻标题
    title_tag = soup.find('h1', {'id': 'articleTitle'})
    title = title_tag.text if title_tag else '标题未找到'
    
    # 获取发布时间
    tree = html.fromstring(response.content)
    publish_time_tag = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span/text()[2]')
    publish_time = publish_time_tag[0].strip() if publish_time_tag else '发布时间未找到'
    
    # 获取文章内容
    article_content_tag = soup.find('p')
    article_content = article_content_tag.text.strip() if article_content_tag else '文章内容未找到'
    
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
