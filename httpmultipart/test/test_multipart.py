#!/usr/bin/env python
#coding: utf-8

import unittest
import copy
import random
import string
import os

from pykit import httpmultipart
from pykit import fsutil

class TestMultipart(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMultipart, self).__init__(*args, **kwargs)

    def test_headers(self):
        test_multipart = httpmultipart.MultipartObject()

        case = [
            [
                {
                    'Content-Length': 998,
                    'Content-Type': 'aaplication/octet-stream'
                },
                {
                    'Content-Length': 998,
                    'Content-Type': 'multipart/form-data; ' +
                        'boundary={b}'.format(b=test_multipart.boundary)
                }
            ],
            [
                {
                    'Content-Length': 1200
                },
                {
                    'Content-Length': 1200,
                    'Content-Type': 'multipart/form-data; ' +
                        'boundary={b}'.format(b=test_multipart.boundary)
                }
            ],
            [
                {
                    'Content-Type': 'application/octet-stream'
                },
                {
                    'Content-Length': 1207,
                    'Content-Type': 'multipart/form-data; ' +
                        'boundary={b}'.format(b=test_multipart.boundary)
                }
            ],
            [
                None,
                {
                    'Content-Length': 1207,
                    'Content-Type': 'multipart/form-data; ' +
                        'boundary={b}'.format(b=test_multipart.boundary)
                }
            ]
        ]

        str1 = '''
                使命：Better Internet ，Better life
                愿景：成为全球受人尊敬的科技公司；最具创新力；最佳雇主
                未来白山的特质：渴求变革；让创新超越客户想象；全球化；真诚、并始终如一
                信条：以用户为中心，其他一切水到渠成；专心将一件事做到极致；越快越好
               '''
        str2 = '''
                12343564343rfe
                fdf4erguu38788894hf
                12rfhfvh8876w91908777yfj
               '''
        str3 = '''
                838839938238838388383838
                dddjjdkkksijdidhdhhhhddd
                djdjdfdf4erguu38788894hf
                12rfhfvh8876w91908777yfj
               '''

        fsutil.write_file(
            '/root/tmp/a.txt', str1
        )
        fsutil.write_file(
            '/root/tmp/b.txt', str2
        )

        def make_str_reader():
            yield str3

        def make_file_reader():
            with open('/root/tmp/a.txt') as f:
                while True:
                    buf = f.read(1024 * 1024)
                    if buf == '':
                        break
                    yield buf

        str_reader = make_str_reader()
        str_size = len(str3)

        file_reader = make_file_reader()
        file_size = os.path.getsize('/root/tmp/a.txt')

        fields = [
            {
                'name': 'metadata1',
                'value': 'lvting',
            },
            {
                'name': 'metadata2',
                'value': [str_reader, str_size],
            },
            {
                'name': 'metadata3',
                'value': [file_reader, file_size, 'a.txt'],
            },
            {
                'name': 'metadata4',
                'value':
                [test_multipart.make_file_reader('/root/tmp/b.txt'),
                          os.path.getsize('/root/tmp/b.txt'), 'b.txt'],
                'headers': {'Content-Type': 'application/octet-stream'}
            },
        ]
        for h in case:
            self.assertEqual(
                h[1],
                test_multipart.make_headers(fields, h[0])
            )

    def test_body(self):
        test_multipart = httpmultipart.MultipartObject()

        str1 = '''
                使命：Better Internet ，Better life
                愿景：成为全球受人尊敬的科技公司；最具创新力；最佳雇主
                未来白山的特质：渴求变革；让创新超越客户想象；全球化；真诚、并始终如一
                信条：以用户为中心，其他一切水到渠成；专心将一件事做到极致；越快越好
               '''
        str2 = '''
                12343564343rfe
                fdf4erguu38788894hf
                12rfhfvh8876w91908777yfj
               '''
        str3 = '''
                838839938238838388383838
                dddjjdkkksijdidhdhhhhddd
                djdjdfdf4erguu38788894hf
                12rfhfvh8876w91908777yfj
               '''

        fsutil.write_file(
            '/root/tmp/a.txt', str1
        )
        fsutil.write_file(
            '/root/tmp/b.txt', str2
        )

        def make_str_reader():
            yield str3

        def make_file_reader():
            with open('/root/tmp/a.txt') as f:
                while True:
                    buf = f.read(1024 * 1024)
                    if buf == '':
                        break
                    yield buf

        str_reader = make_str_reader()
        str_size = len(str3)

        file_reader = make_file_reader()
        file_size = os.path.getsize('/root/tmp/b.txt')

        case = [
            [
                [
                    {
                        'name': 'metadata1',
                        'value': 'lvting'
                    }
                ],
                [
                    '--{b}'.format(b=test_multipart.boundary),
                    'Content-Disposition: form-data; name=metadata1',
                    '',
                    'lvting',
                    '--{b}--'.format(b=test_multipart.boundary),
                ]
            ],
            [
                [
                    {
                        'name': 'metadata2',
                        'value': [str_reader, str_size],
                    }
                ],
                [
                    '--{b}'.format(b=test_multipart.boundary),
                    'Content-Disposition: form-data; name=metadata2',
                    '',
                    str3,
                    '--{b}--'.format(b=test_multipart.boundary),
                ]
            ],
            [
                [
                    {
                        'name': 'metadata3',
                        'value': [file_reader, file_size, 'a.txt'],
                    }
                ],
                [
                    '--{b}'.format(b=test_multipart.boundary),
                    'Content-Disposition: form-data; name=metadata3; '
                        + 'filename=a.txt',
                    'Content-Type: text/plain',
                    '',
                    str1,
                    '--{b}--'.format(b=test_multipart.boundary),
                ]
            ],
            [
                [
                    {
                        'name': 'metadata4',
                        'value':
                        [test_multipart.make_file_reader('/root/tmp/b.txt'),
                            os.path.getsize('/root/tmp/b.txt'), 'b.txt'],
                    }
                ],
                [
                    '--{b}'.format(b=test_multipart.boundary),
                    'Content-Disposition: form-data; name=metadata4; '
                        + 'filename=b.txt',
                    'Content-Type: text/plain',
                    '',
                    str2,
                    '--{b}--'.format(b=test_multipart.boundary),
                ]
            ],

        ]
        for c in case:
            body = test_multipart.make_body_reader(c[0])
            data = []
            for x in body:
                data.append(x)

            self.assertEqual('\r\n'.join(c[1]), ''.join(data))

    def tearDown(self):
        fsutil.remove('/root/tmp/a.txt')
        fsutil.remove('/root/tmp/b.txt')
