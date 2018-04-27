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
res_headers = httpmultipart.make_headers(fields, headers)
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
Raise if the type of value is not a str or a list or the type of value[0]
is not a string, string reader, file reader or file object

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
    `headers` is an optional argument

    -   `name`:
    It's a string that represents field's name

    -   `value`:
    The value represents field's content. The type of value can be a string or a
    list, string indicates that the field is a normal string, However, there are
    three arguments of list: `content`, `size` and `file_name`

        -   `content`:
        The type of `content` can be string, reader, file object

        The string type refers to the user want to upload a string. It takes the
        string as the field body

        The reader type refers to a generator. To read the contents of generator as
        the field body

        The file object type refers to a file object, represents upload the file.
        To read the contents of file as the field body

        -   `size`
        `size` refers to the length of the content, When the type of `content` is a
        string, size can be None

        - `file_name`
        `file_name` is an optional argument, if `file_name` is None, that indicates
        that `content` is uploaded as a normal field, whereas, the field as a file

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
