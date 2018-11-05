import unittest
from unittest import TestCase

from pyspass import ResultChoice
from pyspass import HtmlForm


class TestResultChoice(TestCase):

    def setUp(self):
        self.content_as_dict = [{'column_1': 1, 'column_2': 2}, {'column_1': 4, 'column_2': 5}]

    def test_constructor(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=self.content_as_dict, listing_index='column_1', row_selected=None)
        rl.compose()

    def test_constructor_empty_content(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=None, listing_index='column_1', row_selected=None)
        rl.compose()

    def test_multiple_index(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=self.content_as_dict, listing_index=['column_1'], row_selected=None)
        with self.assertRaises(TypeError):
            rl.compose()

    def test_indirect_format_id(self):
        html_form = HtmlForm(id_html='form_id')
        html_div = html_form.div()
        rl = html_div.result_choice(content=self.content_as_dict, listing_index='column_1', row_selected=None)
        with self.assertRaises(Exception):
            rl.compose()

    def test_set_codes_constructor_with_dict(self):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=self.content_as_dict, listing_index='column_1',
                                                   row_selected=None)
        rl.set_codes("column_1", {1: "a", 2: "c"})
        rl.compose()

    def test_set_codes_constructor_with_list(self):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=self.content_as_dict, listing_index='column_1',
                                                   row_selected=None)
        rl.set_codes("column_1", [1, 2])
        rl.compose()

    def test_set_codes_constructor_with_dict_and_missing_list_index(self):
        html_form = HtmlForm(id_html='form_id')
        rl: ResultChoice = html_form.result_choice(content=self.content_as_dict, listing_index='not_there',
                                                   row_selected=None)
        rl.set_codes("column_1", {1: "a", 2: "c"})
        rl.compose()


if __name__ == '__main__':
    unittest.main()
