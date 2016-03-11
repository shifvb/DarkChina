import datetime
import threading


#
# parse http head, print debug message according to verbose level
#    verbose level 2:
#        print all brief message and original data
#    verbose level 1:
#        print only brief message
#    verbose level 0:
#        print nothing
# return a tuple of (http_method_str, http_path_str, http_protocol_str)
#
# example:
#    if head is str
#        'GET http://www.google.com/ HTTP/1.1\r\nHost: www.google.com\r\n\r\n'
#    then returns tuple
#        ('GET', 'http://www.google.com/', 'HTTP/1.1')
#
def parse_head(head_str: str, verbose: int):
    method, path, protocol = head_str.split('\r\n')[0].split(' ')
    if verbose < 0 or verbose > 2:
        raise Exception('unknown verbose level: {}'.format(verbose))
    if verbose == 0:    # no message
        pass
    elif verbose == 1:  # brief message only
        print('[INFO] [{}] {} {} {}'.format(datetime.datetime.now(), method, path, protocol), end=' ')
        print('[{} in {} running threads]'.format(threading.current_thread().getName(), threading.active_count()))
    elif verbose == 2:  # brief message and original data
        print('[INFO] [{}] {} {} {}'.format(datetime.datetime.now(), method, path, protocol), end=' ')
        print('[{} in {} running threads]'.format(threading.current_thread().getName(), threading.active_count()))
        print(head_str)
    return method, path, protocol


def test():
    for i in range(10):
        parse_head('GET http://www.google.com/ HTTP/1.1\r\nHost: www.google.com\r\n\r\n', 2)


if __name__ == '__main__':
    test()