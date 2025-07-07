# 📰 News-Web-Scraper

## Overview

**News-Web-Scraper** is a Python-based command-line tool that gathers the latest news articles from popular RSS feeds like BBC, CNN, and Reuters. It pulls full-text content using asynchronous web scraping, processes the articles, and exports them to a structured CSV file for easy analysis.

This tool is useful for news aggregators, media analysts, researchers, and anyone who wants quick access to clean, summarized article data.

---

## System Architecture

### Frontend Architecture

- **Interface**: Command-line interface (CLI)
- **User Interaction**: Simple terminal messages and progress bar using `tqdm`
- **Output**: Clean, formatted `articles.csv` file with essential article info

### Backend Architecture

- **Core Logic**: Python-based scraper with async support
- **Networking**: `aiohttp` for fast HTTP requests
- **RSS Parsing**: `feedparser` for reading RSS feeds
- **Article Extraction**: `newspaper3k` for parsing article content
- **Text Preprocessing**: `nltk` for sentence segmentation
- **File Export**: `csv` module for exporting structured data

---

## Modular Design

### 1. Feed Fetcher

- Parses RSS feeds using `feedparser`
- Limits to top 5 articles per feed for quick scrapes

### 2. Article Scraper (Async)

- Asynchronously fetches full article HTML
- Parses content, title, authors, image, and date using `newspaper3k`
- Fallback handling for failed requests

### 3. Data Exporter

- Saves all valid articles to a `CSV` file
- Fields: title, url, authors, publish date, top image, truncated text

---

## Key Components

### `fetch_feed_entries(feed_url)`

- Grabs entries from the RSS URL using `feedparser`

### `fetch_article(session, url)`

- Asynchronously downloads and parses each article
- Uses `newspaper.Article` for full content extraction

### `scrape_all_articles(feed_urls)`

- Coordinates the scraping process using `aiohttp` and `asyncio`
- Handles session management and concurrent tasks
- Displays real-time progress bar with `tqdm`

### `export_to_csv(articles, filename='articles.csv')`

- Writes the collected data into a CSV file
- Handles encoding and formatting

---

## Data Flow

```text
RSS Feeds → FeedParser → Async Fetch (aiohttp) → Newspaper3k Parsing → CSV Export
````

1. Load RSS feeds
2. Extract top article URLs
3. Download and parse articles asynchronously
4. Clean and truncate article text
5. Export all data to a CSV file

---

## External Dependencies

### Core Libraries

* [`aiohttp`](https://docs.aiohttp.org/) – for non-blocking HTTP requests
* [`feedparser`](https://pythonhosted.org/feedparser/) – RSS feed parsing
* [`newspaper3k`](https://github.com/codelucas/newspaper) – article extraction
* [`nltk`](https://www.nltk.org/) – natural language toolkit for tokenization
* [`tqdm`](https://github.com/tqdm/tqdm) – progress bar visualization
* [`csv`](https://docs.python.org/3/library/csv.html) – built-in CSV support

### Optional Utilities

* `logging` – for controlling noisy output from `newspaper3k`
* `nltk.download()` – ensures tokenizer is available at runtime

---

## Setup Instructions

### ✅ Requirements

* Python 3.7+
* Internet connection to fetch articles

### 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/News-Web-Scraper.git
cd News-Web-Scraper
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

> Sample `requirements.txt`:

```
aiohttp
feedparser
newspaper3k
nltk
tqdm
```

3. Run the scraper:

```bash
python scraper.py
```

4. Check the generated `articles.csv` file in the root directory.

---

## Example Output

| Title           | URL                                              | Authors  | Publish Date | Image                                  | Text (Truncated)              |
| --------------- | ------------------------------------------------ | -------- | ------------ | -------------------------------------- | ----------------------------- |
| Sample Headline | [https://cnn.com/sample](https://cnn.com/sample) | John Doe | 2024-07-01   | [https://image.jpg](https://image.jpg) | Lorem ipsum dolor sit amet... |

---

## Deployment Strategy

### Local Usage

* **Run Locally**: `python scraper.py`
* **Output Format**: `CSV`, editable in Excel, Python, or any data tool

### Performance

* Asynchronous fetching boosts performance
* Suitable for small to medium-scale news aggregation tasks


## License

This project is licensed under the **Apache License 2.0**.
