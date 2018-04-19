<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
#   Table of Content

- [Name](#name)
- [Status](#status)
- [Synopsis](#synopsis)
- [Description](#description)
- [Exception](#exception)
  - [httpmultipart.MultipartError](#httpmultipartmultiparterror)
  - [httpmultipart.InvalidArgumentError](#httpmultipartinvalidArgumenterror)
- [Constants](#constants)
  - [httpmultipart.MultipartObject.boundary](#httpmultipartmultipartobjectboundary)
- [Classes](#classes)
  - [httpmultipart.MultipartObject](httpmultipartmultipartobject)
- [Methods](#methods)
  - [httpmultipart.make_headers](#httpmultipartmake_headers)
  - [httpmultipart.make_body_reader](#httpmultipartmake_body_reader)
  - [httpmultipart.make_file_reader](#httpmultipartmake_file_reader)
- [Author](#author)
- [Copyright and License](#copyright-and-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

#   Name

httpmultipart

#   Status

The library is considered production ready.

#   Synopsis

```python
from pykit import httpmultipart

# http request headers
headers = {
    'Content-Length': len(body),
    ...
}

# http request fields
fields = [
    {
        'name': 'field_name',
        'value': content,
        'headers': {}
    },
    ...
]

# get http request headers
res_headers = httpmultipart.make_headers(fields, header)
#res_headers = {
#                  'Content-Type': 'multipart/form-data; boundary=${bound}',
#                  'Conetnt-Length': 1024,
#                  ...
#              }

```

```python
from pykit import httpmultipart

# http request fields
# refer to the explanation above fields

# get http request body reader
body_reader = httpmultipart.make_body_reader(fields)
data = []

for body in body_reader:
    data.append(body)
body = ''.join(data)
#body = '
#           --${bound}
#           Content-Disposition: form-data; name=field_name
#
#           content
#           --${bound}
#           Content-Disposition: form-data; name=field_name; filename=file_name
#           Content-Type: application/octet-stream
#
#           file_content
#           EOF
#           --${bound}--
#        '
```
```python
from pykit import httpmultipart

#the path of the file
file_path = '/root/tmp/example.txt'

#Convert file to generator
file_reader = httpmultipart.make_file_reader(file_path)

```

#   Description

This module provide some util methods to get multipart headers and body.

#   Exceptions

##  httpmultipart.MultipartError

**syntax**:
`httpmultipart.MultipartError`

The base class of the other exceptions in this module.
It is a subclass of `Exception`

##  httpmultipart.InvalidArgumentError

**syntax**:
`httpmultipart.InvalidArgumentError`

A subclass of `MultipartError`
Raise if value is not a str or a list

#   Constants

##  httpmultipart.MultipartObject.boundary

**syntax**:
`httpmultipart.MultipartObject.boundary`

Multipart body need boundary

#   Classes

##  httpmultipart.MultipartObject

**syntax**:
`http.MultipartObject()`

#   Methods

##  httpmultipart.MultipartObject.make_headers

**syntax**:
`httpmultipart.MultipartObject.make_headers`

Return a header according to the fields and headers

Examples:
```
print httpmultipart.make_headers(fields, headers)
```
**arguments**:

-   `fields`:
    a list, each element is a dict in the list, and dict contains three keys,
    `name`, `value` and `headers`

    -   `name`:
    It's a str that represents each field's name

    -   `value`:
    The value can be a str or a list, str says that the field is a normal str,
    the list says that the field can be a large str as a generator or a file
    as a generator, for example, the `list`[`str_reader`, `size`]、 the `list`
    [`file_reader`, `size`, file_name]

        -   `str_reader`:
        It's a generator, representing upload the large str

        -   `file_reader`:
        It's a generator, representing upload the file

        -   `size`:
        the size of the uploaded large str or file

        -   `file_name`:
        upload the name about the file, if `list[0]` is a str_reader, file_name
        is None

    -   `headers`:
    a dict, key is the field_header_name, value is the field_header_value,
    it contains user defined headers and the required headers, such as
    'Content-Disposition' and 'Content-Type'

-   `headers`:
    a `dict`{`header_name`: `header_value`} of http request headers
    It's a default argument and its default value is None

**return**:
dict about headers

##  httpmultipart.MultipartObject.make_body_reader

**syntax**
`httpmultipart.MultipartObject.make_body_reader`

Return a body after multipart encoding according to the fields

Examples:
```
body_reader = httpmultipart.make_body_reader(fields)
data = []

for body in body_reader:
    data.append(body)
print ''.join(data)
```
**arguments**:

-  `fields`:
    refer to the explanation above fields

**return**:
generator about body after multipart encoding

##  httpmultipart.MultipartObject.make_file_reader

**syntax**
`httpmultipart.MultipartObject.make_file_reader`

Return a generator about file

Examples:
```
file_reader = httpmultipart.make_file_reader(file_path)
```
**arguments**

-   `file_path`:
    the path of the file

**return**:
generator about file

#   Author

Ting Lv(吕婷) <ting.lv@baishancloud.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2017 Ting Lv(吕婷) <ting.lv@baishancloud.com>
