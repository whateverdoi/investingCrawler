import requests
from lxml import html
import csv

def fetch_news(url, output_file):
    # 发送HTTP请求
    response = requests.get(url)
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

if __name__ == "__main__":
    # 更新后的URL
    url = "https://cn.investing.com/news/latest-news"
    output_file = 'news.csv'
    fetch_news(url, output_file)
