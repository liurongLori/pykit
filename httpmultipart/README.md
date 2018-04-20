<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
#   Table of Content

- [Name](#name)
- [Status](#status)
- [Synopsis](#synopsis)
- [Description](#description)
- [Exception](#exception)
  - [httpmultipart.MultipartError](#httpmultipartmultiparterror)
  - [httpmultipart.InvalidArgumentTypeError](#httpmultipartinvalidargumenttypeerror)
- [Constants](#constants)
  - [httpmultipart.MultipartObject.boundary](#httpmultipartmultipartobjectboundary)
  - [httpmultipart.MultipartObject.block_size](#httpmultipartmultipartobjectblock_size)
- [Classes](#classes)
  - [httpmultipart.MultipartObject](httpmultipartmultipartobject)
- [Methods](#methods)
  - [httpmultipart.MultipartObject.make_headers](#httpmultipartmultipartobjectmake_headers)
  - [httpmultipart.MultipartObject.make_body_reader](#httpmultipartmultipartobjectmake_body_reader)
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

# get http request body reader
body_reader = httpmultipart.make_body_reader(fields)
data = []

for body in body_reader:
    data.append(body)
body = ''.join(data)
#body = '
#           --FormBoundaryrGKCBY7qhFd3TrwA
#           Content-Disposition: form-data; name=field_name
#
#           content
#           --FormBoundaryrGKCBY7qhFd3TrwA
#           Content-Disposition: form-data; name=field_name; filename=file_name
#           Content-Type: application/octet-stream
#
#           file_content
#           EOF
#           --FormBoundaryrGKCBY7qhFd3TrwA--
#           ...
#        '
```

#   Description

This module provides some util methods to get multipart headers and body.

#   Exception

##  httpmultipart.MultipartError

**syntax**:
`httpmultipart.MultipartError`

The base class of the other exceptions in this module.
It is a subclass of `Exception`

##  httpmultipart.InvalidArgumentTypeError

**syntax**:
`httpmultipart.InvalidArgumentTypeError`

A subclass of `MultipartError`
Raise if value's type is not a str or a list

#   Constants

##  httpmultipart.MultipartObject.boundary

**syntax**:
`httpmultipart.MultipartObject.boundary`

a placeholder that represents out specified delimiter

##  httpmultipart.MultipartObject.block_size

**syntax**:
`httpmultipart.MultipartObject.block_size`

It represents the size of each reading file

#   Classes

##  httpmultipart.MultipartObject

**syntax**:
`http.MultipartObject()`

#   Methods

##  httpmultipart.MultipartObject.make_headers

**syntax**:
`httpmultipart.MultipartObject.make_headers`

Return a header according to the fields and headers

**arguments**:

-   `fields`:
    is a list of the dict, and each elements contains `name`, `value` and `headers`,
    and so on. `headers` is an optional argument

    -   `name`:
    It's a string that represents field's name

    -   `value`:
    The value can be a string or a list, string indicates that the field is a normal
    string, However, there are three situations about list:

    First, the list indicates that field can be a common string generator, and the
    arguments are `str_reader` and `size`. The `str_reader` is a generator,
    representing upload the large string, `size` refers to the length of the
    string

    Second, the list indicates that field can be a file, and the arguments are
    `file_path` and `size`. The `file_path` is the path of the file and `size`
    refers to the length of the file. When the list[0] is a `file_path`, the
    program automatically converts the file by `file_path` into a common string
    generator

    Third, the list indicates that field can be a file generator, and the arguments
    are `file_reader`, `size` and `file_name`. The `file_reader` is a generator,
    representing upload the file, `size` refers to the length of the file, `file_name`
    is the name of the uploaded file

    -   `headers`:
    a dict, key is the `field_header_name`, value is the `field_header_value`,
    it contains user defined headers and the required headers, such as
    'Content-Disposition' and 'Content-Type'

-   `headers`:
    a dict of http request headers, key is the `header_name`, value is the
    `header_value`.  It's a default argument and its default value is None

**return**:
a dict that represents the request headers

##  httpmultipart.MultipartObject.make_body_reader

**syntax**
`httpmultipart.MultipartObject.make_body_reader`

Return a body according to the fields

**arguments**:

-  `fields`:
    refer to the explanation above fields

**return**:
a generator that represents the multipart request body

#   Author

Ting Lv(吕婷) <ting.lv@baishancloud.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2017 Ting Lv(吕婷) <ting.lv@baishancloud.com>
