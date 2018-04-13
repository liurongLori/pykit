#!/usr/bin/env python
#coding: utf-8

import unittest
import copy

from pykit import httpmultipart


class TestMultipart():
    def __init__(self):

        self.test_multipart = httpmultipart.MultipartObject()

    def test_headers(self):
        headers = [
            {
                'Content-Length': 998, 'Content-Type':
                       'aaplication/octet-stream'
            },
            {
                'Content-Length': 1000
            },
            {
                'Content-Type': 'application/octet-stream'
            },
            None,
        ]

        key_value_pair = {
            'metadata1':
            {
                'value': 'lvting'
            },
            'metadata2':
            {
                'value': ['/root/Study/a.txt', 'a.txt'],
                          'headers': {'Content-Type': 'application/octet-stream'}
            },
            'metadata3':
            {
                'value': ['/root/Study/b.txt']
            },
            'metadata3':
            {
                'value': ('/root/Study/b.txt')
            },
        }
        for h in headers:
            self.assertEqual(
                self._headers(key_value_pair, h),
                self.test_multipart.make_headers(key_value_pair, h)
            )

    def test_body(self):
        key_value_pair = {
            'metadata1':
            {
                'value': 'lvting'
            },
            'metadata2':
            {
                'value': ['/root/Study/a.txt', 'a.txt'],
                          'headers': {'Content-Type': 'application/octet-stream'}
            },
            'metadata3':
            {
                'value': ['/root/Study/b.txt']
            },
            'metadata3':
            {
                'value': ('/root/Study/b.txt')
            },
        }
        body = self.test_multipart.make_body_reader(key_value_pair)
        data = []
        for x in body:
            data.append(x)

        self.assertEqual(self._body(key_value_pair), ''.join(data))

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
            field_header = self.test_multipart._get_field_header(
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
        result += '--{b}--'.format(b=self.test_multipart.boundary)

        return result
