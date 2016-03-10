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
import re
import socket
import threading
import getopt


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from http_proxy.tools.decrypt import decrypt
from http_proxy.tools.async_IO import read_write
from http_proxy.tools.parse_head import parse_head
from http_proxy.utils import usage

BUFFER_SIZE = 4096
server_addr = ''
server_port = 0
is_local = False
__version__ = 'DarkChina 0.9.1'


def handle_request(client_sock):
    # receive data from client
    head_str = decrypt(client_sock.recv(BUFFER_SIZE)).decode()

    # analyze data
    method, path, protocol = parse_head(head_str, verbose=2)
    target_sock = _get_target_sock(method, path, client_sock, head_str)

    # async communication
    read_write(client_sock, target_sock)

    # close socket
    client_sock.close()
    target_sock.close()


#
# get the server socket required by client
# example:
#    the path of www.googleapis.com:443 will result in TCP socket of googleapis.com by port 443
#    the path of http://example.com/ will result in TCP socket of example.com by port 80
#
def _get_target_sock(method: str, path: str, client_sock, head_str: str):
    target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if method == 'CONNECT':
        host, port = path.split(':')
        port = int(port)
        target_sock.connect((host, port))
        client_sock.send('HTTP/1.1 200 Connection established\r\n\r\n'.encode())
    else:
        m = re.match(r'http://(.*?)/.*', path)
        host = m.group(1)
        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        target_sock.connect((host, port))
        target_sock.send(head_str.encode())
    return target_sock


def server():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.bind((server_addr, server_port))
    client_sock.listen(5)
    while True:
        conn, addr = client_sock.accept()
        t = threading.Thread(target=handle_request, args=(conn,))
        t.start()


def parse_args():
    global server_addr
    global server_port
    args_dict, args_left = getopt.getopt(sys.argv[1:], 'hVs:p:', [])

    # set values
    for k, v in args_dict:
        if k == '-h':
            usage(is_local)
            sys.exit(0)
        elif k == '-V':
            print(__version__)
            sys.exit(0)
        elif k == '-s':
            server_addr = v
        elif k == '-p':
            server_port = int(v)

    # set default values
    if not server_addr:
        server_addr = '0.0.0.0'
    if not server_port:
        server_port = 2333





if __name__ == '__main__':
    parse_args()
    print('Server listening on {}:{}'.format(server_addr, server_port))
    server()
