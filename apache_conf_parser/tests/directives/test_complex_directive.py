import unittest

from apache_conf_parser.directives.complex_directive import ComplexDirective
from apache_conf_parser.directives.simple_directive import SimpleDirective
from apache_conf_parser.exceptions import NodeCompleteError, ParserError, InvalidLineError, NodeMatchError
from apache_conf_parser.nodes.complex_node import ComplexNode


class TestComplexDirective(unittest.TestCase):
    CLASS = ComplexDirective

    def test_not_changed(self):
        node = self.CLASS()
        self.assertFalse(node.changed)

    def test_lines_empty(self):
        node = self.CLASS()
        self.assertEqual(node.lines, [])

    def test_header_ready(self):
        node = self.CLASS()
        self.assertIsInstance(node.header, SimpleDirective)

    def test_header_not_complete(self):
        node = self.CLASS()
        self.assertFalse(node.header.complete)

    def test_body_ready(self):
        node = self.CLASS()
        self.assertIsInstance(node.body, ComplexNode)

    def test_body_not_complete(self):
        node = self.CLASS()
        self.assertFalse(node.body.complete)

    def test_tail_empty(self):
        node = self.CLASS()
        self.assertEqual(node.tail, "")

    def test_tail_not_matched(self):
        node = self.CLASS()
        self.assertFalse(node.tailmatch)

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
        self.assertFalse(self.CLASS.match("name"))

    def test_match_simple_directive_just_name_leading_space(self):
        self.assertFalse(self.CLASS.match(" name"))

    def test_match_simple_directive_just_name_trailing_space(self):
        self.assertFalse(self.CLASS.match("name "))

    def test_match_simple_directive_just_name_continuation(self):
        self.assertFalse(self.CLASS.match("name\\"))

    def test_match_simple_directive_name_and_args(self):
        self.assertFalse(self.CLASS.match("name something else"))

    def test_match_simple_directive_leading_space(self):
        self.assertFalse(self.CLASS.match("   name something else"))

    def test_match_simple_directive_trailing_space(self):
        self.assertFalse(self.CLASS.match("name something else   "))

    def test_match_simple_directive_continuation(self):
        self.assertFalse(self.CLASS.match("name something else\\"))

    def test_match_complex_directive_empty(self):
        self.assertFalse(self.CLASS.match("<>"))

    def test_match_complex_directive_empty_space(self):
        self.assertFalse(self.CLASS.match("< >"))

    def test_match_complex_directive_just_name(self):
        self.assertTrue(self.CLASS.match("<name>"))

    def test_match_complex_directive_just_name_leading_space(self):
        self.assertTrue(self.CLASS.match("< name>"))

    def test_match_complex_directive_just_name_trailing_space(self):
        self.assertTrue(self.CLASS.match("<name >"))

    def test_match_complex_directive_just_name_open(self):
        self.assertFalse(self.CLASS.match("<name"))

    def test_match_complex_directive_just_name_open_continuation(self):
        self.assertTrue(self.CLASS.match("<name\\"))

    def test_match_complex_directive_just_name_open_space_continuation(self):
        self.assertTrue(self.CLASS.match("<name \\"))

    def test_match_complex_directive_just_name_invalid_1(self):
        self.assertFalse(self.CLASS.match("<na+me>"))

    def test_match_complex_directive_just_name_invalid_2(self):
        self.assertFalse(self.CLASS.match("<na<me>"))

    def test_match_complex_directive_name_and_args_open(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2"))

    def test_match_complex_directive_name_and_args_open_continuation(self):
        self.assertTrue(self.CLASS.match("<name arg1 arg2\\"))

    def test_match_complex_directive_name_and_args_open_space_continuation(self):
        self.assertTrue(self.CLASS.match("<name arg1 arg2 \\"))

    def test_match_complex_directive_closed(self):
        self.assertTrue(self.CLASS.match("<name arg1 arg2>"))

    def test_match_complex_directive_leading_space(self):
        self.assertTrue(self.CLASS.match("  <name arg1 arg2>"))

    def test_match_complex_directive_trailing_space(self):
        self.assertTrue(self.CLASS.match("<name arg1 arg2>  "))

    def test_match_complex_directive_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2>\\"))

    def test_match_complex_directive_space_continuation(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2> \\"))

    def test_match_complex_directive_trailing_text(self):
        self.assertFalse(self.CLASS.match("<name arg1 arg2> text"))

    def test_name_header_incomplete(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        self.assertEqual(node.name, "name")

    def test_name_header_complete(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        self.assertEqual(node.name, "name")

    def test_name_complete(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual(node.name, "name")

    def test_args_new(self):
        node = self.CLASS()
        self.assertEqual(node.arguments, [])

    def test_args_header_incomplete(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        self.assertEqual(node.arguments, ["arg1", ])

    def test_args_header_complete_empty(self):
        node = self.CLASS()
        node.add_line("<name>")
        self.assertEqual(node.arguments, [])

    def test_args_header_complete(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        self.assertEqual(node.arguments, ["arg1", ])

    def test_args_complete(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual(node.arguments, ["arg1", ])

    def test_add_line_complete_1(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.complete = True

    def test_add_line_complete_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_3(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        with self.assertRaises(NodeCompleteError):
            node.add_line("extra")

    def test_add_line_complete_4(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("inner argument1 argument2")
        node.add_line("</name>")
        with self.assertRaises(NodeCompleteError):
            node.add_line("")

    def test_add_line_complete_5(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("inner argument1 argument2")
        node.add_line("</name>")
        with self.assertRaises(NodeCompleteError):
            node.add_line("extra")

    def test_add_line_complete_tail_added_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertTrue(node.body.complete)

    def test_add_line_complete_tail_added_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual(node.tail, "</name>")

    def test_add_line_complete_tail_added_3(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertTrue(node.tailmatch)

    # incomplete header
    def test_add_line_incomplete_header_only_name_lines(self):
        node = self.CLASS()
        node.add_line("<name\\")
        self.assertEqual(node.lines[0], "<name\\")

    def test_add_line_incomplete_header_only_name_header_name(self):
        node = self.CLASS()
        node.add_line("<name\\")
        self.assertEqual(node.header.name, "name")

    def test_add_line_incomplete_header_only_name_header_args(self):
        node = self.CLASS()
        node.add_line("<name\\")
        self.assertEqual(node.header.arguments, [])

    def test_add_line_incomplete_header_only_name_lines_multi_1(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1\\")
        self.assertEqual(node.lines[0], "<name\\")

    def test_add_line_incomplete_header_only_name_lines_multi_2(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1\\")
        self.assertEqual(node.lines[1], "arg1\\")

    def test_add_line_incomplete_header_only_name_header_name_multi(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1\\")
        self.assertEqual(node.header.name, "name")

    def test_add_line_incomplete_header_only_name_header_args_multi(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1\\")
        self.assertEqual(node.header.arguments, ["arg1", ])

    def test_add_line_incomplete_header_name_and_arg_lines(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        self.assertEqual(node.lines[0], "<name arg1\\")

    def test_add_line_incomplete_header_name_and_arg_header_name(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        self.assertEqual(node.header.name, "name")

    def test_add_line_incomplete_header_name_and_arg_header_args(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        self.assertEqual(node.header.arguments, ["arg1", ])

    def test_add_line_incomplete_header_name_and_arg_lines_multi_1(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2\\")
        self.assertEqual(node.lines[0], "<name arg1\\")

    def test_add_line_incomplete_header_name_and_arg_lines_multi_2(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2\\")
        self.assertEqual(node.lines[1], "arg2\\")

    def test_add_line_incomplete_header_name_and_arg_header_name_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2\\")
        self.assertEqual(node.header.name, "name")

    def test_add_line_incomplete_header_name_and_arg_header_args_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2\\")
        self.assertEqual(node.header.arguments, ["arg1", "arg2"])

    # complete header
    def test_add_line_complete_header_only_name_lines(self):
        node = self.CLASS()
        node.add_line("<name>")
        self.assertEqual(node.lines[0], "<name>")

    def test_add_line_complete_header_only_name_header_name(self):
        node = self.CLASS()
        node.add_line("<name>")
        self.assertEqual(node.header.name, "name")

    def test_add_line_complete_header_only_name_header_args(self):
        node = self.CLASS()
        node.add_line("<name>")
        self.assertEqual(node.header.arguments, [])

    def test_add_line_complete_header_only_name_lines_multi_1(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1>")
        self.assertEqual(node.lines[0], "<name\\")

    def test_add_line_complete_header_only_name_lines_multi_2(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1>")
        self.assertEqual(node.lines[1], "arg1>")

    def test_add_line_complete_header_only_name_header_name_multi(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1>")
        self.assertEqual(node.header.name, "name")

    def test_add_line_complete_header_only_name_header_args_multi(self):
        node = self.CLASS()
        node.add_line("<name\\")
        node.add_line("arg1>")
        self.assertEqual(node.header.arguments, ["arg1", ])

    def test_add_line_complete_header_name_and_arg_lines(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        self.assertEqual(node.lines[0], "<name arg1>")

    def test_add_line_complete_header_name_and_arg_header_name(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        self.assertEqual(node.header.name, "name")

    def test_add_line_complete_header_name_and_arg_header_args(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        self.assertEqual(node.header.arguments, ["arg1", ])

    def test_add_line_complete_header_name_and_arg_lines_multi_1(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2>")
        self.assertEqual(node.lines[0], "<name arg1\\")

    def test_add_line_complete_header_name_and_arg_lines_multi_2(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2>")
        self.assertEqual(node.lines[1], "arg2>")

    def test_add_line_complete_header_name_and_arg_header_name_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2>")
        self.assertEqual(node.header.name, "name")

    def test_add_line_complete_header_name_and_arg_header_args_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        node.add_line("arg2>")
        self.assertEqual(node.header.arguments, ["arg1", "arg2"])

    # invalid headers
    def test_add_line_incomplete_header_name_and_arg_invalid(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("<name <arg1\\")

    def test_add_line_incomplete_header_name_and_arg_invalid_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        with self.assertRaises(InvalidLineError):
            node.add_line("<arg2\\")

    def test_add_line_complete_header_name_and_arg_invalid(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("<name <arg1>")

    def test_add_line_complete_header_name_and_arg_invalid_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        with self.assertRaises(InvalidLineError):
            node.add_line("<arg2>")

    def test_add_line_complete_header_name_and_arg_invalid_trailing(self):
        node = self.CLASS()
        with self.assertRaises(InvalidLineError):
            node.add_line("<name arg1>extra")

    def test_add_line_complete_header_name_and_arg_invalid_trailing_multi(self):
        node = self.CLASS()
        node.add_line("<name arg1\\")
        with self.assertRaises(InvalidLineError):
            node.add_line("arg2>extra")

    def test_add_line_after_header(self):
        # lines after header don't go into self.lines
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something else")
        self.assertFalse("something else" in node.lines)

    def test_add_line_complete_check_tail(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertFalse("</name>" in node.lines)

    def test_add_line_not_complete_empty_body_check_body(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        self.assertEqual(node.body.nodes, [])

    def test_add_line_not_complete_not_empty_body_check_body(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something else")
        node.add_line("</name>")
        self.assertEqual(len(node.body.nodes), 1)
        self.assertTrue(str(node.body.nodes[0]), "something else")

    def test_add_line_complete_empty_body_check_body(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual(node.body.nodes, [])

    def test_add_line_complete_not_empty_body_check_body(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something else")
        node.add_line("</name>")
        self.assertEqual(len(node.body.nodes), 1)
        self.assertTrue(str(node.body.nodes[0]), "something else")

    def test_add_line_invalid_tail_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        with self.assertRaises(NodeMatchError):
            node.add_line("</name arg1>")

    def test_add_line_invalid_tail_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something else")
        with self.assertRaises(NodeMatchError):
            node.add_line("</name arg1>")

    def test_add_line_body_not_stable_finish_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("  <something else>")
        node.add_line("  </something>")
        node.add_line("</name>")
        self.assertTrue(node.complete)
        self.assertEqual(len(node.body.nodes), 1)

    def test_add_line_body_not_stable_finish_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("  something else\\")
        node.add_line("  finally")
        node.add_line("</name>")
        self.assertTrue(node.complete)
        self.assertEqual(len(node.body.nodes), 1)

    def test_add_line_body_not_stable_close_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("  <something else>")
        with self.assertRaises(NodeCompleteError):
            node.add_line("</name>")

    def test_add_line_body_not_stable_close_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("  something else\\")
        with self.assertRaises(NodeCompleteError):
            node.add_line("</name>")
        self.assertEqual(node.body.nodes[0].arguments[0], "else")

    def test___str___empty(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            str(node)

    def test___str___incomplete_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        with self.assertRaises(NodeCompleteError):
            str(node)

    def test___str___incomplete_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.body.complete = True
        with self.assertRaises(NodeCompleteError):
            str(node)

    def test___str___complete_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual(str(node), "<name arg1>\n</name>")

    def test___str___complete_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("    something here")
        node.add_line("</name>")
        self.assertEqual(str(node), "<name arg1>\n    something here\n</name>")

    def test_complete_1(self):
        node = self.CLASS()
        node.header.name = "name"
        node.header.complete = True
        node.body.complete = True
        node.tailmatch = True
        self.assertTrue(node.complete)

    def test_complete_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("    inner 5")
        node.add_line("</name>")
        self.assertTrue(node.complete)

    def test_complete_new_1(self):
        node = self.CLASS()
        self.assertFalse(node.complete)

    def test_complete_new_2(self):
        node = self.CLASS()
        node.header.complete = False
        node.body.complete = False
        node.tailmatch = False
        self.assertFalse(node.complete)

    def test_complete_order_1(self):
        node = self.CLASS()
        node.header.name = "name"
        node.header.complete = True
        node.body.complete = False
        node.tailmatch = False
        self.assertFalse(node.complete)

    def test_complete_order_2(self):
        node = self.CLASS()
        node.header.name = "name"
        node.header.complete = True
        node.body.complete = True
        node.tailmatch = False
        self.assertFalse(node.complete)

    def test_complete_order_3(self):
        node = self.CLASS()
        node.header.name = "name"
        node.header.complete = True
        node.body.complete = False
        node.tailmatch = True
        with self.assertRaises(NodeCompleteError):
            node.complete

    def test_complete_order_4(self):
        node = self.CLASS()
        node.header.complete = False
        node.body.complete = False
        node.tailmatch = True
        with self.assertRaises(NodeCompleteError):
            node.complete

    def test_complete_order_5(self):
        node = self.CLASS()
        node.header.complete = False
        node.body.complete = True
        node.tailmatch = False
        with self.assertRaises(NodeCompleteError):
            node.complete

    def test_complete_order_6(self):
        node = self.CLASS()
        node.header.complete = False
        node.body.complete = True
        node.tailmatch = True
        with self.assertRaises(NodeCompleteError):
            node.complete

    def test_str_method_new_complex_directive(self):
        directive = ComplexDirective()
        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an uninitialized simple directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_name_property(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args>'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        expected = test_directive_name
        actual = directive.name
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected name property to be {}, received: {}'.format(expected, actual),
        )

    def test_arguments_property(self):
        directive = ComplexDirective()
        test_arguments = 'some args'
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args>'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        expected = test_arguments.split()
        actual = directive.arguments
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected arguments property to be {}, received: {}'.format(expected, actual),
        )

    def test_angle_brackes_in_directive_header(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args </{name}>'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        with self.assertRaises(InvalidLineError) as err:
            for test_line in test_lines:
                directive.add_line(test_line)
            expected_err_msg = 'Angle brackets not allowed in complex directive header.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_body_stable_check(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args </{name}>'.format(name=test_directive_name),
            'Redirect here \\',
            'there',
            '</{name}>'.format(name=test_directive_name),
        ]
        with self.assertRaises(InvalidLineError) as err:
            for test_line in test_lines:
                directive.add_line(test_line)
            expected_err_msg = 'Angle brackets not allowed in complex directive header.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_add_line_to_complete_node(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            '</{name}>'.format(name=test_directive_name),
            'Redirect here there',
        ]
        with self.assertRaises(NodeCompleteError) as err:
            for test_line in test_lines:
                directive.add_line(test_line)
            expected_err_msg = "Can't add lines to a complete Node."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_set_complete_after_all_complete(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)

        directive.complete = True

        expected = True
        actual = directive.complete
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected complete property to be {}, received: {}'.format(expected, actual),
        )

    def test_body_complete_before_header(self):
        directive = ComplexDirective()
        directive.body.complete = True

        with self.assertRaises(NodeCompleteError) as err:
            directive.complete
            expected_err_msg = "Body is complete but header isn't."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_header_with_extraneous_tail(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_line = '<{name} some args> hir>'.format(name=test_directive_name)

        # TODO, see if we can do an assert calls on that complete.fset(self, val) call
        with self.assertRaises(InvalidLineError) as err:
            # for test_line in test_lines:
            directive.parse_header(test_line)
            expected_err_msg = "Directive header has an extraneous tail:"
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_set_not_complete_after_all_complete(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        with self.assertRaises(NodeCompleteError) as err:
            directive.complete = False
            expected_err_msg = "Cannot set a complex directive to not complete if its parts are all complete"
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_no_closing_tag_after_body_complete(self):
        directive = ComplexDirective()
        directive.add_line('<ImmaComplexDirective some args >')
        # contrived body.complete set to true
        directive.body.complete = True

        test_line = 'Redirect here there'
        with self.assertRaises(InvalidLineError) as err:
            directive.add_line(test_line),
            expected_err_msg = "Expecting closing tag. Got:"
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_tail_match_before_body_complete(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            '<{name}too some args >'.format(name=test_directive_name),
            'Redirect here there',
        ]

        for test_line in test_lines:
            directive.add_line(test_line)

        # TODO: would this ever happen "naturally"
        directive.tailmatch = True
        with self.assertRaises(NodeCompleteError) as err:
            print('tailmatcher', directive.tailmatch, directive.body.complete, directive.complete)
            directive.complete
            expected_err_msg = "TTail is matched but body is not complete."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised InvalidLineError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_add_invalid_line(self):
        directive = ComplexDirective()
        test_line = '!!ImmaComplexDirective !@#$ on'
        with self.assertRaises(ParserError) as err:
            directive.add_line(test_line)
            expected_err_msg = 'Unable to match line.'
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised ParserError exception message, received: {}'.format(expected_err_msg,
                                                                                                     err),
            )

    def test_str_magic_method_after_adding_line(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
            '</{name}>'.format(name=test_directive_name),
        ]
        for test_line in test_lines:
            directive.add_line(test_line)
        expected = '\n'.join(test_lines)
        actual = str(directive)
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected directive str representation to be {}, received: {}'.format(expected, actual),
        )

    def test_str_magic_method_with_incomplete_directive(self):
        directive = ComplexDirective()
        test_directive_name = 'ImmaComplexDirective'
        test_lines = [
            '<{name} some args >'.format(name=test_directive_name),
            'Redirect here there',
        ]
        for test_line in test_lines:
            directive.add_line(test_line)

        with self.assertRaises(NodeCompleteError) as err:
            str(directive)
            expected_err_msg = "Can't turn an incomplete complex directive into a string."
            self.assertIn(
                member=expected_err_msg,
                container=err,
                msg='Expected "{}" in the raised NodeCompleteError exception message, received: {}'.format(
                    expected_err_msg, err),
            )

    def test_dumps_new(self):
        node = self.CLASS()
        with self.assertRaises(NodeCompleteError):
            node.dumps()

    def test_dumps_header_only(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        with self.assertRaises(NodeCompleteError):
            node.dumps()

    def test_dumps_not_complete(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something else")
        with self.assertRaises(NodeCompleteError):
            node.dumps()

    def test_dumps_depth_0(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n</name>", node.dumps(0))

    def test_dumps_depth_0_spaces(self):
        node = self.CLASS()
        node.add_line("<name     arg1>")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n</name>", node.dumps(0))

    def test_dumps_depth_0_tab(self):
        node = self.CLASS()
        node.add_line("<name	arg1>")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n</name>", node.dumps(0))

    def test_dumps_depth_0_nested(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something here")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n" + ComplexDirective.indent_str + "something here\n</name>", node.dumps(0))

    def test_dumps_depth_0_nested_indent_stred_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("  something here")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n" + ComplexDirective.indent_str + "something here\n</name>", node.dumps(0))

    def test_dumps_depth_0_nested_indent_stred_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("    something here")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n" + ComplexDirective.indent_str + "something here\n</name>", node.dumps(0))

    def test_dumps_depth_1(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual("%s<name arg1>\n%s</name>" % ((ComplexDirective.indent_str,) * 2), node.dumps(1))

    def test_dumps_depth_1_nested(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something here")
        node.add_line("</name>")
        self.assertEqual("%s<name arg1>\n%s%ssomething here\n%s</name>" % ((ComplexDirective.indent_str,) * 4),
                         node.dumps(1))

    def test_dumps_depth_1_nested_indent_stred(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("    something here")
        node.add_line("</name>")
        self.assertEqual("%s<name arg1>\n%s%ssomething here\n%s</name>" % ((ComplexDirective.indent_str,) * 4),
                         node.dumps(1))

    def test_dumps_depth_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("</name>")
        self.assertEqual("%s%s<name arg1>\n%s%s</name>" % ((ComplexDirective.indent_str,) * 4), node.dumps(2))

    def test_dumps_leading_space_1(self):
        node = self.CLASS()
        node.add_line("  <name arg1>")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n</name>", node.dumps())

    def test_dumps_leading_space_2(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("  </name>")
        self.assertEqual("<name arg1>\n</name>", node.dumps())

    def test_dumps_leading_space_3(self):
        node = self.CLASS()
        node.add_line("<name arg1>")
        node.add_line("something else")
        node.add_line("</name>")
        self.assertEqual("<name arg1>\n%ssomething else\n</name>" % ComplexDirective.indent_str, node.dumps())


if __name__ == '__main__':
    unittest.main()
