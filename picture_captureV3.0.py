"""
  作者：下流小王子
  版本：3.0
  时间：2019/9/26
  功能：下载美女图片，需要营养快线
"""
import requests
from lxml import etree
import os
import time
import threading


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def pic_save(link_list):
    for pic_link in link_list:
        thread_lock = threading.RLock()
        thread_lock.acquire()
        file_name = pic_link[0].split(r'/')[-1]
        if os.path.exists(file_name):
            print('picture already exists! ')
        else:
            with open(file_name, 'wb') as f:
                req = requests.get(url=pic_link[0], headers=headers)
                # print('picture download result: ', req.status_code)
                f.write(req.content)
                time.sleep(0.1)
        thread_lock.release()


def url_list_get(url, pic_max):
    url_time = time.time()
    link_list = []
    for i in range(1, int(pic_max)+1):
        target = url.format(i)
        html = requests.get(url=target, headers=headers)
        # print('url_get_list result: ',html.status_code)
        html_str = etree.HTML(html.content.decode())
        pic_link = html_str.xpath("//div[@class='main-image']/p/a/img/@src")
        link_list.append(pic_link)
    print('get url_list spent time : ', time.time()-url_time)
    return link_list


def run(main_url):
    org_url = main_url
    url = org_url + '/{}'
    global headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': 'https://www.mzitu.com/193247/5'
    }
    req = requests.get(url=org_url, headers=headers)
    print(req.status_code)
    html_str = etree.HTML(req.content.decode())
    pic_max = html_str.xpath('//div[@class="pagenavi"]/a/span/text()')[-2]
    pic_title = html_str.xpath("//div[@class='main-image']/p/a/img/@alt")
    print(pic_title)
    print(pic_max)
    path = r'D:\BaiduYunDownload\mzhitu'
    os.chdir(path)
    if os.path.exists(pic_title[0]):
        # print('direction already exists! ')
        pass
    else:
        os.mkdir(pic_title[0])
    os.chdir(pic_title[0])
    link_url_list = url_list_get(url, pic_max)
    # print(pic_link)
    for _ in range(5):
        t = threading.Thread(target=pic_save, args=(link_url_list,))
        t.start()
        t.join()
    # pic_save(link_url_list)
    # duration_time = time.time() - org_time
    # print('download picture time: ', duration_time)


if __name__ == '__main__':
    search_url = 'https://www.mzitu.com/search/%E9%BB%84%E6%A5%BD%E7%84%B6/page/1/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': 'https://www.mzitu.com/193247/5'
    }
    res = requests.get(url=search_url, headers=headers)
    print(res.status_code)
    html = etree.HTML(res.content.decode())
    post_list = html.xpath('//*[@id="pins"]/li/a/@href')
    post_page_max = html.xpath('/html/body/div[2]/div[1]/div[2]/nav/div/a[1]/text()')[0]
    print(post_page_max)
    print(post_list)
    for url in post_list:
            run(url)
    if post_page_max != 1:
        for i in range(2, int(post_page_max) + 1):
            target_url = search_url[:-2] + repr(i)
            res = requests.get(url=target_url, headers=headers)
            html = etree.HTML(res.content.decode())
            post_list = html.xpath('//*[@id="pins"]/li/a/@href')
            for url in post_list:
                run(url)