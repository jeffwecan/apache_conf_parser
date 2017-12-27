#!/usr/bin/env python
import unittest

from apache_conf_parser.directives.simple_directive import SimpleDirective
from apache_conf_parser.exceptions import NodeCompleteError, ParserError, InvalidLineError, DirectiveError


class TestSimpleDirective(unittest.TestCase):
    CLASS = SimpleDirective

    def test_not_complete(self):
        node = self.CLASS()
        self.assertFalse(node.complete)

    def test_not_changed(self):
        node = self.CLASS()
        self.assertFalse(node.changed)

    def test_lines_empty(self):
        node = self.CLASS()
        self.assertEqual(node.lines, [])

    def test_match_None(self):
        self.assertFalse(self.CLASS.match(None))

    def test_match_empty(self):
        self.assertFalse(self.CLASS.match(""))

    def test_match_comment_solo(self):
        self.assertFalse(self.CLASS.match("#"))

    def test_match_comment_solo_space(self):
        self.assertFalse(self.CLASS.match(" #"))

    def test_match_comment_space(self):
        self.assertFalse(self.CLASS.match(" # this is a comment"))

    def test_match_comment_no_space(self):
        self.assertFalse(self.CLASS.match("# this is a comment"))

    def test_match_comment_continuation(self):
        self.assertFalse(self.CLASS.match("# this is a comment\\"))

    def test_match_blank_spaces(self):
        self.assertFalse(self.CLASS.match("   "))

    def test_match_blank_tabs(self):
        self.assertFalse(self.CLASS.match("		"))

    def test_match_blank_continuation(self):
        self.assertFalse(self.CLASS.match("   \\"))

    def test_match_simple_directive_just_name(self):
        self.assertTrue(self.CLASS.match("name"))

    def test_match_simple_directive_just_name_leading_space(self):
        self.assertTrue(self.CLASS.match(" name"))

    def test_match_simple_directive_just_name_trailing_space(self):
        self.assertTrue(self.CLASS.match("name "))

    def test_match_simple_directive_just_name_continuation(self):
        self.assertTrue(self.CLASS.match("name\\"))

    def test_match_simple_directive_name_and_args(self):
        self.assertTrue(self.CLASS.match("name something else"))

    def test_match_simple_directive_leading_space(self):
        self.assertTrue(self.CLASS.match("   name something else"))

    def test_match_simple_directive_trailing_space(self):
        self.assertTrue(self.CLASS.match("name something else   "))

    def test_match_simple_directive_continuation(self):
        self.assertTrue(self.CLASS.match("name something else\\"))

    def test_match_complex_directive_empty(self):
        self.assertFalse(self.CLASS.match("<>"))

    def test_match_complex_directive_empty_space(self):
        self.assertFalse(self.CLASS.match("< >"))

    def test_match_complex_directive_just_name(self):
        self.assertFalse(self.CLASS.match("<name>"))

    def test_match_complex_directive_just_name_leading_space(self):
        self.assertFalse(self.CLASS.match("< name>"))

    def test_match_complex_directive_just_name_trailing_space(self):
        self.assertFalse(self.CLASS.match("<name >"))

    def test_match_complex_directive_just_name_open(self):
        self.assertFalse(self.CLASS.match("<name"))

    def test_match_complex_directive_just_name_open_continuation(self):
        self.assertFalse(self.CLASS.match("<name\\"))

    def test_match_complex_directive_just_name_open_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name \\"))

    def test_match_complex_directive_just_name_invalid_1(self):
        self.assertFalse(self.CLASS.match("<na+me>"))

    def test_match_complex_directive_just_name_invalid_2(self):
        self.assertFalse(self.CLASS.match("<na<me>"))

    def test_match_complex_directive_name_and_args_open(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2"))

    def test_match_complex_directive_name_and_args_open_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2\\"))

    def test_match_complex_directive_name_and_args_open_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2 \\"))

    def test_match_complex_directive_closed(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>"))

    def test_match_complex_directive_leading_space(self):
        self.assertFalse(self.CLASS.match("  <name arg1 arg2>"))

    def test_match_complex_directive_trailing_space(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>  "))

    def test_match_complex_directive_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>\\"))

    def test_match_complex_directive_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2> \\"))

    def test_match_complex_directive_trailing_text(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2> text"))

    def test___str___empty(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            str(node)

    def test___str___multiple(self):
        line1 = "name arg1\\"
        line2 = "arg2 arg3"
        node = self.CLASS()
        node.add_line(line1)
        node.add_line(line2)
        self.assertEqual(line1 + "\n" + line2, str(node))

    def test___str___new(self):
        line = "name"
        node = self.CLASS()
        node.add_line(line)
        self.assertEqual(line, str(node))

    def test___str___changed_1(self):
        line = "name"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual(line, str(node))

    def test___str___changed_2(self):
        line = "name arg1"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual(line, str(node))

    def test___str___changed_3(self):
        line = "    name"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual("name", str(node))

    def test___str___changed_4(self):
        line = "    name arg1"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual("name arg1", str(node))

    def test___str___changed_5(self):
        line = "    name	arg1"
        node = self.CLASS()
        node.add_line(line)
        node.changed = True
        self.assertEqual("name arg1", str(node))

    def test_add_line_complete_1(self):
        node = self.CLASS()
        node.name = "name"
        node.complete = True
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_2(self):
        node = self.CLASS()
        node.add_line("name arg1")
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_3(self):
        node = self.CLASS()
        node.add_line("name arg1")
        with self.assertRaises(NodeCompleteError):
            node.add_line("arg2 arg3")

    def test_add_line_incomplete_header_name_and_arg_bracket_arg(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("name <arg1\\")

    def test_add_line_incomplete_header_name_and_arg_bracket_arg_multi(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        with self.assertRaises(InvalidLineError):
            node.add_line("<arg2\\")
        self.assertEqual(node.arguments[0], "arg1")

    def test_add_line_complete_header_name_and_arg_bracket_arg_1(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("name <arg1")

    def test_add_line_complete_header_name_and_arg_bracket_arg_2(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("name arg1>")

    def test_add_line_complete_header_name_and_arg_bracket_arg_multi_1(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        with self.assertRaises(InvalidLineError):
            node.add_line("<arg2")
        self.assertEqual(node.arguments[0], "arg1")

    def test_add_line_complete_header_name_and_arg_bracket_arg_multi_2(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        with self.assertRaises(InvalidLineError):
            node.add_line("arg2>")
        self.assertEqual(node.arguments[0], "arg1")

    def test_add_line_added_first(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertEqual(node.lines[0], "name arg1")

    def test_add_line_added_second_1(self):
        node = self.CLASS()
        node.add_line("name arg1")
        node.complete = False
        node.add_line("arg2")
        self.assertEqual(node.lines[0], "name arg1")
        self.assertEqual(node.lines[1], "arg2")

    def test_add_line_added_second_2(self):
        node = self.CLASS()
        node.add_line("name arg1")
        node.complete = False
        node.add_line("arg2 ")
        self.assertEqual(node.lines[0], "name arg1")
        self.assertEqual(node.lines[1], "arg2 ")

    def test_add_line_autocomplete(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertTrue(node.complete)

    def test_add_line_autochanged(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertFalse(node.changed)

    def test_add_line_continuation_1(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        self.assertFalse(node.complete)

    def test_add_line_continuation_2(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        node.add_line("arg2\\")
        self.assertFalse(node.complete)

    def test_add_line_continuation_3(self):
        node = self.CLASS()
        node.add_line("name arg1\\")
        node.add_line("arg2")
        self.assertTrue(node.complete)

    def test_add_line_space_continuation(self):
        node = self.CLASS()
        node.add_line("name arg1 \\")
        self.assertFalse(node.complete)

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

    def test_dumps_depth_0(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertEqual("name arg1", node.dumps(0))
    def test_dumps_depth_1(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertEqual(self.CLASS().indent_str+"name arg1", node.dumps(1))
    def test_dumps_depth_2(self):
        node = self.CLASS()
        node.add_line("name arg1")
        self.assertEqual(self.CLASS().indent_str*2+"name arg1", node.dumps(2))


if __name__ == '__main__':
    unittest.main()
