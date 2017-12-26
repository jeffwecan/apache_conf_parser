

from unittest import TestCase

from apache_conf_parser.directives.simple_directive import SimpleDirective
from apache_conf_parser.exceptions import NodeCompleteError, ParserError, InvalidLineError, DirectiveError


class TestSimpleDirective(TestCase):

    def test_str_method_new_simple_directive(self):
        directive = SimpleDirective()
        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an uninitialized simple directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line(self):
        directive = SimpleDirective()
        test_line = 'ImmaSimpleDirective on'
        directive.add_line(test_line)
        expected = [test_line]
        actual = directive.lines
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected lines attribute to be {}, received: {}'.format(expected, actual),
        )

    def test_add_to_header_when_already_complete(self):
        directive = SimpleDirective()
        # set a test name so our directive is marked as "stable"
        test_name = 'ImmaDirective'
        directive.name = test_name
        directive.complete = True
        test_header_line = 'RewriteEngine	on'
        with self.assertRaises(NodeCompleteError) as err:
            directive.parse_directive_header(test_header_line)
            expected_err_msg = 'Cannot add to the header of a complete directive.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_to_header_with_none_as_arg(self):
        directive = SimpleDirective()
        test_header_line = None
        with self.assertRaises(DirectiveError) as err:
            directive.parse_directive_header(test_header_line)
            expected_err_msg = 'An empty line is not a valid header line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised DirectiveError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_to_header_with_trailing_backslash_in_line(self):
        directive = SimpleDirective()
        test_header_line = 'RewriteEngine	on\\'
        directive.parse_directive_header(test_header_line)
        expected_argument = 'on'
        actual_argument = directive.arguments[0]
        self.assertEqual(
            first=expected_argument,
            second=actual_argument,
            msg='Expected first argument for directive to be {}, received: {}'.format(expected_argument, actual_argument),
        )

    def test_set_name_twice(self):
        directive = SimpleDirective()
        test_name = 'ImmaSimpleDirective'
        directive.name = test_name
        with self.assertRaises(DirectiveError) as err:
            directive.name = test_name
            expected_err_msg = "Name is already set."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised DirectiveError exception message, received: {}'.format(expected_err_msg, err),
            )
        # expected = [test_line]
        # actual = directive.lines
        # self.assertEqual(
        #     first=expected,
        #     second=actual,
        #     msg='Expected lines attribute to be {}, received: {}'.format(expected, actual),
        # )

    def test_add_invalid_line(self):
        directive = SimpleDirective()
        test_line = '!!ImmaSimpleDirective !@#$ on'
        with self.assertRaises(ParserError) as err:
            directive.add_line(test_line)
            expected_err_msg = 'Unable to match line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised ParserError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_add_line_with_none_as_arg(self):
        directive = SimpleDirective()
        test_header_line = None
        with self.assertRaises(InvalidLineError) as err:
            directive.add_line(test_header_line)
            expected_err_msg = 'An empty line is not a valid header line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_set_unstable_directive_to_complete(self):
        directive = SimpleDirective()
        with self.assertRaises(NodeCompleteError) as err:
            directive.complete = True
            expected_err_msg = "Can't set an unstable Directive to complete."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_str_magic_method_after_adding_line(self):
        directive = SimpleDirective()
        test_line = 'ImmaSimpleDirective on'
        directive.add_line(test_line)
        expected = test_line
        actual = str(directive)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive str representation to be {}, received: {}'.format(expected, actual),
        )

    def test_content_property_new_directive(self):
        directive = SimpleDirective()

        with self.assertRaises(NodeCompleteError) as err:
            directive.content
            expected_err_msg = 'Name has not been set yet.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(expected_err_msg, err),
            )

    def test_repr_magic_method(self):
        directive = SimpleDirective()
        test_name = 'ImmaDirective'
        directive.name = test_name
        expected = '<%s Directive at %s>' % (test_name, id(directive))
        actual = repr(directive)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive __repr__ method to return {}, received: {}'.format(expected, actual),
        )

    def test_content_property_after_setting_name(self):
        directive = SimpleDirective()
        test_name = 'ImmaDirective'
        directive.name = test_name
        expected = test_name
        actual = directive.content
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive content property to be {}, received: {}'.format(expected, actual),
        )
