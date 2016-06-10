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
PATH_LEN = 44
# codec_list = ['utf-8', 'gbk', 'gb2312']


def parse_head(head_str: bytes):
    method, path, protocol = head_str.split(b'\r\n')[0].split(b' ')
    # assert str(type(method)) == "<class 'bytes'>"
    # assert str(type(protocol)) == "<class 'bytes'>"
    # assert str(type(path)) == "<class 'bytes'>"
    method = method.decode()
    path = path.decode()
    protocol = protocol.decode()
    # assert str(type(method)) == "<class 'str'>"
    # assert str(type(path)) == "<class 'str'>"
    # assert str(type(protocol)) == "<class 'str'>"
    logging.info('[INFO] [{}] {:7} {:44} {}'.format(get_time_str(), method, short_str(path, PATH_LEN), protocol))
    logging.debug('[DEBUG] [{} in {} running threads]'.format(threading.current_thread().getName(), threading.active_count()))
    logging.debug(head_str)
    logging.debug('')
    return method, path, protocol


# def seq_decode(s: bytes, codec_list):
#     '''
#     decode bytes with multiple codec
#     '''
#     # todo: it's not workable ...
#     for codec in codec_list:
#         try:
#             return s.decode(encoding=codec)
#         except UnicodeDecodeError:
#             continue


# def testSeqDecode():
#     assert "sfje" == seq_decode("sfje".encode(encoding='utf-8'), codec_list)
#     assert "3dfgg" == seq_decode("3dfgg".encode(encoding='gbk'), codec_list)
#     assert "3dfgg" == seq_decode("3dfgg".encode(encoding='gb2312'), codec_list)


def testkParseHead():
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    for i in range(10):
        parse_head(b'GET http://www.google.com/ HTTP/1.1\r\nHost: www.google.com\r\n\r\n')


if __name__ == '__main__':
    testkParseHead()
    # testSeqDecode()
