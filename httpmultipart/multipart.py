#!/usr/bin/env python
#coding: utf-8

import os.path
import uuid
import errno
import copy

from pykit import mime
from collections import Iterator


class MultipartError(Exception):
    pass


class InvalidArgumentError(MultipartError):
    pass


class MultipartObject(object):

    def __init__(self):
        self.boundary = uuid.uuid4().hex

    def make_headers(self, fields, headers=None):

        if headers is None:
            headers = {}
        else:
            headers = copy.deepcopy(headers)

        headers['Content-Type'] = 'multipart/form-data; ' + \
            'boundary={b}'.format(b=self.boundary)

        if 'Content-Length' not in headers:
            body_size = self._get_body_size(fields)
            headers['Content-Length'] = body_size

        return headers

    def make_body_reader(self, fields):

        for field in fields:
            name, value, headers = (
                field['name'], field['value'], field.get('headers', {}))

            _reader, size, headers = self._get_normal_field(
                name, value, headers)
            field_header = self._get_field_header(headers)

            yield field_header

            for buf in _reader:
                yield buf

            yield '\r\n'

        yield '--{b}--'.format(b=self.boundary)

    def make_file_reader(self, file_path):
        with open(file_path) as f:
            while True:
                buf = f.read(1024 * 1024)
                if buf == '':
                    break
                yield buf

    def _get_normal_field(self, name, value, headers):
        _reader, size, file_name = None, None, None
        headers = copy.deepcopy(headers)
        field_headers = []

        if isinstance(value, str):
            _reader, size = self._make_str_reader(value), len(value)
            cont_dis = 'Content-Disposition: form-data; ' + \
                'name={n}'.format(n=name)
            field_headers.append(cont_dis)
        elif isinstance(value, list):
            _reader, size, file_name = (value + [None])[:3]

            if file_name is None:
                cont_dis = 'Content-Disposition: form-data; ' + \
                    'name={n}'.format(n=name)
                field_headers.append(cont_dis)
            else:
                cont_dis = 'Content-Disposition: form-data; ' + \
                    'name={n}; filename={fn}'.format(n=name, fn=file_name)
                field_headers.append(cont_dis)

                if 'Content-Type' not in headers:
                    file_type = mime.get_by_filename(file_name)
                    headers['Content-Type'] = str(file_type)
        else:
            raise InvalidArgumentError(
                'value is invalid type {x}'.format(x=type(value)))

        for ki, vi in headers.items():
            field_headers.append(ki+': '+vi)

        field_headers.extend([''] * 2)

        return _reader, size, field_headers

    def _get_field_size(self, field):
        name, value, headers = (
            field['name'], field['value'], field.get('headers', {}))

        _reader, size, headers = self._get_normal_field(
            name, value, headers)

        field_header = self._get_field_header(headers)

        field_size = len(field_header)
        field_size += size

        field_size += len('\r\n')

        return field_size

    def _get_body_size(self, fields):
        body_size = 0

        for field in fields:
            body_size += self._get_field_size(field)

        body_size += len('--{b}--'.format(b=self.boundary))

        return body_size

    def _get_field_header(self, headers):
        field_header = ['--{b}'.format(b=self.boundary)]

        for h in headers:
            field_header.append(h)

        return '\r\n'.join(field_header)


    def _make_str_reader(self, strs):
        yield strs
