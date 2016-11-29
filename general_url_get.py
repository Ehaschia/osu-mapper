import requests
import re

'''
@author Ehaschia
'''


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def get_real_url(url, num):
    proxy = {
        "http": "http://127.0.0.1:7070",
        "https": "http://127.0.0.1:7070",
    }
    headers = {
        'Host': 'www.mediafire.com',
        # 'Cache-Control': 'no-cache',
        'Accpet': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,de;q=0.2',
    }
    r = requests.get(url[num], headers=headers, proxies=proxy, allow_redirects=False)
    tmp_url = r.headers._store['location'][1]
    if re.search('file', tmp_url):
        r = requests.get(url[num], headers=headers, proxies=proxy)
        real_url = re.findall('kNO.*";', r.content)[0]
        real_url = real_url[7:-2]
    else:
        real_url = r.headers._store['location'][1]
    return real_url


if __name__ == '__main__':
    # get the short url list
    tmp_file = open('stored_url.txt', 'r')
    to_read_url = []
    line = tmp_file.readline()
    while line:
        to_read_url.append(line[:-1])
        line = tmp_file.readline()
    for i in range(0, 517):
        real_url = get_real_url(to_read_url, i)
        print(real_url)
        download_file(real_url)
