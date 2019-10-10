import requests
from lxml import etree
import os
import time
import threading


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


def run():
    org_url = 'https://www.mzitu.com/162495/22'
    url = org_url.strip(org_url.split('/')[-1]) + '{}'
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
    org_time = time.time()
    t2 = threading.Thread(target=pic_save, args=(link_url_list,))
    t2.start()
    t1 = threading.Thread(target=pic_save, args=(link_url_list,))
    t1.start()
    # pic_save(link_url_list)
    # duration_time = time.time() - org_time
    # print('download picture time: ', duration_time)


if __name__ == '__main__':
    run()