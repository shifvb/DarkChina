#!/usr/bin/env python3
#
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

import os
import sys
import socket
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from http_proxy.tools.encrypt import encrypt
from http_proxy.tools.async_IO import read_write
from http_proxy.tools.parse_head import parse_head
from http_proxy.utils import parse_args
from http_proxy.utils import check_ver
from http_proxy.utils import get_pretty_str
from http_proxy.utils import get_time_str

BUFFER_SIZE = 4096
is_local = True
__version__ = 'DarkChina 0.9.1'


def handle_request(client_sock, server_addr: str, server_port: int, verbose: int):
    try:
        # receive data from client(i.e. browser)
        head_data = client_sock.recv(BUFFER_SIZE)
        if not head_data:
            client_sock.close()
            return
        parse_head(head_data.decode(), verbose=verbose)  # show debug message
        encrypted_data = encrypt(head_data)  # encrypt data
        target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # send encrypted data to server
        target_sock.connect((server_addr, server_port))
        target_sock.send(encrypted_data)
        read_write(client_sock, target_sock)  # async communication
        target_sock.close()  # close socket
    except TimeoutError:
        print('[WARNING] [{}] {:7} {} time out.'.format(get_time_str(), "link to", get_pretty_str(server_addr, 31)))
    except ConnectionResetError:
        print('[WARNING] [{}] {:7} {} reseted.'.format(get_time_str(), "link to", get_pretty_str(server_addr, 32)))
    except ConnectionAbortedError:
        print('[WARNING] [{}] {:7} {} aborted by client.'.format(get_time_str(), "link to",
                                                                 get_pretty_str(server_addr, 21)))
    except ConnectionRefusedError:
        print('[WARNING] [{}] {:7} {} was refused.'.format(get_time_str(), "link to", get_pretty_str(server_addr, 28)))
    finally:
        client_sock.close()


def client(server_addr: str, server_port: int, local_addr: str, local_port: int, verbose: int):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.bind((local_addr, local_port))
    client_sock.listen(5)
    while True:
        conn, addr = client_sock.accept()
        t = threading.Thread(target=handle_request, args=(conn, server_addr, server_port, verbose))
        t.daemon = True
        t.start()


if __name__ == '__main__':
    check_ver()
    d = parse_args(is_local, __version__)
    print('Target server: {}:{}'.format(d["server_addr"], d["server_port"]))
    print('Client listening on {}:{}'.format(d["local_addr"], d["local_port"]))
    client(**d)
