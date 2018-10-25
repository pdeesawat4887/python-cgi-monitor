import re

def checkMAC(s):
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", s.lower()):
        return s
    else:
        return "invalid mac-address format"



print checkMAC("AA:BB:CC:DD:EE:FF")
print checkMAC("00-11-22-33-44-66")
print checkMAC("1 2 3 4 5 6 7 8 9 a b c")
print checkMAC("This is not a mac")