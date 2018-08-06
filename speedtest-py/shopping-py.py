import pythonwhois
import urlparse
from pip._vendor.colorama import Fore, Style
import urllib
import requests
import time


class Shopping:
    website_list = []

    def __init__(self):
        pass

    def get_shopping_website(self, file='conf/shopping_conf.txt'):
        with open(file) as f:
            for line in f:
                obj = line.rstrip()
                self.website_list.append(obj)
                # parse_obj = urlparse.urlparse(obj)
                # # print parse_obj
                # self.website_list.append(parse_obj.netloc)

    def get_whois(self, url_website):
        parse_obj = urlparse.urlparse(url_website)
        try:
            result = pythonwhois.get_whois(parse_obj.netloc)
            return result
        except:
            print Fore.RED + "Please use correct name without http(s)://" + Style.RESET_ALL

    def usage_result(self, result):

        if 'Prohibited' in result['status'][0]:
            status = 'unknow'
        else:
            status = result['status'][0]

        expire_date = result['expiration_date'][0]

        return status, expire_date

    def get_webpage(self, url):
        try:
            res_https = urllib.urlopen(url)
            code = res_https.getcode()
            # reason = httplib.responses[status]
            res_https.close()

            # status = self.tool.check_code(code)

        except Exception as ex:
            code = 'Could not connect to page. at Class'
        return code

    def checkStatusHTTPS(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
        try:
            res_https = requests.get(url, headers=headers)
            self.status = res_https.status_code
            self.reason = res_https.reason
            res_https.close()
        except Exception as ex:
            self.status = 'Could not connect to page.'
            self.reason = 'Could not connect to page.'

        return self.status, self.reason


shopping = Shopping()
shopping.get_shopping_website()
print shopping.website_list

# # For test
# res = bella.get_whois('amazon.com')
# print res['status'][0]

for i in shopping.website_list:
    url = i.replace('www.', "")
    print "-------------------->  ", Fore.GREEN, url, Style.RESET_ALL
    result = shopping.get_whois(url)
    status, expire_date = shopping.usage_result(result)
    print "Status: ", status
    print "Expired Date: ", expire_date, expire_date.date(), expire_date.time()
    # print urllib.urlopen(i).getcode()
    # print shopping.get_webpage(i)
    print shopping.checkStatusHTTPS(i)
    print "-----------------/--------------------/--------------"

# result = bella.get_whois('shopee.co.th')
# print result, '\n\n'
# print result['status'][0]
# print result['creation_date'][0]
# print result['updated_date'][0]
# print result['expiration_date'][0]
