import scrapy


class LawyerUrlSpider(scrapy.Spider):
    name = 'lawyer_url'
    allowed_domains = ['members.calbar.ca.gov']
    # start_urls = ['http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=a&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=']
    # la_url = 'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=sm&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=LA&LegalSpecialty=&LanguageSpoken='

    def start_requests(self):
        alphabet='abcdefghijklmnopqrstuvwxyz'
        
        
        for letter1 in alphabet:
            for letter2 in alphabet:
                letters = letter1+letter2
                la_url = f'http://members.calbar.ca.gov/fal/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName={letters}&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=&State=&Zip=&District=&County=LA&LegalSpecialty=&LanguageSpoken='

                yield scrapy.Request(la_url, self.parse)

    # stopping notes: able to parse first td of row but need to adjust selector to isolate name 

    def parse(self, response):
        rows=response.css('.rowASRLodd')
        for row in rows:
            # get info from first cell which has name and url
            cells=row.css('td')
            # extract text for name
            name=cells[0].css('* ::text').extract()
            # text for name has a lot of white space and returns as list. loop through list with .join()
            name = ''.join(name).strip()
            # attrib (see scrapy selector docs) to extract url
            url=cells[0].css('a').attrib['href']
            # obtain active members
            status=cells[1].css('* ::text').extract()
            status=''.join(status).strip()
            #this is a clause to bypass any attorneys who are disbarred or inactive
            if status != 'Active':
                continue
            #yielding only active members along with name and url to their contact page
            root_url='http://members.calbar.ca.gov'
            yield {
                'name':name,
                'url' : root_url+url,
                'status':status,
            }

            # root url for member information: http://members.calbar.ca.gov
        