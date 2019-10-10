import requests
import os
from concurrent.futures import ThreadPoolExecutor
import datetime
import random
'''
作者:moshushi
日期:2019/10/05
功能:
  根据m3u8 url地址下载视频
版本:1.0
'''


def main():
    url = 'https://2.dadi-yun.com/20190724/ZX5ROLGY//800kb/hls/index.m3u8'
    head_url = 'https://2.dadi-yun.com'
    global headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': 'https://2.dadi-yun.com/share/Xb7UtCt1uiDQOzkO'
    }
    global base_path
    base_path = r'D:\BaiduYunDownload\20180512\ts_file'
    target_path = r'D:\BaiduYunDownload\20180512\050'
    response = requests.get(url=url, headers=headers)
    print(response.status_code)
    ts_str = response.content.decode().split("\n")
    # print(ts_str)
    ts_str_list = []
    for string in ts_str:
        if string.endswith('.ts'):
            ts_str_list.append(head_url + string)
    # print(ts_str_list)
    download(ts_str_list)
    # pool = ThreadPoolExecutor(max_workers=20)
    # pool_iter = pool.map(download, ts_str_list)
    # for p_iter in pool_iter:
    #     print('thread pool is working')
    combine(base_path, target_path, "video{}".format(random.randint(2, 1000)))


def download(ts_urls):

    for i in range(len(ts_urls)):

        ts_url = ts_urls[i]

        file_name = ts_url.split("/")[-1]

        print("开始下载 %s" % file_name)

        start = datetime.datetime.now().replace(microsecond=0)

        try:

            response = requests.get(ts_url, stream=True, verify=False, headers=headers)

        except Exception as e:

            print("异常请求：%s"%e.args)

            return

        ts_path = base_path+"/{0}.ts".format(i)

        with open(ts_path, "wb+") as file:

            for chunk in response.iter_content(chunk_size=1024):

                if chunk:

                    file.write(chunk)

        end = datetime.datetime.now().replace(microsecond=0)

        print("耗时：%s"%(end-start))


def file_walker(ts_path):
    file_list = []
    for root, dirs, files in os.walk(ts_path):
        for fn in files:
            p = str(root+'/'+fn)
            file_list.append(p)
    return file_list


def file_name_sort(file_l):
    return int(file_l.split('/')[-1].strip('.ts'))


def combine(ts_path, combine_path, file_name):
    file_list = file_walker(ts_path)
    file_path = combine_path + '/' + file_name + '.ts'
    file_list.sort(key=file_name_sort)
    print(file_list)
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())


if __name__ == '__main__':
    main()
