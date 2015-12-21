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
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from http_proxy.decrypt import decrypt
from http_proxy.async_IO import read_write

BUFFER_SIZE = 4096
listen_addr = '127.0.0.1'
listen_port = 4444


def handle_request(client_sock):
    # receive data from client
    head_str = decrypt(client_sock.recv(BUFFER_SIZE)).decode()

    # analyze data
    method, path, protocol = head_str.split('\r\n')[0].split(' ')
    print('[INFO] [{}] {} {} {}'.format(datetime.datetime.now(), method, path, protocol), end=' ')  # debug
    print('[{} in {} running threads]'.format(threading.current_thread().getName(), threading.active_count()))
    target_sock = _get_target_sock(method, path, client_sock, head_str)

    # async communication
    read_write(client_sock, target_sock)

    # close socket
    client_sock.close()
    target_sock.close()


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
        target_sock.connect((host, 80))
        target_sock.send(head_str.encode())
    return target_sock


def server():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.bind((listen_addr, listen_port))
    client_sock.listen(5)
    while True:
        conn, addr = client_sock.accept()
        t = threading.Thread(target=handle_request, args=(conn,))
        t.start()


if __name__ == '__main__':
    print('Server listening on {}:{}'.format(listen_addr, listen_port))
    server()
