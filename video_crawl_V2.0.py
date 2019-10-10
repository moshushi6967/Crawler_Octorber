import requests
import os
from concurrent.futures import ThreadPoolExecutor
import datetime
import time
import random
import urllib3
'''
作者:moshushi
日期:2019/10/05
功能:
  多线程根据m3u8 url地址下载视频
版本:2.0
'''


class FileCombineTool:
    def __init__(self, base_path, target_path, file_name):
        self.base_path = base_path
        self.target_path = target_path
        self.file_name = file_name
        self.combine()

    def file_walker(self):
        file_list = []
        for root, dirs, files in os.walk(self.base_path):
            for fn in files:
                p = str(root + '/' + fn)
                file_list.append(p)
        return file_list

    def file_sort(self, file_l):
        return int(file_l.split('/')[-1].strip('.ts'))

    def combine(self):
        file_list = self.file_walker()
        file_path = self.target_path + '/' + self.file_name + '.mp4'
        # file_list.sort(key=file_name_sort)
        file_list.sort(key=self.file_sort)
        # print(file_list)
        if os.path.exists(file_path):
            print('file exist! ')
        else:
            with open(file_path, 'wb+') as fw:
                for i in range(len(file_list)):
                    fw.write(open(file_list[i], 'rb').read())


class M3u8DownloadTool:
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        # iPhone 6：
        "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
    ]

    def __init__(self, m3u8_url, title):
        self.m3u8_url = m3u8_url
        self.title = title
        self.headers = {
            'User-Agent': random.choice(M3u8DownloadTool.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate,br',
            'referer': 'https://img.mascwgs.com/ckplayer/ckplayer.swf',
        }
        self.base_path = 'D:/BaiduYunDownload/20180512/ts_file' + '/' + self.title
        self.target_path = 'D:/BaiduYunDownload/20180512/050'

    def url_parse(self, url):
        return requests.get(url=url, headers=self.headers).content.decode()

    def get_ts_url_list(self, m3u8_response):
        ts_str = m3u8_response.split("\n")
        ts_url_list = []
        head_url = self.m3u8_url[:self.m3u8_url.index('.com')+4]
        for string in ts_str:
            if string.endswith('.ts'):
                ts_url_list.append(head_url + string)
        print(ts_url_list[-5:])
        return ts_url_list

    def ts_download(self, ts_url):
        file_name = ts_url.split("/")[-1]
        ts_file = self.base_path + "/{0}.ts".format(file_name.split('.')[0][-5:])
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)
        if os.path.exists(ts_file):
            print('ts file exists ! ')
        else:
            try:
                print("开始下载 %s" % file_name)
                start = datetime.datetime.now().replace(microsecond=0)
                time.sleep(0.5)
                urllib3.disable_warnings()
                response = requests.get(ts_url, stream=True, verify=False, headers=self.headers)
            except Exception as e:
                print("异常请求：%s" % e.args)
                return
            with open(ts_file, "wb+") as file:

                for chunk in response.iter_content(chunk_size=1024):

                    if chunk:
                        file.write(chunk)

            end = datetime.datetime.now().replace(microsecond=0)
            print("耗时：%s" % (end - start))
            return ts_url

    def __call__(self):
        m3u8_url_response = self.url_parse(self.m3u8_url)
        ts_url_list = self.get_ts_url_list(m3u8_url_response)
        pool = ThreadPoolExecutor(max_workers=30)
        for ts_url in pool.map(self.ts_download, ts_url_list):
            print('download file is :', ts_url)
        FileCombineTool(self.base_path, self.target_path, self.title)


if __name__ == '__main__':
    url = 'https://hao.czybjz.com/ppvod/A89373E703519EC19A211D156E98DEFE.m3u8'
    video_title = '极速杀手'
    m3u8_download = M3u8DownloadTool(url, video_title)
    m3u8_download()
#
# def main():
#     # url = 'https://2.dadi-yun.com/20190722/WiTd7N9K//800kb/hls/index.m3u8'
#     url = input('please input your m3u8 url address: ')
#     index_end = url.index('.com') + 4
#     head_url = url[:index_end]
#     print(head_url)
#     ran_num = random.randint(2, 10000)
#     global headers
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
#         'Referer': 'https://2.dadi-yun.com/share/Xb7UtCt1uiDQOzkO'
#     }
#     global base_path
#     base_path = r'D:\BaiduYunDownload\20180512\ts_file' + '/' + repr(ran_num)
#     if not os.path.exists(base_path):
#         os.mkdir(base_path)
#     # os.remove(base_path)
#     target_path = r'D:\BaiduYunDownload\20180512\050'
#     response = requests.get(url=url, headers=headers)
#     print(response.status_code)
#
#
#
#
#
# def download(ts_url):
#     file_name = ts_url.split("/")[-1]
#
#     print("开始下载 %s" % file_name)
#
#     start = datetime.datetime.now().replace(microsecond=0)
#
#     try:
#
#         response = requests.get(ts_url, stream=True, verify=False, headers=headers)
#
#     except Exception as e:
#
#         print("异常请求：%s"%e.args)
#
#         return
#
#     ts_path = base_path+"/{0}.ts".format(file_name.split('.')[0][-3:])
#     if os.path.exists(ts_path):
#         print('ts file exists ! ')
#     else:
#         with open(ts_path, "wb+") as file:
#
#             for chunk in response.iter_content(chunk_size=1024):
#
#                 if chunk:
#
#                     file.write(chunk)
#
#         end = datetime.datetime.now().replace(microsecond=0)
#         print("耗时：%s"%(end-start))
#         return ts_url
#
#
# def file_walker(ts_path):
#     file_list = []
#     for root, dirs, files in os.walk(ts_path):
#         for fn in files:
#             p = str(root+'/'+fn)
#             file_list.append(p)
#     return file_list
#
#
# def file_name_sort(file_l):
#     return int(file_l.split('/')[-1].strip('.ts'))
#
#
# def combine(ts_path, combine_path, file_name):
#     file_list = file_walker(ts_path)
#     file_path = combine_path + '/' + file_name + '.ts'
#     file_list.sort(key=file_name_sort)
#     print(file_list)
#     if os.path.exists(file_path):
#         print('file exist! ')
#     else:
#         with open(file_path, 'wb+') as fw:
#             for i in range(len(file_list)):
#                 fw.write(open(file_list[i], 'rb').read())
#
#
# if __name__ == '__main__':
#     main()
