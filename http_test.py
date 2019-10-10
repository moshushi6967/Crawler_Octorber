import requests
import re

def main():
    org_url = 'http://www.yhdzx.com/?m=vod-play-id-26402-src-1-num-1.html'
    response = requests.get(org_url)
    js_url = re.findall('mac_url=unescape\(\'(.*?)\'\);',response.text,re.S)[0]
    print(js_url)


if __name__ == '__main__':
    main()