#!/usr/bin/env python
import unittest

from parameterized import parameterized

from apache_conf_parser.directives.rewrite_base import RewriteBase


class TestRewriteBase(unittest.TestCase):

    @parameterized.expand([
        ("normal", 'RewriteBase /some/path', '/some/path'),
    ])
    def test_matches_valid_directives(self, name, directive_line, expected_url_path):
        directive = RewriteBase()
        directive.add_line(directive_line)
        self.assertIsNotNone(
            obj=directive.matches,
            msg='Directive expected to match RewriteBase for "%s" ("%s"), it did not match.' % (name, directive_line)
        )

        actual_url_path = directive.url_path
        self.assertEqual(
            first=actual_url_path,
            second=actual_url_path,
            msg='url_path attribute for RewriteBase returned unexpected value: "%s". Expected: "%s".' % (expected_url_path, actual_url_path)
        )

    @parameterized.expand([
        ("wrong directive name", 'Redirect /some/path'),
    ])
    def test_does_not_match_invalid_directives(self, name, directive_line):
        directive = RewriteBase()
        directive.add_line(directive_line)
        self.assertIsNone(
            obj=directive.matches,
            msg='Directive not expected to match RewriteBase for "%s" ("%s"), it did match.' % (name, directive_line)
        )


if __name__ == '__main__':
    unittest.main()
