import unittest
from unittest import TestCase

from pyspass import HtmlForm, HtmlDiv


class TestHtmlForm(TestCase):

    def setUp(self):
        pass

    def test_get_form_with_no_parent(self):
        div = HtmlDiv()
        self.assertEqual(div.get_form(), None)

    def test_get_form_with_no_parent_form(self):
        div_outer = HtmlDiv('outer_div')
        div = div_outer.div()
        self.assertEqual(div.get_form(), None)

    def test_error_on_nested_forms_for_nonform(self):
        form_outer = HtmlForm('outer_form')
        div = form_outer.div()
        form_inner = div.form('inner_form')
        div_sub = form_inner.div()
        with self.assertRaises(Exception):
            div_sub.get_form()

    def test_error_on_nested_forms_for_form(self):
        form_outer = HtmlForm('outer_form')
        div = form_outer.div()
        form_inner = div.form('inner_form')
        with self.assertRaises(Exception):
            form_inner.get_form()


if __name__ == '__main__':
    unittest.main()
