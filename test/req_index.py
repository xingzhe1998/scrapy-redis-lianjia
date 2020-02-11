import requests


def req_index():
    res = requests.get('https://sz.lianjia.com/zufang/pg1/#contentList')
    print(res.status_code)
    print(res.content.decode())


if __name__ == '__main__':
    req_index()
