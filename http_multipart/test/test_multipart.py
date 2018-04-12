#!/usr/bin/env python
#coding: utf-8

import unittest
import copy

from pykit import http_multipart


class TestPostClient():
    def __init__(self):

        self.test_multipart = http_multipart.MultipartRequest()
        self.headers = [
            {'Content-Length': 998, 'Content-Type':
             'aaplication/octet-stream'},
            {'Content-Length': 1000},
            {'Content-Type': 'application/octet-stream'},
            None,
        ]

        self.field = {
            'metadata1': {'value': 'lvting'},
            'metadata2': {'value': ['/root/Study/a.txt', 'a.txt'],
                          'headers': {'Content-Type': 'application/octet-stream'}},
            'metadata3': {'value': ['/root/Study/b.txt']},
            'metadata3': {'value': ('/root/Study/b.txt')},
        }

    def test_headers(self):
        for h in self.headers:
            self.assertEqual(
                self._headers(self.field, h),
                self.test_multipart.make_headers(self.field, h)
            )

    def test_body(self):
        body = self.test_multipart.make_body_reader(self.field)
        data = []
        for x in body:
            data.append(x)

        self.assertEqual(self._body(self.field), ''.join(data))

    def _headers(self, field, headers):
        if headers is None:
            headers = {}
        else:
            headers = copy.deepcopy(headers)

        headers['Content-Type'] = 'multipart/form-data;' + \
            'boundary=' + self.test_multipart.boundary

        if 'Content-Length' not in headers:
            headers['Content-Length'] = self.test_multipart._get_body_size(
                field)

        return headers

    def _body(self, field):
        result = ''

        for name, f in field.items():
            value, headers = f['value'], f.get('headers', {})
            field_header = self.test_multipart._get_one_field_header(
                                      name, value, headers)
            result += ''.join(field_header)
            data = []

            if isinstance(value, str):
                data.append(value)
            elif isinstance(value, list):
                file_path = (value)[0]

                with open(file_path) as f:
                    while True:
                        buf = f.read(1024*1024)
                        if buf == '':
                            break
                        data.append(buf)
            result += '\r\n'.join(data)
            result += '\r\n'
        result += '--'+self.test_multipart.boundary+'--'

        return result

if __name__ == '__main__':
    unittest.main()
