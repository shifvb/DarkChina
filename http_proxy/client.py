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

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from http_proxy.encrypt import encrypt
from http_proxy.async_IO import read_write

BUFFER_SIZE = 4096
local_addr = '127.0.0.1'
local_port = 12306
server_addr = '127.0.0.1'
server_port = 4444


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


if __name__ == '__main__':
    print('Client listening on {}:{}'.format(local_addr, local_port))
    client()
