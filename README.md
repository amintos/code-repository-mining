# Setup instructions
This projects contains a Python 3 client-server application. Please follow the instructions for each part below:

## Client setup
1. Change directories to the `client/` folder and install the dependencies:
```
pip install -r requirements.txt
```

Then, simply scan your system for vulnerable packages via: `./checksystem.py`. Currently, only apt and pacman
package managers are supported, which translates to most Debian or Arch based Linux distributions.

## Server setup
This setup assumes the GHtorrent database dump at the HPI chair for software architecture.
Furthermore a mongoDB instance needs to be running and you need to have access to it.
The data procurement and setup is quite tedious:

1. Change directories to `data/`
2. Copy the `config.py.smpl` to `config.py` and edit it so it works for your installation
3. Run `create-cve-search-view.sql`.  Wait for completion.
4. Install `scrapy` via `pip install scrapy`
5. Download my TweetScraper fork https://github.com/flxw/TweetScraper
6. Configure the TweetScraper via its `settings.py` to reflect your PostgreSQL settings and have the TweetScraper use it
7. Run `./crawl-cve-tweets-from-github-subset` *from inside* the TweetScraper project directory. You can go ahead with the next step while the crawler is doing its thing.
8. Download and setup https://github.com/cve-search/cve-search. Wait for completion here.
9. Run `mine-cve-search-into-postgres.py`. Wait for completion.
11. Run `create-reference-url-extraction-view.sql`, `create-tweet-extracted-views.sql`, `create-cwe-nist-reference-ranking.sql` and `create-twitter-user-ranking.sql`. In that order.

The API server setup is straightforward and can be summarized in three commands:
```
cd server
pip install -r requirements.txt
hug -f api.py
```
