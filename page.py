# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import threading
import json
import requests
import os
import queue


def getJson(url, header):
    try:
        # data_list = []
        response = requests.get(url, headers=header, verify=False, timeout=30)
        response.encoding = 'utf-8'
        # print(response.text)
        dic = json.loads(response.text)['data']
        return dic
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


class downloadPage(object):
    class download(threading.Thread):
        def __init__(self, fileQueue, urlQueue, head):
            threading.Thread.__init__(self)
            self.urlQueue = urlQueue
            self.fileQueue = fileQueue
            self.head = head

        def run(self):
            while True:
                if self.urlQueue.empty():
                    break
                filePath = self.fileQueue.get()
                # print(filePath)
                url = self.urlQueue.get()
                # print(url)
                head = self.head
                try:
                    response = requests.get(url, headers=head, verify=False, timeout=30)
                    response.encoding = 'utf-8'
                    soup_texts = BeautifulSoup(response.text, 'lxml')
                    texts = soup_texts.find_all(class_='book-main')
                    soup_text = BeautifulSoup(str(texts), 'lxml')
                    fileText = soup_text.div.text.replace('\xa0', '')
                    file = open(filePath, 'wb')
                    file.write(fileText.encode('utf-8'))
                    file.close()
                except Exception as r:
                    print(r)


if __name__ == "__main__":
    downloadPage = downloadPage()
    url_queue = queue.Queue()
    file_queue = queue.Queue()
    bookUrl = 'http://book.mdjxqqw.cn/agent/novel/index.html?page=1&limit=1000'
    bookHead = {
        'Host': 'book.mdjxqqw.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'http://book.mdjxqqw.cn/agent/novel/index.html',
        'Cookie': 'PHPSESSID=8u0f757pm786dja8ou7kr0a9u2',
    }
    chapterHead = {
        'Host': 'book.mdjxqqw.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'http://book.mdjxqqw.cn/agent/novel/chapter.html?book_id=%d',
        'Cookie': 'PHPSESSID=8u0f757pm786dja8ou7kr0a9u2',
    }
    bookJson = getJson(bookUrl, bookHead)
    # print(bookJson[0])
    num = int(len(bookJson))
    basePath = os.getcwd() + '\\download'
    for i in range(num):
        # print(bookJson[i]['id'])
        # print(bookJson[i]['name'])
        chapterHead['Referer'] = 'http://book.mdjxqqw.cn/agent/novel/chapter.html?book_id=%d'
        chapterHead['Referer'] = chapterHead['Referer'] % int(bookJson[i]['id'])
        # print(bookJson[i]['name'])
        bookPath = basePath + '\\' + bookJson[i]['name'].strip()
        # print(bookPath)
        mkdir(bookPath)
        print(bookJson[i]['name'] + "is start book_id = " + bookJson[i]['id'])
        # print (chapterHead['Referer'])
        chapterUrl = chapterHead['Referer'] + '&page=1&limit=%d' % int(bookJson[i]['total_chapter'])
        chapterJson = getJson(chapterUrl, chapterHead)
        # print (chapterJson[51]['name'] + chapterJson[51]['id'])
        for j in range(int(len(chapterJson))):
            showUrl = 'http://book.mdjxqqw.cn/agent/novel/showinfo.html?id=%s' % chapterJson[j]['id']
            showHead = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
                'Cookie': 'PHPSESSID=8u0f757pm786dja8ou7kr0a9u2'
            }
            url_queue.put(showUrl)
            file_queue.put(bookPath + '\\' + chapterJson[j]['name'].strip() + '.txt')
        threads = []
        for t in range(50):
            threads.append(downloadPage.download(file_queue, url_queue, showHead))
        for thread in threads:
            thread.start()
        # 启动线程
        for thread in threads:
            thread.join()
        # 阻塞线程
