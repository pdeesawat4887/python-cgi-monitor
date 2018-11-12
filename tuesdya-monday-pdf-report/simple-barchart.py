

label = ['Active', 'Inactive', 'Idle']
value = [50, 25, 25]
color = ['green', 'red', 'gray']

label.extend(color)

print label

from random import randint
print(randint(0, 9))


banner = "SELECT {extra}"
test = "Hello {hi}".format(hi=banner.format(extra='jjjjjk'))

print test