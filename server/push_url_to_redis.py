import redis


def push_func():
    pool = redis.ConnectionPool(host="xxx.xxx.xxx.xxx", port=6379, password="Your Redis Password",db=1)
    redis_client = redis.Redis(connection_pool=pool)
    for numb_sz in range(1,40):
        url_sz = 'https://sz.lianjia.com/zufang/pg{}/#contentList'.format(str(numb_sz))
        print(url_sz)
        redis_client.lpush('crawl_url:th', url_sz)


if __name__ == '__main__':
    push_func()
