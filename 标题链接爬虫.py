import requests
from lxml import html
import csv
import random
import time

def fetch_news(url, output_file):
    # 设置User-Agent以模拟浏览器请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 发送HTTP请求
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'  # 设置编码

            # 解析HTML内容
            tree = html.fromstring(response.text)

            # 使用XPath查找新闻标题和链接
            news_items = tree.xpath('//a[@class="text-inv-blue-500 hover:text-inv-blue-500 hover:underline focus:text-inv-blue-500 focus:underline whitespace-normal text-sm font-bold leading-5 !text-[#181C21] sm:text-base sm:leading-6 lg:text-lg lg:leading-7" and @data-test="article-title-link"]')

            # 打开CSV文件并写入新闻标题和链接
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['标题', '链接']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for item in news_items:
                    title = item.text_content()
                    link = item.get('href')
                    writer.writerow({'标题': title, '链接': link})

            # 增加随机延迟，防止被反爬虫机制检测到
            time.sleep(random.uniform(1, 3))
            break
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise

if __name__ == "__main__":
    # 更新后的URL
    url = "https://cn.investing.com/news/latest-news"
    output_file = 'news.csv'
    fetch_news(url, output_file)
