# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import json
import requests
import os
import re
import math


def getSoup(url, header):
    try:
        # data_list = []
        response = requests.get(url, headers=header, verify=False, timeout=30)
        response.encoding = 'utf-8'
        # print(response.text)
        soupTexts = BeautifulSoup(response.text, 'lxml')
        return soupTexts
    except Exception as e:
        print(e)


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        try:
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print('create success')
        except Exception as e:
            print(e)
    else:
        print('file name already exists')


if __name__ == "__main__":
    head = {
        'Host': 'www.syxandlpc.love',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.syxandlpc.love/daili.php?m=Mch&c=Novel&a=index&p=1',
        'Connection': 'keep-alive',
        'Cookie': 'user=tiloj0u25q2qn00m8avke14ps3',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    head2 = {
        'Host': 'www.syxandlpc.love',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cookie': 'user=tiloj0u25q2qn00m8avke14ps3',
        'Upgrade-Insecure-Requests': '1',
    }
    for k in range(2, 65):
        bookUrl = 'http://www.syxandlpc.love/daili.php?m=Mch&c=Novel&a=index&p=%d' % k
        soup_texts = getSoup(bookUrl, head2)  # 获取书单
        soup = soup_texts.find_all('tr')
        # 遍历所有书
        bookNum = len(soup)  # 当前页书的总数
        print(bookNum)  #
        for j in range(1, bookNum):
            # print(str(j))
            book = soup[j]  # 必须从1开始运行

            basePath = 'G:\\bookdownload'  # 文件根路径
            # print(book)
            bookName = "".join(book.find_all('p')[0].text.split())
            print(bookName)  # 获取书名
            bookPath = basePath + '\\' + bookName
            mkdir(bookPath)
            chapterNum = int(re.findall('\d+', book.find_all('p')[1].text)[0])
            print(chapterNum)  # 获取章节数
            pages = math.ceil(chapterNum / 15)  # 向上取整 计算页数
            showUrl = book.find_all('a')[0]['href']
            showUrl = 'http://www.syxandlpc.love' + showUrl

            for i in range(1, pages + 1):
                print(i)
                url = showUrl + '&p=%d' % i
                response = requests.get(url, headers=head, verify=False, timeout=30)
                response.encoding = 'utf-8'
                soup_texts = BeautifulSoup(response.text, 'lxml')

                texts = soup_texts.find_all(class_='btn btn-info looks')
                h = 1
                for item in texts:
                    fileName = '第%s章' % re.findall('\d+', soup_texts.find_all('tr')[h].find_all('td')[1].text)[0] # 文件名
                    soup_text = BeautifulSoup(str(item['data-info']), 'lxml')
                    fileText = soup_text.body.text.replace('\xa0', '')  # 小说章节内容
                    # print(fileText)

                    # print(fileName)
                    # print(bookPath + '\\' + fileName + '.txt')
                    try:
                        file = open(bookPath + '\\' + fileName + '.txt', 'wb')
                        file.write(fileText.encode('utf-8'))
                        file.close()
                    except Exception as r:
                        print(r)
                    h = h + 1
