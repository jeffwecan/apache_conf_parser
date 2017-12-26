#!/usr/bin/env python
import unittest
from unittest.mock import patch, mock_open

from apache_conf_parser import ApacheConfParser
from apache_conf_parser.exceptions import NodeCompleteError


class TestApacheConfParser(unittest.TestCase):

    def test_read_conf_from_string(self):
        test_content = 'Redirect here there'
        apache_conf_parser = ApacheConfParser(test_content, infile=False)
        expected = test_content
        actual = str(apache_conf_parser)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected str(apache_conf_parser) to return %s, received: %s' % (expected, actual)
        )

    def test_parse_twice(self):
        test_content = 'Redirect here there'
        apache_conf_parser = ApacheConfParser(test_content, infile=False)
        apache_conf_parser.parse()
        expected = test_content
        actual = str(apache_conf_parser)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected str(apache_conf_parser) to return %s, received: %s' % (expected, actual)
        )

    def test_read_conf_from_file(self):
        test_path = '/some/test/path/.htaccess'
        test_content = 'Redirect here there'
        with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
            apache_conf_parser = ApacheConfParser(test_path)
            expected = test_content
            actual = str(apache_conf_parser)
            self.assertEqual(
                first=expected,
                second=actual,
                msg='Expected str(apache_conf_parser) to return %s, received: %s' % (expected, actual)
            )

        mock_file.assert_called_with(test_path)

    def test_read_conf_from_string_with_delay(self):
        apache_conf_parser = ApacheConfParser('Redirect here there', infile=False, delay=True)
        with self.assertRaises(NodeCompleteError) as err:
            str(apache_conf_parser)
            expected_err_msg = "Can't turn an incomplete complex node into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )


if __name__ == '__main__':
    unittest.main()
