import unittest
from unittest import TestCase

from pyspass import HtmlSelect, HtmlDiv


class TestHtmlSelect(TestCase):

    def setUp(self):
        self.content_as_dict = [{'column_1': 1, 'column_2': 2}]

    def test_dropdown_with_content_as_dict(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', {'A': 'Code A', 'B': 'Code B'})
        self.assertIn('<option value="A">Code A</option>', str(drop))
        self.assertIn('<option value="B">Code B</option>', str(drop))

    def test_dropdown_with_content_as_list(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B'])
        self.assertIn('<option value="A">A</option>', str(drop))
        self.assertIn('<option value="B">B</option>', str(drop))

    def test_dropdown_with_content_as_list_and_input_asaw_str(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input='B')
        self.assertIn('<option value="B" selected="selected">B</option>', str(drop))

    def test_dropdown_with_content_as_list_and_input_as_list_of_str(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=['B'])
        self.assertIn('<option value="B" selected="selected">B</option>', str(drop))

    def test_dropdown_with_content_as_list_and_input_as_list_of_dicttype(self):
        div = HtmlDiv()
        request_dict = {'abc': 'B', 'def': 'A'}
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=request_dict)
        self.assertIn('<option value="B" selected="selected">B</option>', str(drop))

    def test_dropdown_with_content_as_list_and_input_as_list_of_multiple_str_with_option_false(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=['B', 'C'], multiple=False)
        self.assertIn('<option value="B" selected="selected">B</option>', str(drop))
        self.assertIn('<option value="C" selected="selected">C</option>', str(drop))

    def test_dropdown_with_content_as_list_and_input_as_list_of_multiple_str_with_option_true(self):
        div = HtmlDiv()
        drop = div.dropdown('abc', ['A', 'B', 'C', 'D'], var_input=['B', 'C'], multiple=True)
        self.assertIn('<option value="B" selected="selected">B</option>', str(drop))
        self.assertIn('<option value="C" selected="selected">C</option>', str(drop))

    def test_dropdown_with_content_as_dict_and_optgroup(self):
        div = HtmlDiv()
        optgroups = {'AB': ['A', 'B'], 'CD': ['C', 'D']}
        drop = div.dropdown('abc', {'A': 'Code A', 'B': 'Code B', 'C': 'Code C', 'D': 'Code D'}, optgroups=optgroups)
        self.assertIn('<option value="A">Code A</option>', str(drop))
        self.assertIn('<option value="B">Code B</option>', str(drop))
        self.assertIn('<option value="C">Code C</option>', str(drop))
        self.assertIn('<option value="D">Code D</option>', str(drop))
        print(str(drop))


if __name__ == '__main__':
    unittest.main()
