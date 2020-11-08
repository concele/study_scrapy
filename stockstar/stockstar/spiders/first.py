import scrapy
from selenium import webdriver
from stockstar.items import StockstarItem
#网易新闻爬取

class FirstSpider(scrapy.Spider):
    name = 'first'
    #allowed_domains = ['www.baidu.com/']
    start_urls = ['https://news.163.com/']
    models_urls = []
    def __init__(self):
        self.bro = webdriver.Edge(executable_path='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe')
    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        #5个模块
        alist = [3,4,6,7,8]

        for index in alist:
            #对应详情页网页链接
            model_url = li_list[index].xpath('./a/@href').extract_first()
            self.models_urls.append(model_url)
            #对每个模块url发起请求
            for url in self.models_urls:
                yield scrapy.Request(url,callback=self.parse_model)

    #解析每个板块页面中对应新闻标题及详情页url(动态加载)
    def parse_model(self,response):
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item = StockstarItem()
            item['title'] = title
            #对新闻详情页url发起请求
            yield scrapy.Request(url=new_detail_url,callback=self.parse_detail,meta={'item':item})

    #解析新闻内容
    def parse_detail(self,response):
        content = response.xpath('//*[@id="endText"]//text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content
        yield item

    def closed(self,spider):
        print('结束')
        self.bro.quit()