#!/usr/bin/env python3
from requests_html import HTMLSession
import requests
import random
import sys
import os

import logging
import logging.handlers

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler
LOG_FILE = '/opt/python/log/downloader.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10485760, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

session = HTMLSession()
list_url = 'http://www.allitebooks.com/page/'

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

def get_list(url):
    response = session.get(url)
    all_link = response.html.find('.entry-title a')
    for link in all_link:
        getBookUrl(link.attrs['href'])

def getBookUrl(url):
    response = session.get(url)
    l = response.html.find('.download-links a', first=True)
    if l is not None:
        link = l.attrs['href'];
        download(link)

def download(url):
    headers={ "User-Agent":random.choice(USER_AGENTS) }
    filename = url.split('/')[-1].replace(' ','_')
    if ".pdf" in url:
        file = '/tmp/books/'+filename
        with open(file, 'wb') as f:
            logger.info("Downloading %s",filename)
            response = requests.get(url, stream=True, headers=headers)

            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    logger.info("\r{:.0f}% [{}{}]".format((done/50.0)*100, '=' * done, ' ' * (50-done)))
            logger.info(filename, 'Download complete!!!')

def run():
    if not os.path.exists('/tmp/books/'):
        os.mkdir('/tmp/books/')
    for i in range(1,5):
        get_list(list_url + str(i))

if __name__ == '__main__':
    run()
