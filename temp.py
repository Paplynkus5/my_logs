import time

print('_'.join(map(str, time.localtime()[0:3])) + ' ' + ':'.join(map(str, time.localtime()[3:6])))