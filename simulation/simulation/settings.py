# -*- coding: utf-8 -*-

BOT_NAME = 'simulation'

SPIDER_MODULES = ['simulation.simulation.spiders']
NEWSPIDER_MODULE = 'simulation.simulation.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 '\
             '(KHTML, like Gecko) Chrome / 63.0.3239.84 Safari / 537.36'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 16
COOKIES_ENABLED = True

FEED_FORMAT = 'json'
FEED_URI = 'principals_data.json'
