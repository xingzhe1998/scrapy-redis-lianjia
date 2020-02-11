# -*- coding: utf-8 -*-
import re
from scrapy import Request
from urllib.request import urljoin
from lianjia.items import LianjiaItem
from scrapy_redis.spiders import RedisSpider


class SpiderSpider(RedisSpider):

    name = 'spider'
    # allowed_domains = ['lianjia.com']
    # start_urls = ['https://www.sz.lianjia.com/']
    # redis_key = 'crawl:spider_task_url'


    def __init__(self, site_code='', *args, **kwargs):
        super(SpiderSpider, self).__init__(*args, **kwargs)
        # 可以在爬虫的构造方法里指定redis_key，这个发现很重要
        # 因为如此便可以通过命令行模式指定从哪个redis队列取值
        # exp: scrapy crawl spider -a site_code=th
        # 便可以指定site_code
        self.redis_key = 'crawl_url:' + site_code


    def make_request_from_data(self, data):
        print('make_request_from_data')
        # 取出来的数据为`bytes`类型的字符串
        url = data.decode()
        headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://sz.lianjia.com',
            'Referer': 'https://sz.lianjia.com/zufang/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        }
        meta = {'test_key': 'crawl_from_lj_web_site'}
        return Request(url=url, meta=meta, headers=headers, callback=self.parse)

    # def start_requests(self):
    #     for numb_sz in range(1,40):
    #         url_sz = 'https://sz.lianjia.com/zufang/pg{}/#contentList'.format(str(numb_sz))
    #         yield scrapy.Request(url=url_sz, callback=self.parse)
    #     for numb_gz in range(1,40):
    #         url_gz = 'https://gz.lianjia.com/zufang/pg{}/#contentList'.format(str(numb_gz))
    #         yield scrapy.Request(url=url_gz, callback=self.parse)
    #     for numb_bj in range(1,40):
    #         url_bj = 'https://bj.lianjia.com/zufang/pg{}/#contentList'.format(str(numb_bj))
    #         yield scrapy.Request(url=url_bj, callback=self.parse)
    #     for numb_wh in range(1,40):
    #         url_wh = 'https://wh.lianjia.com/zufang/pg{}/#contentList'.format(str(numb_wh))
    #         yield scrapy.Request(url=url_wh, callback=self.parse)

    def parse(self, response):
        print('redis_key', self.redis_key)
        meta = response.meta
        print(meta['test_key'])
        item = LianjiaItem()
        infos = response.xpath('//div[@class="content__list--item"]')
        for info in infos:
            u_list = response.xpath('//*[@id="content"]/div[1]/p/a/@href').get().split('/') # //*[@id="content"]/div[1]/p/a
            base_url = u_list[0] + '//' + u_list[2]
            item['r_url'] = urljoin(base_url,info.xpath('a[@class="content__list--item--aside"]/@href').get())
            item['r_img_url'] = info.xpath('a[@class="content__list--item--aside"]/img/@data-src').get()
            item['r_title'] = info.xpath('div/p[contains(@class, "content__list--item--title")]/a/text()').get().strip()
            item['r_info'] = re.sub(r'\s','',''.join(info.xpath('div/p[contains(@class, "content__list--item--des")]//text()').getall()))
            item['r_city'] = info.xpath('//*[@id="content"]/div[1]/p/a/text()').get().split(' ')[-1][:2]
            item['r_locate'] = item['r_city']+ '-' +item['r_info'].split('/')[0]
            item['r_date'] = info.xpath('div[@class="content__list--item--main"]//span[@class="content__list--item--time oneline"]/text()').get()
            item['r_price'] = ''.join(info.xpath('div[@class="content__list--item--main"]/span[@class="content__list--item-price"]//text()').getall())
            item['r_tags'] = '/'.join([value for value in [val.strip() for val in info.xpath('div[@class="content__list--item--main"]/p[@class="content__list--item--bottom oneline"]//text()').getall()] if value != ''])
            print(item)
            yield item
