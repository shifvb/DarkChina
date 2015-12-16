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


import socket
import threading
import re

BUFFER_SIZE = 4096
local_addr = '127.0.0.1'
local_port = 4444


def handle_request(client):
    head_raw = client.recv(BUFFER_SIZE)
    if not head_raw:
        client.close()
        return
    head_str = head_raw.decode()
    head_list = head_str.split('\r\n')
    method, path, protocol = head_list[0].split(' ')

    print('[INFO] {} {} {}'.format(method, path, protocol), end=' ')  # debug
    print('[{} in {} running threads]'.format(threading.current_thread().getName(), threading.active_count()))
    # print(head_list)

    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    filtered_head = _filter_head(head_list)
    if method == 'CONNECT':
        host, port = path.split(':')
        port = int(port)
        target.connect((host, port))
        client.send('HTTP/1.1 200 Connection established\r\n\r\n'.encode())
    else:
        m = re.match(r'http://(.*?)/.*', path)
        host = m.group(1)
        target.connect((host, 80))
        target.send(filtered_head.encode())
    _read_write(client, target)
    client.close()


def _read_write(client, target):
    import select
    time_out_max = 20
    socs = [client, target]
    count = 0
    while 1:
        count += 1
        (recv, _, error) = select.select(socs, [], socs, 3)
        if error:
            break
        if recv:
            for in_ in recv:
                data = in_.recv(8192)
                if in_ is client:
                    out = target
                else:
                    out = client
                if data:
                    out.send(data)
                    count = 0
        if count == time_out_max:
            break


def _filter_head(head_list: list):
    buffer = ''
    for line in head_list:
        if line.startswith('Connection'):
            continue
        else:
            buffer += (line + '\r\n')
    buffer += '\r\n'
    return buffer


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((local_addr, local_port))
    client.listen(5)
    while True:
        conn, addr = client.accept()
        t = threading.Thread(target=handle_request, args=(conn,))
        t.start()


if __name__ == '__main__':
    print('Proxy listening on {}:{}'.format(local_addr, local_port))
    main()
