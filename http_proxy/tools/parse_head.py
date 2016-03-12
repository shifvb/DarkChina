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
import logging
from http_proxy.utils import get_time_str
from http_proxy.utils import short_str

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


def parse_head(head_str: str):
    method, path, protocol = head_str.split('\r\n')[0].split(' ')
    logging.info('[{}] {:7} {:35} {}'.format(get_time_str(), method, short_str(path, PATH_LEN), protocol))
    logging.debug(
            '[{}] {} {} {}'.format(get_time_str(), method, path, protocol) + ' [{} in {} running threads]\n'.format(
                threading.current_thread().getName(), threading.active_count()) + head_str)
    return method, path, protocol


def test():
    import logging
    logging.basicConfig(level=logging.INFO)
    for i in range(10):
        parse_head('GET http://www.google.com/ HTTP/1.1\r\nHost: www.google.com\r\n\r\n')


if __name__ == '__main__':
    test()
