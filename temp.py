import time

while True:
    print('archived_logs\\merged\\' + '-'.join(map(str, time.localtime()[0:3])) + ' ' + ''.join(f'{time_element:02s}' for time_element in map(str, time.localtime()[3:6])) + '.log')
    print('archived_logs\\merged\\' + '-'.join(f'{time_element:02d}' for time_element in time.localtime()[0:3]) + ' ' + ''.join(f'{time_element:02d}' for time_element in time.localtime()[3:6]) + '.log')
    time.sleep(1)