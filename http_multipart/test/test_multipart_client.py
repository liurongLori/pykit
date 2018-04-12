#!/usr/bin/env python
#coding: utf-8

import unittest
import threading
import time

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from pykit import http_multipart

HOST = '127.0.0.1'
PORT = 30040

class TestPostClient(unittest.TestCase):
    def test_field(self):
        case = {
                'metadata1': {'value': ['/root/Study/a.txt', 'a.txt'], 'headers':
                          {'Content-Type': 'application/octet-stream'}},
                'metadata2': {'value': 'lvting'},
                'metadata3': {'value': ['/root/Study/a.txt', 'a.txt']},
                'metadata4': {'value': ['/root/Study/b.txt']},
                'metadata5': {'value': ['/root/Study/c.txt'], 'headers':
                          {'Content-Type': 'application/octet-stream'}},
                #'metadata6': {'value': ()},
               }

        self.post_client = http_multipart.PostClient(HOST, PORT)
        self.post_client.send_fields(case)
        self.assertEqual(self._response(), self._field(case))

        self.tearDown()
    def setUp(self):
        self.server_thread = None
        self.http_server = None
        self.post_client = None
        self.field = None

        self.server_thread = threading.Thread(target=self._start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)
        self._type_equality_funcs = {}

    def tearDown(self):
        if self.http_server is not None:
            self.http_server.shutdown()
            self.http_server.server_close()

        self.server_thread.join()

    def _field(self, key_value_pair):
        result = ''

        for k, f in key_value_pair.items():
            name, value, headers = k, f['value'], f.get('headers', {})
            field_header = self.post_client._get_one_field_header(
                                      name, value, headers)
            result += ''.join(field_header)
            data = []

            if isinstance(value, str):
                data.append(value)
            elif isinstance(value, list):
                file_path = (value)[0]

                with open(file_path) as f:
                    while True:
                        has_read = f.read(1024*1024)
                        if has_read == '':
                            break
                        data.append(has_read)
            result += '\r\n'.join(data)
            result += '\r\n'
        result += '--'+self.post_client.boundary+'--'

        return result

    def _response(self):
        result = self.post_client.read_response()
        bufs = ''
        while True:
            buf = self.post_client._read_body(1024*1024)
            if buf == '':
                break
            bufs += buf

        return bufs

    def _start_server(self):
        self.http_server = HTTPServer((HOST, PORT), Handle)
        self.http_server.serve_forever()

class Handle(BaseHTTPRequestHandler):

    def do_POST(self):
        datas = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.send_header('Content-Length', int(self.headers['Content-Length']))
        self.end_headers()
        self.wfile.write(datas)

if __name__ == '__main__':
    unittest.main()
