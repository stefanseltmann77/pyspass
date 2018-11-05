import unittest
from unittest import TestCase

from pyspass import ResultEditor
from pyspass import HtmlForm


class TestResultEditor(TestCase):
    def setUp(self):
        self.content_as_dict = [{'column_id': 1,
                                 'column_2': 2,
                                 'column_3': 'A'},
                                {'column_id': 2,
                                 'column_2': 4,
                                 'column_3': 'B'},
                                {'column_id': 3,
                                 'column_2': 6,
                                 'column_3': 'C'}]

    def test_resultEditor(self):
        form = HtmlForm(id_html='form_id')
        re = ResultEditor(content=self.content_as_dict, listing_index='column_id', row_selected='2')
        form.add(re)
        re.compose()

    def test_resultEditor_show_all(self):
        form = HtmlForm(id_html='form_id')
        re = ResultEditor(content=self.content_as_dict, listing_index='column_id', row_selected='2', show_all=True)
        form.add(re)
        re.compose()


if __name__ == '__main__':
    unittest.main()
