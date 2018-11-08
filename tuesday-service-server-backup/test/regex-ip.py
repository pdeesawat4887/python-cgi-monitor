import re

ip = "172.1.30.172"

ip_candidates = re.findall(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

# ip_candidates = re.findall(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip)
# ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$

# print ip_candidates
# print type(ip_candidates)
# print ip_candidates

# if ip_candidates.__len__() != 0:
#     print '.'.join(ip_candidates[0])
# else:
#     print "Incorrect IP"


number = "3222"
import re
# print "Valid" if re.match("^[a-zA-Z0-9_-]*$", word) else "Invalid"

print number if re.match("^[0-9]*$", number) else None