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


def usage(is_local: bool) -> None:
    """show usage doc."""
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
        print('\t-v verbose level           verbose level 0->2, default: 0')
    else:
        print('\nUsage: python3 ./server.py [option [value]]...\n')
        print('DarkChina server_side help document\n')
        print('Options:')
        print('\t-h                          show this help document')
        print('\t-s server_addr              server address, default: 0.0.0.0')
        print('\t-p server_port              server port, default: 2333')
        print('\t-V version                  show current version')
        print('\t-v verbose level            verbose level 0->2, default: 0')

def parse_args(is_local: bool, version: str) -> dict:
    """parse args from command line and return config dict."""
    config_dict = {}
    if is_local:  # is_local is True, local side
        args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVl:b:s:p:v:', [])
        # set values
        for k, v in args_dict:
            if k == '-h':
                usage(is_local)
                sys.exit(0)
            elif k == '-V':
                print(version)
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

        # set default values
        config_dict.setdefault("local_addr", '127.0.0.1')
        config_dict.setdefault("local_port", 12306)
        if not config_dict.get("server_addr", None):
            print('\nServer address required!')
            usage(is_local)
            sys.exit(1)
        config_dict.setdefault("server_port", 2333)
        config_dict.setdefault("verbose", 0)

    else:  # is_local is False, server side
        args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVs:p:v:', [])
        # set values
        for k, v in args_dict:
            if k == '-h':
                usage(is_local)
                sys.exit(0)
            elif k == '-V':
                print(version)
                sys.exit(0)
            elif k == '-s':
                config_dict["server_addr"] = v
            elif k == '-p':
                config_dict["server_port"] = int(v)
            elif k == '-v':
                config_dict["verbose"] = int(v)

        # set default values
        config_dict.setdefault("server_addr", '0.0.0.0')
        config_dict.setdefault("server_port", 2333)
        config_dict.setdefault("verbose", 0)
    return config_dict


def check_ver():
    '''check compatibility'''
    if not sys.version >= '3.2':
        print('python 3.3+ required!')
        sys.exit(0)


if __name__ == '__main__':
    result = parse_args(False, 'test version')
    print(result)
