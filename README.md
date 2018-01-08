# Working dump for the Code Repository Mining seminar

# Setup
Assuming a vanilla gh-torrent PostgreSQL and a running mongoDB database:
1. Copy the `config.py.smpl` to `config.py`
2. Run `create-cve-search-view.sql`.  Wait for completion.
3. Install `scrapy`, a Python package, and download the TweetScraper addition and configure it to use the PostgreSQL database
  a. https://github.com/flxw/TweetScraper
4. Download and setup the github-project cve-search
6. While cve-search is downloading, run `manipulation/crawl-cve-tweets-from-github-subset.py`.  Wait for completion.
5. Once cve-search has completed setup, run `manipulation/mine-tweets-from-mongodb-to-postgres.py`. Wait for completion.
6. Run `create-reference-url-extraction-view.sql` and `create-tweet-extracted-views.sql`. Wait for completion.
