import dns.resolver

my_resolver = dns.resolver.Resolver()
my_resolver.timeout = 1
my_resolver.lifetime = 1

my_resolver_test = dns.resolver.Resolver()
my_resolver_test.timeout = 1
my_resolver_test.lifetime = 1

# 8.8.8.8 is Google's public DNS server
my_resolver.nameservers = ['8.8.8.8']
answer = my_resolver.query('google.com', 'A')

my_resolver_test.nameservers = ['1.1.1.1']
answer_test = my_resolver_test.query('google.com', 'A')

collection_main = []
collection_test = []

for data in answer:
    collection_main.append(data.to_text())

print '-------------------------------------------'

for data in answer_test:
    collection_test.append(data.to_text())

if collection_main.sort() == collection_test.sort():
    print 'Yeap'
# print "canonical_name: ", answer.canonical_name
# print "Expiration: ", answer.expiration
# print "QNAME: ", answer.qname
# print "RDCLASS: ", answer.rdclass
# print "RDTYPE: ",answer.rdtype
# print "RESPONSE: ", answer.response
# print "RRSET: ", dir(answer.rrset)
#
# print answer.rrset[0]

# import dns.resolver
#
#
# def get_domain(domain):
#     types = [
#         'A',
#         'TXT',
#         'CNAME',
#         'NS',
#     ]
#     for type in types:
#         try:
#             response = dns.resolver.query(domain, type)
#             for data in response:
#                 print type, "-", data.to_text()
#         except Exception as err:
#             print(err)
#
#
# if __name__ == '__main__':
#     get_domain('stackoverflow.com')
