<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
#   Table of Content

- [Name](#name)
- [Status](#status)
- [Synopsis](#synopsis)
- [Description](#description)
- [Exception](#exceptions)
  - [httpmultipart.MultipartError](#httpmultipartmultiparterror)
  - [httpmultipart.InvalidArgumentError](#httpmultipartinvalidArgumenterror)
- [Constants](#constants)
  - [httpmultipart.MultipartObject.boundary](#httpmultipartmultipartobjectboundary)
- [Classes](#classes)
  - [httpmultipart.MultipartObject](httpmultipartmultipartobject)
- [Methods](#methods)
  - [httpmultipart.make_headers](#httpmultipartmake_headers)
  - [httpmultipart.make_body_reader](#httpmultipartmake_body_reader)
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

headers = {
    'Content-Type: multipart/form-data; boundary=${bound}'
}

key_value_pair = {
    'metadata1':
    {
        'value': 'lvting'
    },
    'metadata2':
    {
        'value': ['/root/tmp/a.txt', 'a.txt'],
        'headers': {'Content-Type': 'application/octet-stream'}
    },
    'metadata3':
    {
        'value': ['/root/tmp/b.txt']
    },
}

print httpmultipart.make_headers(key_value_pair, header)
```

```python
from pykit import httpmultipart

key_value_pair = {
    'metadata1':
    {
        'value': 'lvting'
    },
    'metadata2':
    {
        'value': ['/root/tmp/a.txt', 'a.txt'],
        'headers': {'Content-Type': 'application/octet-stream'}
    },
    'metadata3':
    {
        'value': ['/root/tmp/b.txt']
    },
}

body_reader = httpmultipart.make_body_reader(key_value_pair)
data = []

for body in body_reader:
    data.append(body)

print ''.join(data)
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
##  httpmultipart.MultipartObject.make_body_reader

**syntax**:
`httpmultipart.MultipartObject.make_headers`

Return a header according to the key_value_pair and headers

Examples:
```
print httpmultipart.make_headers(key_value_pair, header)
```
**arguments**:

-  `key_value_pair`:
   a `dict`(`field_name`, `filed`) is used in body after multipart encoding

   - `field_name`:
   It's a str that represents each field name

   - `field`
   It's a dict, and the dict includes both the value and headers elements,
   value can be a str or a list, str refers to the field being uploaded as a
   str, and the `list`(`file_path`, `file_name`) indicates that the field is
   uploaded as a file; headers elements must contain Content-Disposition,and if the file
   is uploaded, it must also have Content-Type
     - `file_path`:
     upload the path to the file
     - `file_name`:
     upload the name about the file, the argument can also be None

-  `headers`:
   a `dict`(`header_name`, `header_value`) of http request headers
   It's a default argument and its default value is None

**return**:
dict about headers

`httpmultipart.MultipartObject.make_body_reader`

Return a body after multipart encoding according to the key_value_pair

Examples:
```
body_reader = httpmultipart.make_body_reader(key_value_pair)
data = []

for body in body_reader:
    data.append(body)
print ''.join(data)
```
**arguments**:

-  `key_value_pair`:
   a `dict`(`field_name`, `filed`) is used in body after multipart encoding

   - `field_name`:
   It's a str that represents each field name

   - `field`
   It's a dict, and the dict includes both the value and headers elements,
   value can be a str or a list, str refers to the field being uploaded as a
   str, and the `list`(`file_path`, `file_name`) indicates that the field is
   uploaded as a file; headers elements must contain Content-Disposition,and if the file
   is uploaded, it must also have Content-Type
     - `file_path`:
     upload the path to the file
     - `file_name`:
     upload the name about the file,the argument can also be None

**return**:
generator about body after multipart encoding

#   Author

Ting Lv(吕婷) <ting.lv@baishancloud.com>

#   Copyright and License

The MIT License (MIT)

Copyright (c) 2017 Ting Lv(吕婷) <ting.lv@baishancloud.com>
