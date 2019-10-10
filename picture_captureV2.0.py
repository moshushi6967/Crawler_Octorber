"""
  作者：下流小王子
  版本：2.0
  时间：2019/9/26
  功能：下载美女图片，需要营养快线
"""
import requests
from lxml import etree
import os
import threading


class MeizhiSpider:
    def __init__(self, url):
        self.url = url + "/{}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': 'https://www.mzitu.com/193247/5'
        }
        self.path = r'D:\BaiduYunDownload\mzhitu'

    def get_url_list(self, pic_max):
        return [self.url.format(i) for i in range(1, int(pic_max)+1)]

    def parse_url(self, url):
        response = requests.get(url=url, headers=self.headers)
        print(response.status_code)
        return response.content

    def get_pic_list(self, url_list):
        pic_link_list = []
        for url in url_list:
            html_str = self.parse_url(url).decode()
            html = etree.HTML(html_str)
            pic_link = html.xpath("//div[@class='main-image']/p/a/img/@src")
            pic_link_list.append(pic_link)
        return pic_link_list

    def save_pic(self, pic_link_list, pic_title):
        if pic_title:
            print('准备爬取: ', pic_title)
            os.chdir(self.path)
            if os.path.exists(pic_title.strip()):
                print('目录已存在 ')
            else:
                os.mkdir(self.path+'/'+pic_title.strip())
            os.chdir(pic_title)
            for pic_link in pic_link_list:
                with open(pic_link[0].split(r'/')[-1], 'wb') as f:
                    f.write(self.parse_url(pic_link[0]))

    def run(self):
        content = self.parse_url(self.url.format(2))
        html_str = content.decode()
        html = etree.HTML(html_str)
        pic_max = html.xpath('//div[@class="pagenavi"]/a/span/text()')[-2]
        pic_title = html.xpath("//div[@class='main-image']/p/a/img/@alt")[0]
        url_list = self.get_url_list(pic_max)
        print(url_list)
        pic_link_list = self.get_pic_list(url_list)
        print(pic_link_list)
        self.save_pic(pic_link_list, pic_title)

        # 1. url_list
        # 2.历遍url，发送请求，获取响应
        # 3.提取数据
        # 4.保存


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


if __name__ == "__main__":
    search_url = 'https://www.mzitu.com/search/%E9%BB%84%E6%A5%BD%E7%84%B6/page/1/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': 'https://www.mzitu.com/193247/5'
    }
    res = requests.get(url=search_url,headers=headers)
    print(res.status_code)
    dir_title = search_url.split('/')[-3]
    print(dir_title)
    html = etree.HTML(res.content.decode())
    post_list = html.xpath('//*[@id="pins"]/li/a/@href')
    print(post_list)
    for url in post_list:
        meizhi = MeizhiSpider(url)
        meizhi.run()