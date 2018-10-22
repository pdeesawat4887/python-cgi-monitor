import time
import re

ip_str = "23.34.45.45"

def ipFormatChk(ip_str):
    if len(ip_str.split())== 1:
        ipList = ip_str.split('.')
        if len(ipList) == 4:
            for i, item in enumerate(ipList):
                try:
                    ipList[i] = int(item)
                except:
                    return None
                if not isinstance(ipList[i], int):
                    flag = False
            if max(ipList) < 256:
                return ip_str
            else:
                return None
        else:
            return None
    else:
        return None

def verify_ip(ip):
    ip_candidates = re.findall(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                               r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                               r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                               r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

    if ip_candidates.__len__() != 0:
        return '.'.join(ip_candidates[0])
    else:
        return None

# t_s1=time.time()
# h1 = ipFormatChk(ip_str)
# e_s1=time.time()
#
# t_s2=time.time()
# h2 = verify_ip(ip_str)
# e_s2=time.time()
#
# print "h1: ", (e_s1-t_s1)*1000, h1
# print "h2: ", (e_s2-t_s2)*1000, h2

def verify_number(number):
    try:
        return number if re.match("^[0-9]*$", number) else None
    except:
        return None


def verify_text(text):
    try:
        return text if re.match("^[a-zA-Z0-9_-]*$", text) else None
    except:
        return None


print verify_text(None)