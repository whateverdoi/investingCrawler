
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        # We'll add our crawling code here
        result = await crawler.arun(url="https://cn.investing.com/news/forex-news/article-2530384")
        
        # 将结果保存为 Markdown 文件
        with open("crawl_result.md", "w", encoding="utf-8") as file:
            file.write(result.markdown)
        
        print("Crawl result saved as 'crawl_result.md'")
if __name__ == "__main__":
    asyncio.run(main())