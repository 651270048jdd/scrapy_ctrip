# -*- coding: utf-8 -*-
import scrapy
import json
from ctrip.items import CtripItem

class BoatSpider(scrapy.Spider):
    name = 'boat'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://cruise.ctrip.com/search/s2a25o5.html']


    def parse(self, response):
        boats = response.xpath('//*[@class="route_list "]')
        for each_boat in boats:
            post={}
            post['Client.SellerID']=each_boat.xpath('./@data-ubt-sellerid').extract()[0]
            post['VoyaID'] = each_boat.xpath('./@data-ubt-voyaid').extract()[0]
            post['SailingID'] = each_boat.xpath('./@data-ubt-sailingid').extract()[0]
            #item = CtripItem()
            #item['name'] = each_boat.xpath('./a/div[@class="route_info"]/h2[@class="route_title"]/text()').extract()[0]
            #item['href'] = each_boat.xpath('./a/@href').extract()[0]#链接
            #item['route'] = each_boat.xpath('./a/div[@class="route_side"]/div[@class="route_category"]/text()').extract()[0]#航线
            #item['route_col'] = each_boat.xpath('./a/div[@class="route_info"]/p[@class="route_info_col"]/span[@class="txt_link_strong"]/text()').extract()[0]
            #item['supplier'] = each_boat.xpath('./a/div[@class="route_info"]/div[@class="route_supplier"]/text()').extract()[0]#链接
            #data_ubt_sellerid=each_boat.xpath('./@')
            #print(data_ubt_sellerid)
            yield self.parse_page(post)
            #yield item


    #post数据请求
    def parse_page(self,post):
        post['Client.PromotionCode']=post['PackageID']=''
        FormRequest = scrapy.http.FormRequest(
            url='http://cruise.ctrip.com/Cruise-Booking-Online/CrystalProject/Booking/GetSailingDetailV3',
            # header={
            #     'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,likeGecko) Chrome/57.0.2987.133 Safari/537.36 X-Requested-With:XMLHttpRequest',
            #     'Origin': 'http: // cruise.ctrip.com Pragma:no-cache'
            # },
            formdata=post,
            callback=self.get_price  # 这是指定回调函数，就是发送request之后返回的结果到哪个函数来处理。
        )
        return  FormRequest



    def get_price(self,response):
        reponseJosn=response.body
        item = CtripItem()
        item['name'] =reponseJosn.decode()
        yield item
        # for each_json in reponseJosn:
        # print(each_json)