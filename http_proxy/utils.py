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

import getopt
import sys
import time
import logging

time_fmt = '%y-%m-%d %H:%M:%S'


def usage(is_local: bool) -> None:
    """
    show usage doc.
    about verbose level: (according to logging module)
         <=1: CRITICAL, ERROR, WARNING, INFO, DEBUG
           2: CRITICAL, ERROR, WARNING, INFO
           3: CRITICAL, ERROR, WARNING
           4: CRITICAL, ERROR
           5: CRITICAL,
          >5: no message
    """
    if is_local:
        print()
        print('DarkChina client_side help document')
        print('Usage: python3 ./server.py [option [value]]...')
        print('Options:')
        print('\t-h                         show this help document')
        print('\t-l local_addr              local binding address, default: 127.0.0.1')
        print('\t-b local_port              local binding port, default: 12306')
        print('\t-s server_addr             server address')
        print('\t-p server_port             server port, default: 2333')
        print('\t-V version                 show current version')
        print('\t-v verbose level           verbose level, default: 2')
    else:
        print('\nUsage: python3 ./server.py [option [value]]...\n')
        print('DarkChina server_side help document\n')
        print('Options:')
        print('\t-h                          show this help document')
        print('\t-s server_addr              server address, default: 0.0.0.0')
        print('\t-p server_port              server port, default: 2333')
        print('\t-V version                  show current version')
        print('\t-v verbose level            verbose level, default: 2')


def parse_args(is_local: bool, version: tuple) -> dict:
    """parse args from command line and return config dict."""
    config_dict = {}
    if is_local:  # is_local is True, local side
        args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVl:b:s:p:v:', [])
        for k, v in args_dict:
            if k == '-h':
                usage(is_local)
                sys.exit(0)
            elif k == '-V':
                print('DarkChina {}.{}.{}'.format(*version))
                sys.exit(0)
            elif k == '-l':
                config_dict["local_addr"] = v
            elif k == '-b':
                config_dict["local_port"] = int(v)
            elif k == '-s':
                config_dict["server_addr"] = v
            elif k == '-p':
                config_dict["server_port"] = int(v)
            elif k == '-v':
                config_dict["verbose"] = int(v)

        config_dict.setdefault("local_addr", '127.0.0.1')
        config_dict.setdefault("local_port", 12306)
        if not config_dict.get("server_addr", None):
            print('\nServer address required!')
            usage(is_local)
            sys.exit(1)
        config_dict.setdefault("server_port", 2333)

    else:  # is_local is False, server side
        args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVs:p:v:', [])
        for k, v in args_dict:
            if k == '-h':
                usage(is_local)
                sys.exit(0)
            elif k == '-V':
                print('DarkChina {}.{}.{}'.format(*version))
                sys.exit(0)
            elif k == '-s':
                config_dict["server_addr"] = v
            elif k == '-p':
                config_dict["server_port"] = int(v)
            elif k == '-v':
                config_dict["verbose"] = int(v)

        config_dict.setdefault("server_addr", '0.0.0.0')
        config_dict.setdefault("server_port", 2333)

    # common config
    config_dict.setdefault("verbose", 2)
    logging.basicConfig(level=config_dict["verbose"] * 10, format='[%(levelname)s] %(message)s')
    config_dict.pop("verbose")
    return config_dict


def check_ver():
    """check compatibility"""
    if not sys.version >= '3.2':
        print('python 3.2+ required!')
        sys.exit(0)


def short_str(s: str, length=35) -> str:
    """return a copy of s. If the length of s > length, return part of it."""
    if len(s) > length:
        return s[:length - 3] + '...'
    else:
        return s


def get_time_str():
    """return current time str in chinese style."""
    return time.strftime(time_fmt)


if __name__ == '__main__':
    pass
