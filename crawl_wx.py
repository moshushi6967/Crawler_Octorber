import requests
import json
import time
'''
遇到不懂的问题？Python学习交流群：821460695满足你的需求，资料都已经上传群文件，可以自行下载！
'''
url = 'http://mp.weixin.qq.com/mp/xxx'


def get_wx_article(biz, uin, key, index=0, count=10):
    offset = (index + 1) * count
    params = {
        '__biz': biz,
        'uin': uin,
        'key': key,
        'offset': offset,
        'count': count,
        'action': 'getmsg',
        'f': 'json'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    response = requests.get(url=url, params=params, headers=headers)
    print(response.status_code)
    resp_json = response.json()
    if resp_json.get('errmsg') == 'ok':
        resp_json = response.json()
        # 是否还有分页数据， 用于判断return的值
        can_msg_continue = resp_json['can_msg_continue']
        # 当前分页文章数
        msg_count = resp_json['msg_count']
        general_msg_list = json.loads(resp_json['general_msg_list'])
        list = general_msg_list.get('list')
        print(list, "**************")
        for i in list:
            app_msg_ext_info = i['app_msg_ext_info']
            # 标题
            title = app_msg_ext_info['title']
            # 文章地址
            content_url = app_msg_ext_info['content_url']
            # 封面图
            cover = app_msg_ext_info['cover']

            # 发布时间
            datetime = i['comm_msg_info']['datetime']
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime))


        if can_msg_continue == 1:
            return True
        return False
    else:
        print('获取文章异常...')
        return False


if __name__ == '__main__':
    biz = 'Mzg4MTA2Nzg0NA=='
    uin = 'NDIyMTI5NDM1'
    key = '20a680e825f03f1e7f38f326772e54e7dc0fd02ffba17e92730ba3f0a0329c5ed310b0bd55b3c0b1f122e5896c6261df2eaea4036ab5a5d32dbdbcb0a638f5f3605cf1821decf486bb6eb4d92d36c620'
    index = 0
    while 1:
        print(f'开始抓取公众号第{index + 1} 页文章.')
        flag = get_wx_article(biz, uin, key, index=index)
        # 防止和谐，暂停8秒
        time.sleep(8)
        index += 1
        if not flag:
            print('公众号文章已全部抓取完毕，退出程序.')
            break

        print(f'..........准备抓取公众号第{index + 1} 页文章.')
