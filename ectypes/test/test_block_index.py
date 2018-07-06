#!/usr/bin/env python2
# coding: utf-8

import unittest

from pykit import ectypes
from pykit import ututil
from pykit.ectypes import BlockIndex

dd = ututil.dd


class TestBlockIndex(unittest.TestCase):

    def test_parse_invalid(self):
        cases = (
            '',
            'a',
            '0',
            '00',
            '000',
            '000a',
            'a000',
        )

        for bad in cases:
            self.assertRaises(ectypes.BlockIndexError, ectypes.BlockIndex.parse, bad)

    def test_parse(self):

        cases = (
                ('0000', (0, 0)),
                ('0001', (0, 1)),
                ('0101', (1, 1)),
                ('1234', (12, 34)),
                (BlockIndex(12, 34), (12, 34)),
        )

        for inp, expected in cases:
            dd(inp)
            dd(expected)

            rst = ectypes.BlockIndex.parse(inp)
            self.assertEqual(expected, rst)

    def test_new_invalid(self):

        cases = (
            (-1, 0),
            (100, 0),
            (0, -1),
            (0, 100),
        )

        for i, j in cases:
            dd(i, j)
            self.assertRaises(ectypes.BlockIndexError, ectypes.BlockIndex, i, j)
