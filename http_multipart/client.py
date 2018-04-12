#!/usr/bin/env python
#coding: utf-8

import os
import os.path
import uuid
import errno
import copy

from pykit import mime

class MultipartError(Exception):
    pass


class InvalidArgumentError(MultipartError):
    pass


class MultipartRequest(object):

    def __init__(self):
        self.boundary = uuid.uuid4().hex

    def make_headers(self, key_value_pair, headers=None):

        if headers is None:
            headers = {}
        else:
            headers = copy.deepcopy(headers)

        body_size = None

        headers['Content-Type'] = 'multipart/form-data;' + \
            'boundary='+self.boundary

        if 'Content-Length' not in headers:
            body_size = self._get_body_size(key_value_pair)
            headers['Content-Length'] = body_size

        return headers

    def make_body_reader(self, key_value_pair):

        for field_name, field in key_value_pair.items():
            value, headers = field['value'], field.get('headers', {})

            str_header = self._get_one_field_header(
                field_name, value, headers)

            yield str_header

            if isinstance(value, str):

                yield value
            elif isinstance(value, list):
                file_path = value[0]

                with open(file_path) as f:
                    while True:
                        buf = f.read(1024*1024)
                        if buf == '':
                            break

                        yield buf
            else:
                raise InvalidArgumentError(
                    'value is invalid {x}'.format(x=value))

            yield '\r\n'

        yield '--'+self.boundary+'--'

    def _get_one_field_header(self, name, value, headers):
        headers = copy.deepcopy(headers)
        field_header = ['--' + self.boundary]

        if isinstance(value, str):
            field_header.append('Content-Dispostion: form-data;name=' + name)

        elif isinstance(value, list):
            file_path, file_name = (value + [None])[:2]

            if file_name is None:
                file_name = os.path.basename(file_path)

            field_header.append('Content-Dispostion: form-data;'
                                + 'name=' + name + ';filename=' + file_name)

            if 'Content-Type' not in headers:
                file_type = mime.get_by_filename(file_name)
                headers['Content-Type'] = str(file_type)
        else:
            raise InvalidArgumentError(
                'value is invalid {x}'.format(x=value))

        for ki, vi in headers.items():
            field_header.append(ki+': '+vi)

        field_header.extend(['']*2)
        return '\r\n'.join(field_header)

    def _get_one_field_size(self, name, field):
        value, headers = field['value'], field.get('headers', {})

        field_size = len(self._get_one_field_header(name, value, headers))
        file_path = value[0]

        if isinstance(value, str):
            field_size += len(value)
        elif isinstance(value, list):
            field_size += os.path.getsize(file_path)

        field_size += len('\r\n')

        return field_size

    def _get_body_size(self, key_value_pair):
        body_size = 0

        for name, field in key_value_pair.items():
            body_size += self._get_one_field_size(name, field)

        body_size += len('--'+self.boundary+'--')

        return body_size
