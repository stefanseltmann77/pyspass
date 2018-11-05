import unittest
from unittest import TestCase

from pyspass import ResultListing


class TestResultListing(TestCase):

    def setUp(self):
        self.content_as_dict = [{'column_1': 1, 'column_2': 2}]

    def test_resultListing(self):
        rl = ResultListing(self.content_as_dict)

    def test_result_listing_dict_no_mapping(self):
        r1 = ResultListing(self.content_as_dict)
        # no error

    def test_result_listing_dict_exact_list_mapping(self):
        mapping = ['column_1', 'column_2']
        rl = ResultListing(self.content_as_dict, mapping=mapping, show_all=False)
        self.assertEqual(rl._derive_columnnames_for_display(), mapping)

    def test_result_listing_dict_pruned_list_mapping(self):
        mapping = ['column_1']
        rl = ResultListing(self.content_as_dict, mapping=mapping, show_all=False)
        self.assertEqual(rl._derive_columnnames_for_display(), mapping)

    def test_result_listing_dict_pruned_list_mapping_showall(self):
        mapping = ['column_2']
        rl = ResultListing(self.content_as_dict, mapping=mapping, show_all=True)
        self.assertEqual(sorted(rl._derive_columnnames_for_display()), ['column_1', 'column_2'])
        # no error

    def test_result_listing_dict_overlapping_list_mapping(self):
        mapping = ['column_1', 'column_2', 'column3']
        rl = ResultListing(self.content_as_dict, mapping=mapping, show_all=False)
        self.assertEqual(rl._derive_columnnames_for_display(), ['column_1', 'column_2'])

    def test_result_listing_dict_differing_list_mapping(self):
        content = [{'column_1': 1, 'column_2': 2}]
        r1 = ResultListing(content, mapping=['XYZ', 'ABC'])
        # no error

#     def test_result_listing(self):
#         content = [{'column_1': 1, 'column_2': 2}]
#         r1 = ResultListing(content)
#         assert(str(r1).strip() == """<table >
# <tr ><th >column_1<th/><th >column_2<th/>
# <tr/>
# <tr ><td >1<td/><td >2<td/>
# <tr/>
# </table>""")
if __name__ == '__main__':
    unittest.main()