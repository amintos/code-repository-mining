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

1. Change directories to `data/`
2. Copy the `config.py.smpl` to `config.py` and edit it so it works for your installation
3. Run `create-cve-search-view.sql`.  Wait for completion.
4. Install `scrapy` via `pip install scrapy`
5. Download my TweetScraper fork https://github.com/flxw/TweetScraper
  1. Configure the TweetScraper via its `settings.py`
4. Download and setup the github-project cve-search
6. While cve-search is downloading, run `manipulation/crawl-cve-tweets-from-github-subset.py`.  Wait for completion.
5. Once cve-search has completed setup, run `manipulation/mine-tweets-from-mongodb-to-postgres.py`. Wait for completion.
6. Run `create-reference-url-extraction-view.sql` and `create-tweet-extracted-views.sql`. Wait for completion.
1. Install all requirements 
