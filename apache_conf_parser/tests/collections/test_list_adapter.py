#!/usr/bin/env python
import unittest

from apache_conf_parser.collections.list_adapter import ListAdapter


class TestListAdapter(unittest.TestCase):

    def test___init___empty_2(self):
        iterable = []
        self.assertEqual(list(ListAdapter(*iterable)), [])

    def test___init___plain(self):
        self.assertEqual(list(ListAdapter(1, 2)), [1, 2])

    def test___init___list(self):
        iterable = [1, 2]
        self.assertEqual(list(ListAdapter(*iterable)), [1, 2])

    def test___init___tuple(self):
        iterable = (1, 2)
        self.assertEqual(list(ListAdapter(*iterable)), [1, 2])

    def test___init___generator(self):
        iterable = (x for x in [1, 2])
        self.assertEqual(list(ListAdapter(*iterable)), [1, 2])

    def test___init___lc(self):
        iterable = [x for x in [1, 2]]
        self.assertEqual(list(ListAdapter(*iterable)), [1, 2])

    def test___init___items(self):
        la = ListAdapter(1, 2)
        self.assertEqual(la.items, [1, 2])

    def test___len___empty(self):
        la = ListAdapter()
        self.assertEqual(len(la), 0)

    def test___len___not_empty(self):
        la = ListAdapter(1, 2)
        self.assertEqual(len(la), 2)

    def test___contains___empty(self):
        la = ListAdapter()
        self.assertFalse(1 in la)

    def test___contains___not_empty(self):
        la = ListAdapter(1, 2)
        self.assertTrue(1 in la)

    def test_instantiation(self):
        list_adapter = ListAdapter()
        expected = []
        actual = list_adapter.items
        self.assertEqual(
            first=expected,
            second=actual,
            msg='New list adapter expected to contain an empty list in items attribute, found: %s' % actual
        )

    def test_instantiation_with_items(self):
        test_items = [1, 2, 3]
        list_adapter = ListAdapter(*test_items)
        expected = test_items
        actual = list_adapter.items
        self.assertEqual(
            first=expected,
            second=actual,
            msg='New list adapter expected to contain list of initial args in items attribute, found: %s' % actual
        )

    def test_contains_value(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = test_item in list_adapter
        self.assertTrue(
            expr=actual,
            msg='Expected list_adapter contains magic method to return True for value: %s' % test_item
        )

    def test_set_item(self):
        test_item = 2
        list_adapter = ListAdapter(1)
        list_adapter[0] = test_item
        expected = test_item
        actual = list_adapter[0]
        self.assertEqual(
            first=expected,
            second=actual,
            msg='Expected item at index 0 to be set to %s, found: %s' % (expected, actual)
        )

    def test_del_item(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        del list_adapter[0]
        actual = test_item in list_adapter
        self.assertFalse(
            expr=actual,
            msg='Expected list_adapter contains magic method to return False for value: %s' % test_item
        )
        with self.assertRaises(IndexError):
            assert list_adapter[0]

    def test_ne(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = list_adapter != list_adapter
        self.assertFalse(
            expr=actual,
            msg='Expected list_adapter to be equal to itself'
        )

    def test_lt(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = list_adapter < ListAdapter()
        self.assertFalse(
            expr=actual,
            msg='Expected empty list_adapter to be less than one containing items'
        )

    def test_lte(self):
        test_item = 1
        list_adapter = ListAdapter(test_item)
        actual = (list_adapter <= list_adapter)
        self.assertTrue(
            expr=actual,
            msg='Expected list_adapter to be less than or equal to itself'
        )


if __name__ == '__main__':
    unittest.main()
