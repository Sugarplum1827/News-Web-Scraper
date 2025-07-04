import asyncio
import feedparser
from newspaper import Article
import aiohttp
from tqdm import tqdm
import logging
import nltk
import csv

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
logging.getLogger("newspaper").setLevel(logging.WARNING)

RSS_FEEDS = [
    'http://feeds.bbci.co.uk/news/rss.xml',
    'http://rss.cnn.com/rss/edition.rss',
    'http://feeds.reuters.com/reuters/topNews'
]


def fetch_feed_entries(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries


async def fetch_article(session, url):
    try:
        article = Article(url, language='en')
        async with session.get(url, timeout=10) as response:
            html = await response.text()
            article.set_html(html)
            article.download_state = 2
            article.parse()
            return {
                'url': url,
                'title': article.title,
                'authors': article.authors,
                'publish_date': str(article.publish_date),
                'top_image': article.top_image,
                'text': article.text[:500] + '...'
            }
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None


async def scrape_all_articles(feed_urls):
    articles = []
    async with aiohttp.ClientSession(
            headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = []
        for feed_url in feed_urls:
            entries = fetch_feed_entries(feed_url)
            for entry in entries[:5]:
                tasks.append(fetch_article(session, entry.link))

        for future in tqdm(asyncio.as_completed(tasks),
                           total=len(tasks),
                           desc="Scraping"):
            result = await future
            if result:
                articles.append(result)
    return articles


def export_to_csv(articles, filename='articles.csv'):
    fieldnames = [
        'title', 'url', 'authors', 'publish_date', 'top_image', 'text'
    ]
    with open(filename, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'authors': ", ".join(article.get('authors', [])),
                'publish_date': article.get('publish_date', ''),
                'top_image': article.get('top_image', ''),
                'text': article.get('text', '')
            })
    print(f"\n✅ Exported {len(articles)} articles to {filename}")


if __name__ == '__main__':
    all_articles = asyncio.run(scrape_all_articles(RSS_FEEDS))
    export_to_csv(all_articles)
