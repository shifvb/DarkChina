# The MIT License (MIT)
#
# Copyright shifvb 2015
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
import getopt


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from http_proxy.tools.encrypt import encrypt
from http_proxy.tools.async_IO import read_write

BUFFER_SIZE = 4096
local_addr = ''
local_port = 0
server_addr = ''
server_port = 0
__version__ = 'DarkChina 0.9.0'


def handle_request(client_sock):
    # receive data from client(i.e. browser)
    head_data = client_sock.recv(BUFFER_SIZE)
    if not head_data:
        client_sock.close()
        return

    # encrypt data
    encrypted_data = encrypt(head_data)

    # send encrypted data to server
    target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_sock.connect((server_addr, server_port))
    target_sock.send(encrypted_data)

    # async communication
    read_write(client_sock, target_sock)

    # close socket
    client_sock.close()
    target_sock.close()


def client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.bind((local_addr, local_port))
    client_sock.listen(5)
    while True:
        conn, addr = client_sock.accept()
        t = threading.Thread(target=handle_request, args=(conn,))
        t.start()


def parse_args():
    global local_addr
    global local_port
    global server_addr
    global server_port
    args_dict, args_left = getopt.getopt(sys.argv[1:], 'hvl:b:s:p:', [])

    # get values
    for k, v in args_dict:
        if k == '-h':
            usage()
            sys.exit(0)
        elif k == '-v':
            print(__version__)
            sys.exit(0)
        elif k == '-l':
            local_addr = v
        elif k == '-b':
            local_port = int(v)
        elif k == '-s':
            server_addr = v
        elif k == '-p':
            server_port = int(v)

    # get default values
    if not local_addr:
        local_addr = '127.0.0.1'
    if not local_port:
        local_port = 12306
    if not server_addr:
        print('\nServer address required!')
        usage()
        sys.exit(1)
    if not server_port:
        server_port = 2333


def usage():
    print()
    print('DarkChina client_side help document')
    print('Usage: python3 ./server.py [option [value]]...')
    print('Options:')
    print('\t-h                         show this help document')
    print('\t-l local_addr              local binding address, default: 127.0.0.1')
    print('\t-b local_port              local binding port, default: 12306')
    print('\t-s server_addr             server address')
    print('\t-p server_port             server port, default: 2333')


if __name__ == '__main__':
    parse_args()
    print('Client listening on {}:{}'.format(local_addr, local_port))
    client()
