#coding:utf-8
import scrapy
from zhihu.items import zhihuItem
from scrapy import Request
import sqlite3


class ZhihuSpider(scrapy.Spider):
    
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        'http://www.zhihu.com/question/36983299',
        'http://www.zhihu.com/question/37062763',
        'http://www.zhihu.com/question/30489442',
        'http://www.zhihu.com/question/28782497'
        
    ]
    
    conn = sqlite3.connect("URLTITLE.db")
    
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS url_title(id integer primary key AUTOINCREMENT, url text, title text, code text)')
    c.execute('CREATE TABLE IF NOT EXISTS urls(url text primary key)')
    
    id = 0
    
    def parse(self, response):
        #print type(response.url)
        #item = zhihuItem
        if response.url.strip() in self.start_urls:
            self.c.execute('SELECT * FROM urls WHERE url = (?)',(response.url.strip(),))
            lines = self.c.fetchall()
            if len(lines) == 0:
                self.c.execute("INSERT INTO url_title (url, title, code) VALUES (?, ?, ?)", (response.url.strip(), response.xpath('//title/text()').extract()[0].strip(), response.xpath('//html').extract()[0]))
                self.c.execute("INSERT INTO urls VALUES (?)", (response.url.strip(), ))
        else:
            self.c.execute("INSERT INTO url_title (url, title, code) VALUES (?, ?, ?)", (response.url.strip(), response.xpath('//title/text()').extract()[0].strip(), response.xpath('//html').extract()[0]))
            self.c.execute("INSERT INTO urls VALUES (?)", (response.url.strip(), ))
        
        
        '''title = response.xpath('//title/text()').extract()[0].strip()
        title += '\n'

        self.file.write(title)'''
        
        self.conn.commit()
        #item['link'] = response.url 
        newurls = response.xpath('//ul/li/a').re('question_link.*?="(.*?)">')
        
        for i in range(len(newurls)):
            newurls[i] = ('http://www.zhihu.com' + newurls[i])
            
        for new_url in newurls:
                self.c.execute('SELECT * FROM urls WHERE url = (?)',(new_url,))
                lines = self.c.fetchall()
                if len(lines) == 0:
                    yield Request(url = new_url, callback = self.parse, )
        
        
    
    
