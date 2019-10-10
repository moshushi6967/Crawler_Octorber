import requests
from lxml import etree
import os
import re
import time


def get_text(txt_url):
    txt_url = 'http://www.87sq.com' + txt_url
    response = requests.get(url=txt_url, headers=headers)
    html_str = response.content.decode()
    html = etree.HTML(html_str)
    title = html.xpath('/html/body/div/div[3]/h1/text()')[0]
    try:
        next_page_link = html.xpath('/html/body/div/div[3]/div[3]/strong/span[2]/a/@href')[0]
        txt = re.findall(r'<div class="content">(.*?)</div>', html_str, re.S)[0]
        save_text(title, txt)
        print('finish download and save :', title)
        time.sleep(3)
        get_text(next_page_link)
    except Exception:
        print('callback end! ')


def save_text(title, txt):
    if os.path.exists(title):
        print('txt already be downloaded! ')
    else:
        txt = txt.replace(' ', '')
        txt = txt.replace('</p><p>', '')
        os.chdir(path)
        with open(f"{title}.txt", 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write(f"{txt}\n")
            f.write("\n")


if __name__ == '__main__':
    if __name__ == '__main__':
        url = '/Wznews/53430.html'
        path = r'D:\BaiduYunDownload\mzhitu\txtfile'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': 'http://www.87sq.com/Wzlist/jiqingxiaoshuo.html'
        }
        get_text(url)

