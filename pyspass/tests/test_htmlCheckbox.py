import unittest
from unittest import TestCase

from pyspass import HtmlCheckbox, HtmlDiv


class TestHtmlCheckbox(TestCase):

    def setUp(self):
        pass

    def test_checkbox_without_minimum_params(self):
        div = HtmlDiv()
        div.checkbox(name="check_test", value=1, label='label')
        self.assertIn('<input type="checkbox" name="check_test" value="1"/>', str(div))


if __name__ == '__main__':
    unittest.main()
