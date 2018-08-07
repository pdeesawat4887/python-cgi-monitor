import pythonwhois
import urlparse
from pip._vendor.colorama import Fore, Style
import urllib
import requests
import time


class Shopping:
    website_list = []

    def __init__(self):
        self.get_shopping_website()
        pass

    def get_shopping_website(self, file='conf/shopping_conf.txt'):
        with open(file) as f:
            for line in f:
                obj = line.rstrip()
                self.website_list.append(obj)

    def get_whois(self, url_website):
        parse_obj = urlparse.urlparse(url_website)
        try:
            result = pythonwhois.get_whois(parse_obj.netloc)

            if 'Prohibited' in result['status'][0]:
                status = 'unknow'
            else:
                status = result['status'][0]

            expire_date = result['expiration_date'][0].date()
            # return result
        except Exception as error:
            print 'Error: ', error
            status = "Cannot Found in Whois"
            expire_date = "Cannot Found in Whois"

        # try:
        #     if 'Prohibited' in result['status'][0]:
        #         status = 'unknow'
        #     else:
        #         status = result['status'][0]
        #
        #     expire_date = result['expiration_date'][0].date()
        # except:
        #     status = "Cannot Found in Whois"
        #     expire_date = "Cannot Found in Whois"

        return status, expire_date

    def usage_result(self, result):

        try:
            if 'Prohibited' in result['status'][0]:
                status = 'unknow'
            else:
                status = result['status'][0]

            expire_date = result['expiration_date'][0].date()
        except:
            status = "Cannot Found in Whois"
            expire_date = "Cannot Found in Whois"

        return status, expire_date

    def checkStatusHTTPS(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
        try:
            res_https = requests.get(url, headers=headers)
            status = res_https.status_code
            res_https.close()
        except Exception as ex:
            status = 'Could not connect to page.'

        return status

    def main(self):
        pass


shopping = Shopping()
# shopping.get_shopping_website()
print shopping.website_list

# # For test
# res = bella.get_whois('amazon.com')
# print res['status'][0]

for i in shopping.website_list:
    url = i.replace('www.', "")
    print "-------------------->  ", Fore.GREEN, url, Style.RESET_ALL

    status, expire_date = shopping.get_whois(url)
    # status, expire_date = shopping.usage_result(result)

    print "Status: ", status
    print "Expired Date: ", expire_date

    print shopping.checkStatusHTTPS(i)

    print "-----------------/--------------------/--------------"

# result = bella.get_whois('shopee.co.th')
# print result, '\n\n'
# print result['status'][0]
# print result['creation_date'][0]
# print result['updated_date'][0]
# print result['expiration_date'][0]
