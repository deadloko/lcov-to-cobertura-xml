#!/usr/bin/env python

# Copyright 2011-2012 Eric Wendelin
#
# This is free software, licensed under the Apache License, Version 2.0,
# available in the accompanying LICENSE.txt file.

import unittest

from lcov_cobertura import LcovCobertura


class Test(unittest.TestCase):
    """Unit tests for lcov_cobertura."""

    def test_parse(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nend_of_record\n')
        result = converter.parse()
        self.assertTrue('packages' in result)
        self.assertTrue('foo' in result['packages'])
        self.assertEqual(result['packages']['foo']['branches-covered'], 1)
        self.assertEqual(result['packages']['foo']['branches-total'], 2)
        self.assertEqual(result['packages']['foo']['branch-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['line-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext'][
                             'branches-covered'], 1)
        self.assertEqual(result['packages']['foo']['classes']['foo/file.ext'][
                             'branches-total'], 2)
        self.assertEqual(
            result['packages']['foo']['classes']['foo/file.ext']['methods'],
            {})

    def test_parse_with_functions(self):
        converter = LcovCobertura(
            'TN:\nSF:foo/file.ext\nDA:1,1\nDA:2,0\nFN:1,(anonymous_1)\nFN:2,namedFn\nFNDA:1,(anonymous_1)\nend_of_record\n')
        result = converter.parse()
        self.assertEqual(result['packages']['foo']['line-rate'], '0.5')
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)
        self.assertEqual(
            result['packages']['foo']['classes']['foo/file.ext']['methods'][
                '(anonymous_1)'], ['1', '1'])
        self.assertEqual(
            result['packages']['foo']['classes']['foo/file.ext']['methods'][
                'namedFn'], ['2', '0'])

    def test_exclude_package_from_parser(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,1\nDA:2,0\nend_of_record\nSF:bar/file.ext\nDA:1,1\nDA:2,1\nend_of_record\n',
            '.',
            'foo')
        result = converter.parse()
        self.assertTrue('foo' not in result['packages'])
        self.assertTrue('bar' in result['packages'])
        # Verify that excluded package did not skew line coverage totals
        self.assertEqual(result['packages']['bar']['line-rate'], '1.0')

    def test_generate_cobertura_xml(self):
        converter = LcovCobertura(
            'TN:\nSF:foo/file.ext\nDA:1,1\nDA:2,0\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nFN:1,(anonymous_1)\nFN:2,namedFn\nFNDA:1,(anonymous_1)\nend_of_record\n')
        parsed_lcov = {'packages': {
            'foo': {'branches-covered': 1, 'line-rate': '0.5',
                    'branch-rate': '0.5',
                    'lines-covered': 1, 'branches-total': 2, 'lines-total': 2,
                    'classes': {
                        'Bar': {'branches-covered': 1, 'lines-covered': 1,
                                'branches-total': 2,
                                'methods': {
                                    '(anonymous_1)': ['1', '1'],
                                    'namedFn': ['2', '0']
                                },
                                'lines': {
                                    1: {'hits': '1', 'branches-covered': 1,
                                        'branches-total': 2, 'branch': 'true'},
                                    2: {'hits': '0', 'branches-covered': 0,
                                        'branches-total': 0, 'branch': 'false'}
                                },
                                'lines-total': 2, 'name': 'file.ext'}},
                    }},
            'summary': {'branches-covered': 1, 'branches-total': 2,
                        'lines-covered': 1, 'lines-total': 2},
            'timestamp': '1346815648000'}
        xml = converter.generate_cobertura_xml(parsed_lcov)

        with open('cobertura_reference.xml', 'r') as cobertura_reference:
            self.assertEqual(xml, cobertura_reference.read())

    def test_treat_non_integer_line_execution_count_as_zero(self):
        converter = LcovCobertura(
            'SF:foo/file.ext\nDA:1,=====\nDA:2,2\nBRDA:1,1,1,1\nBRDA:1,1,2,0\nend_of_record\n')
        result = converter.parse()
        self.assertEqual(result['packages']['foo']['lines-covered'], 1)
        self.assertEqual(result['packages']['foo']['lines-total'], 2)


if __name__ == '__main__':
    unittest.main()
