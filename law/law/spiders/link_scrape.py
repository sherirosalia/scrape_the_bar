import scrapy
import pandas as pd


class LinkScrapeSpider(scrapy.Spider):
    name = 'link_scrape'
    allowed_domains = ['members.calbar.ca.gov']
    # start_urls = ['http://members.calbar.ca.gov/fal/Licensee/Detail/228348', 'http://members.calbar.ca.gov/fal/Licensee/Detail/293345', 'http://members.calbar.ca.gov/fal/Licensee/Detail/33290']

    def start_requests(self):
        df=pd.read_csv('la_lawyers.csv')
        for i,lawyer in df.iterrows():
            link=lawyer['url']               

            yield scrapy.Request(link, self.parse, meta={'name':lawyer['name']})    

    def parse(self, response):
        email_id=response.css('#content-main>.body-text>style').re_first(r'(#e[0-9]+){display:inline;}')
        email_text=response.css(email_id + ' ::text').extract()
        email_text = ''.join(email_text).strip()
        # moduleMemberDetail
        member_info=response.css('#moduleMemberDetail>div>p::text').extract()
        processed_info=[]
        processed_dict={}
        for info in member_info:
            info=info.strip()
            if info != '' and (':' in info):
                name, value = info.split(':', 1)
                processed_dict[name]=value.strip()
            processed_info.append(info)
        processed_dict['Email']=email_text
        # processed_dict['processed_info']=processed_info
        name=response.meta['name'].split()
        name=' '.join(name)
        processed_dict['Name']=name

        # processed_dict['Email_id']=email_id

        yield processed_dict
        # yield {
        #     'email_id':email_id,
        #     'email_text':email_text,
        #     'processed_info':processed_info,
        #     # 'member_info':member_info,
        #     # 'url' : root_url+url,
        #     # 'status':status,
        #  }

        # for selection in selections:
        #     # #e9{display:inline;}
        #     style = selection.get()
        #     style.re()

        #     yield {
        #         'selection':selection.get(),
        #         # 'url' : root_url+url,
        #         # 'status':status,
        #     }

        
