#!/usr/bin/env python
#coding: utf-8

import unittest
import copy

from pykit import httpmultipart


class TestMultipart(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMultipart, self).__init__(*args, **kwargs)

        self.test_multipart = httpmultipart.MultipartObject()

    def test_headers(self):
        case = [
            [
                {
                    'Content-Length': 998,
                    'Content-Type': 'aaplication/octet-stream'
                },
                {
                    'Content-Length': 998,
                    'Content-Type': 'multipart/form-data;' + \
                            'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ],
            [
                {
                    'Content-Length': 1000
                },
                {
                    'Content-Length': 1000,
                    'Content-Type': 'multipart/form-data;' + \
                            'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ],
            [
                {
                    'Content-Type': 'application/octet-stream'
                },
                {
                    'Content-Length': 914,
                    'Content-Type': 'multipart/form-data;' + \
                            'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ],
            [
                None,
                {
                    'Content-Length': 914,
                    'Content-Type': 'multipart/form-data;' + \
                            'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ]
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
        }
        for h in case:
            self.assertEqual(
                h[1],
                self.test_multipart.make_headers(key_value_pair, h[0])
            )

    def test_body(self):
        case = [
            [
                {
                    'metadata1':
                    {
                        'value': 'lvting'
                    }
                },
                [
                    '--{b}'.format(b=self.test_multipart.boundary),
                    'Content-Dispostion: form-data;name=metadata1',
                    ''
                ]
            ],
            [
                {
                    'metadata2':
                    {
                        'value': ['/root/Study/a.txt', 'a.txt'],
                        'headers': {'Content-Type': 'application/octet-stream'}
                    }
                },
                [
                    '--{b}'.format(b=self.test_multipart.boundary),
                    'Content-Dispostion: form-data;name=metadata2;' \
                                         + 'filename=a.txt',
                    'Content-Type: application/octet-stream',
                    ''
                ]
            ],
            [
                {
                    'metadata3':
                    {
                        'value': ['/root/Study/b.txt']
                    }
                },
                [
                    '--{b}'.format(b=self.test_multipart.boundary),
                    'Content-Dispostion: form-data;name=metadata3;' \
                                         + 'filename=b.txt',
                    'Content-Type: text/plain',
                    ''
                ]
            ],
        ]
        key_value_pair = {}
        for c in case:
            for name, field in c[0].items():
                key_value_pair[name] = field

        body = self.test_multipart.make_body_reader(key_value_pair)
        data = []
        for x in body:
            data.append(x)

        self.assertEqual(self._body(case), ''.join(data))

    def _body(self, case):
        result = ''

        for c in case:
            field_header = c[1]
            result += '\r\n'.join(field_header)
            result += '\r\n'

            for field in c[0].values():
                value, headers = field['value'], field.get('headers', {})

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
