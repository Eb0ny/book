# -*- coding:UTF-8 -*-
import os
from urllib import request
from bs4 import BeautifulSoup

if __name__ == "__main__":
    download_url = 'http://book.mdjxqqw.cn/agent/novel/showinfo.html?id=417790'
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    head['Cookie'] = 'PHPSESSID=n1g7vfmsjct950tfbhjks4cc3e'
    # for id in range(500000):
    download_req = request.Request(url=download_url, headers=head)
    download_response = request.urlopen(download_req)
    download_html = download_response.read().decode('utf-8', 'ignore')
    soup_texts = BeautifulSoup(download_html, 'lxml')
    texts = soup_texts.find_all(class_='book-main')
    soup_text = BeautifulSoup(str(texts), 'lxml')
    print(soup_text.div.text)


    print(soup_text.div.text.replace('\xa0',''))


