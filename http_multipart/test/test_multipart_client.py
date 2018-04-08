#!/usr/bin/env python
#coding: utf-8

from pykit import http_multipart

class TestPostClient(object):

    def test_field(self):
        case = {
            'metadata1': {'value': ['/root/Study/c.txt', None], 'headers':
                          {'Content-Type': 'application/octet-stream'}},
            'metadata2': {'value': 'lvting'},
            'metadata3': {'value': ['/root/Study/a.txt', 'a.txt'], 'headers': {}},
            'metadata4': {'value': ['/root/Study/b.txt', None]},
            'metadata5': {'value': ('/root/Study/c.txt', None), 'headers':
                          {'Content-Type': 'application/octet-stream'}},
            'metadata6': {'value': ('/root/Study/a.txt', 'a.txt'), 'headers': {}},
            'metadata7': {'value': ('/root/Study/b.txt', None)},
             }

        self.post_client = http_multipart.PostClient('www.baidu.com', 80)
        self.post_client.multipart_request()
        field = self.post_client.send_field(case)
        print field


if __name__ == '__main__':
    cli = TestPostClient()
    cli.test_field()
