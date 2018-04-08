#!/usr/bin/env python
#coding: utf-8

from random import Random
from pykit import http
from pykit import mime


class PostClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.headers = {}
        self.boundary = ''

        self.http_client = http.Client(self.host, self.port)

    def multipart_request(self, headers={}):
        self.send_multipart_request('/', 'POST', headers)

    def response(self):
        self.read_response()

    def send_multipart_request(self, uri, method, headers):
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'multipart/form-data;'

        self.boundary = self._random_boundary()
        headers['Content-Type'] += 'boundary=${'+self.boundary+'}'

        self.http_client.send_request(uri, method=method, headers=headers)

    def read_response(self):
        test_status, test_headers = self.http_client.read_response()
        return test_status, test_headers

    def read_body(self):
        self.http_client.read_body(32)

    def send_field(self, key_value_pair={}):
        field = self._field(key_value_pair)

        self.http_client.send_body(field)
        return field

    def _field(self, key_value_pair):
        post_data = []

        for k, v in key_value_pair.items():
            post_data.append('--${'+self.boundary+'}')

            if isinstance(v['value'], str):
                post_data.append('Content Dispostion:form-data;name='+k)

                if 'headers' in v:
                    for ki, vi in v['headers'].items():
                        post_data.append(ki+':'+vi)

                post_data.append('')
                post_data.append(v['value'])
            elif isinstance(v['value'], list) or isinstance(v['value'], tuple):
                fname = ''
                if v['value'][1] is None:
                    fname = v['value'][0].split('/')[-1]
                else:
                    fname = v['value'][1]
                post_data.append('Content Dispostion:form-data;'
                            +'name='+k+';filename='+fname)

                file_type = mime.get_by_filename(fname)

                if 'headers' in v:
                    if 'Content-Type' not in v['headers']:
                        v['headers']['Content-Type'] = str(file_type)
                else:
                    v['headers'] = {}
                    v['headers']['Content-Type'] = str(file_type)

                for ki, vi in v['headers'].items():
                    post_data.append(ki+':'+vi)

                post_data.append('')
                post_data.append(self._read_file(v['value'][0]))

        post_data.append('--${'+self.boundary+'}--')
        post_data = '\r\n'.join(post_data)

        return post_data

    def _read_file(self, path):
        bufs = ''

        with open(path) as f:
            line = f.readline()
            while line:
                bufs += line
                line = f.readline()

        return str(bufs)

    def _random_boundary(self):
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        random_length = 8
        result = ''
        random = Random()

        for i in range(random_length):
            result += chars[random.randint(0, len(chars)-1)]

        return result

