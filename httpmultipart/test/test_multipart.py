#!/usr/bin/env python
#coding: utf-8

import unittest
import copy

from pykit import httpmultipart
from pykit import fsutil


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
                    'Content-Type': 'multipart/form-data;' +
                    'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ],
            [
                {
                    'Content-Length': 1000
                },
                {
                    'Content-Length': 1000,
                    'Content-Type': 'multipart/form-data;' +
                    'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ],
            [
                {
                    'Content-Type': 'application/octet-stream'
                },
                {
                    'Content-Length': 925,
                    'Content-Type': 'multipart/form-data;' +
                    'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ],
            [
                None,
                {
                    'Content-Length': 925,
                    'Content-Type': 'multipart/form-data;' +
                    'boundary={b}'.format(b=self.test_multipart.boundary)
                }
            ]
        ]

        fsutil.write_file(
            '/root/tmp/a.txt',
            '''
                使命：Better Internet ，Better life
                愿景：成为全球受人尊敬的科技公司；最具创新力；最佳雇主
                未来白山的特质：渴求变革；让创新超越客户想象；全球化；真诚、并始终如一
                信条：以用户为中心，其他一切水到渠成；专心将一件事做到极致；越快越好
            '''
        )
        fsutil.write_file(
            '/root/tmp/b.txt',
            '''
                12343564343rfe
                fdf4erguu38788894hf
                12rfhfvh8876w91908777yfj
            '''
        )
        key_value_pair = {
            'metadata1':
            {
                'value': 'lvting'
            },
            'metadata2':
            {
                'value': ['/root/tmp/a.txt', 'a.txt'],
                'headers': {'Content-Type': 'application/octet-stream'}
            },
            'metadata3':
            {
                'value': ['/root/tmp/b.txt']
            },
        }
        for h in case:
            self.assertEqual(
                h[1],
                self.test_multipart.make_headers(key_value_pair, h[0])
            )

    def test_body(self):
        fsutil.write_file(
            '/root/tmp/a.txt',
            '''
                使命：Better Internet ，Better life
                愿景：成为全球受人尊敬的科技公司；最具创新力；最佳雇主
                未来白山的特质：渴求变革；让创新超越客户想象；全球化；真诚、并始终如一
                信条：以用户为中心，其他一切水到渠成；专心将一件事做到极致；越快越好
            '''
        )
        fsutil.write_file(
            '/root/tmp/b.txt',
            '''
                12343564343rfe
                fdf4erguu38788894hf
                12rfhfvh8876w91908777yfj
            '''
        )
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
                        'value': ['/root/tmp/a.txt', 'a.txt'],
                        'headers': {'Content-Type': 'application/octet-stream'}
                    }
                },
                [
                    '--{b}'.format(b=self.test_multipart.boundary),
                    'Content-Dispostion: form-data;name=metadata2;'
                    + 'filename=a.txt',
                    'Content-Type: application/octet-stream',
                    ''
                ]
            ],
            [
                {
                    'metadata3':
                    {
                        'value': ['/root/tmp/b.txt']
                    }
                },
                [
                    '--{b}'.format(b=self.test_multipart.boundary),
                    'Content-Dispostion: form-data;name=metadata3;'
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
