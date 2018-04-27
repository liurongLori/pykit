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


class InvalidArgumentTypeError(MultipartError):
    pass


class MultipartObject(object):

    def __init__(self, block_size=1024 * 1024):
        self.block_size = block_size

        self.boundary = uuid.uuid4().hex

        self.delimiter = '--{b}'.format(b=self.boundary)
        self.terminator = '--{b}--'.format(b=self.boundary)

    def make_headers(self, fields, headers=None):

        if headers is None:
            headers = {}
        else:
            headers = copy.deepcopy(headers)

        headers['Content-Type'] = 'multipart/form-data; ' + \
            'boundary={b}'.format(b=self.boundary)

        if 'Content-Length' not in headers:
            headers['Content-Length'] = self._get_body_size(fields)

        return headers

    def make_body_reader(self, fields):

        for field in fields:
            name, value, headers = (
                field['name'], field['value'], field.get('headers', {}))

            fbody_reader, fbody_size, headers = self._standardize_field(
                name, value, headers)

            yield self._get_field_header(headers)

            for buf in fbody_reader:
                yield buf

            yield '\r\n'

        yield self.terminator

    def _standardize_field(self, name, value, headers):
        fbody_reader, fbody_size, fname = None, None, None

        if isinstance(value, str):
            fbody_reader, fbody_size = self._make_str_reader(value), len(value)
            headers = self._set_content_disposition(headers, name, None)
        elif isinstance(value, list):
            fbody_reader, fbody_size, fname = (value + [None] + [None])[:3]
            headers = self._set_content_disposition(headers, name, fname)

            if isinstance(fbody_reader, file):
                fbody_reader = self._make_file_reader(fbody_reader)

            if isinstance(fbody_reader, str):
                fbody_size = len(fbody_reader)
                fbody_reader = self._make_str_reader(fbody_reader)

            if fname is not None and 'Content-Type' not in headers:
                headers['Content-Type'] = (
                        str(mime.get_by_filename(fname)))
        else:
            raise InvalidArgumentTypeError(
                'type of value {x} is valid'.format(x=type(value)))

        return fbody_reader, fbody_size, headers

    def _get_field_size(self, field):
        fbody_reader, fbody_size, headers = self._standardize_field(
            field['name'], field['value'], field.get('headers', {}))

        field_headers = self._get_field_header(headers)

        return len(field_headers) + fbody_size + len('\r\n')

    def _get_body_size(self, fields):
        body_size = 0

        for field in fields:
            body_size += self._get_field_size(field)

        return body_size + len(self.terminator)

    def _get_field_header(self, headers):
        field_headers = [self.delimiter]

        field_headers.append('Content-Disposition: ' +
            self._pop_content_disposition(headers))

        for k, v in headers.items():
            field_headers.append(k+': '+v)

        field_headers.extend([''] * 2)

        return '\r\n'.join(field_headers)

    def _make_file_reader(self, file_object):

        while True:
            buf = file_object.read(self.block_size)
            if buf == '':
                break
            yield buf

    def _make_str_reader(self, data):
        yield data

    def _set_content_disposition(self, headers, name, fname):

        if fname is None:
            headers['Content-Disposition'] = (
                    'form-data; name={n}'.format(n=name))
        else:
            headers['Content-Disposition'] = (
                'form-data; name={n}; filename={fn}'.format(n=name, fn=fname))

        return headers

    def _pop_content_disposition(self, headers):
        return headers.pop('Content-Disposition')
