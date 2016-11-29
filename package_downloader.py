import requests
from bs4 import BeautifulSoup
from cookielib import LWPCookieJar
import re
import os
import time
'''
@author Ehaschia
'''

# load url
def load_url(url, url_file):
    line = url_file.readline()
    while line:
        url.append(line[:-1])
        # print(line)
        line = url_file.readline()
    return url


def load_page(url, header, cookie_file):
    ses = requests.session()
    ses.headers.update(header)
    ses.cookies = LWPCookieJar(cookie_file)
    for i in url:
        r = ses.get(i)
        ses.cookies.save()
        print r.url, r.history
        soup = BeautifulSoup(r.content)
        print(soup.prettify())


if __name__ == '__main__':
    COOKIE_FILE = 'package_cookie.txt'
    url_file = open('stored_url.txt', 'r')
    url = []
    store_url =[]
    headers = {
        'Host': 'www.mediafire.com',
        # 'Cache-Control': 'no-cache',
        'Accpet': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,de;q=0.2',
    }
    #url = ['http://www.mediafire.com/?2gfnyzx4z6xyjuz']
    load_url(url, url_file)
    #load_page(url, headers, COOKIE_FILE)
    for i in url:
        r = requests.get(i)
        match_line = re.findall('kNO.*";', r.content)[0]
        print match_line[7:-2]
        store_url.append(match_line[7:-2])
        time.sleep(30)
    store_file = open('download_url.txt', 'w')
    for i in store_url:
        store_file.write(i)
        store_file.write('\n')
    store_file.close()
    print("success stored url!")