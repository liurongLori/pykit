#!/usr/bin/env python
#coding: utf-8

import os
import os.path
import uuid
import errno
import copy

from random import Random
from pykit import http
from pykit import mime

class HttpError(Exception):
    pass


class InvalidArgumentError(HttpError):
    pass


class SendFieldError(HttpError):
    pass

class NoneFieldError(HttpError):
    pass


class PostClient(object):
    def __init__(self, host, port, headers=None, timeout=60):
        self.host = host
        self.port = port
        self.headers = copy.deepcopy(headers) or {}
        self.is_requested = False
        self.body_size = None
        self.has_content_length = True

        self.http_client = http.Client(self.host, self.port)
        self.boundary = uuid.uuid4().hex
        self.headers['Content-Type'] = 'multipart/form-data;'+'boundary='+self.boundary

    def read_response(self):
        status, headers = self.http_client.read_response()
        result = {
                    'status': status,
                    'headers': headers,
                    'body': self._read_body
                 }

        return result

    def send_fields(self, key_value_pair=None):

        if self.has_content_length is False and self.is_requested is True:
            raise SendFieldError('can not repeat to send field {x}'
                              .format(x=key_value_pair))

        if self.is_requested is False:
            self.body_size = self._get_body_size(key_value_pair)
            self._request()

        for field_name, field in key_value_pair.items():
            self._send_one_field(field_name, field)

        if key_value_pair is not None:
            self.http_client.send_body('--'+self.boundary+'--')
        else:
            raise NoneFieldError('can not send None field {x}'
                              .format(x=key_value_pair))

    def _send_one_field(self, name, field):
        f = copy.deepcopy(field)
        value, headers = f['value'], f.get('headers', {})

        field_header = self._get_one_field_header(name, value, headers)

        if isinstance(value, str):

            self.http_client.send_body(field_header)
            self.http_client.send_body(value)

        elif isinstance(value, list):
            file_path = value[0]

            self.http_client.send_body(field_header)

            with open(file_path) as f:
                while True:
                    has_read = f.read(1024*1024)
                    if has_read == '':
                        break
                    self.http_client.send_body(has_read)
        else:
            raise InvalidArgumentError('value is invalid {x}'.format(x=value))

        self.http_client.send_body('\r\n')

    def _get_one_field_header(self, name, value, headers):
        field_header = ['--'+self.boundary]

        if isinstance(value, str):
            field_header.append('Content-Dispostion: form-data;name='+name)

        elif isinstance(value, list):
            file_path, file_name = (value + [None])[:2]

            if file_name is None:
                file_name = os.path.basename(file_path)

            field_header.append('Content-Dispostion: form-data;'
                            +'name='+name+';filename='+file_name)

            if 'Content-Type' not in headers:
                file_type = mime.get_by_filename(file_name)
                headers['Content-Type'] = str(file_type)

        for ki, vi in headers.items():
            field_header.append(ki+': '+vi)

        field_header.extend([''] * 2)
        return '\r\n'.join(field_header)

    def _get_one_field_size(self, name, field):
        f = copy.deepcopy(field)
        value, headers = f['value'], f.get('headers', {})
        field_size = 0

        field_header = self._get_one_field_header(name,
                        value, headers)

        field_size += len(field_header)

        if isinstance(value, str):
            field_size += len(value)
        elif isinstance(value, list):
            field_size += os.path.getsize(value[0])

        field_size += len('\r\n')

        return field_size

    def _get_body_size(self, key_value_pair):
        real_size = 0

        for n, f in key_value_pair.items():
            real_size += self._get_one_field_size(n, f)

        real_size += len('--'+self.boundary+'--')

        return real_size

    def _request(self):
        self.is_requested = True

        if 'Content-Length' not in self.headers:
            self.headers['Content-Length'] = self.body_size
            self.has_content_length = False

        self.http_client.send_request(
                '/', 'POST', headers=self.headers)

    def _read_body(self, size):
        return self.http_client.read_body(size)
