# The MIT License (MIT)
#
# Copyright shifvb 2015-2016
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import threading
from http_proxy.utils import get_time_str
from http_proxy.utils import get_pretty_str

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
PATH_LEN = 35


def parse_head(head_str: str, verbose: int):
    method, path, protocol = head_str.split('\r\n')[0].split(' ')
    if verbose == 0:  # no message
        pass
    elif verbose == 1:  # brief message only
        print('[INFO] [{}] {:7} {:35} {}'.format(get_time_str(), method, get_pretty_str(path, PATH_LEN), protocol))
    elif verbose == 2:  # brief message and original data
        print('[INFO] [{}] {} {} {}'.format(get_time_str(), method, path, protocol), end=' ')
        print('[{} in {} running threads]'.format(threading.current_thread().getName(), threading.active_count()))
        print(head_str)
    return method, path, protocol


def test():
    for i in range(10):
        parse_head('GET http://www.google.com/ HTTP/1.1\r\nHost: www.google.com\r\n\r\n', 2)


if __name__ == '__main__':
    test()
