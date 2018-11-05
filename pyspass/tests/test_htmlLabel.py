import unittest
from unittest import TestCase

from pyspass import HtmlDiv


class TestHtmlLabel(TestCase):

    def setUp(self):
        pass

    def test_rendering_with_forid(self):
        div = HtmlDiv()
        div.label(content="test", for_id="input_id")
        self.assertIn('<label for="input_id">test</label>', str(div).replace("\n", ""))


if __name__ == '__main__':
    unittest.main()
