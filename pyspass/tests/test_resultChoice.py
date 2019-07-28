import unittest
from unittest import TestCase

from sqlalchemy import Table, MetaData, Column, Integer, String, select

from pyspass import HtmlForm
from pyspass import ResultChoice


class TestResultChoice(TestCase):

    def setUp(self):
        self.content_as_dict = [{'column_1': 1, 'column_2': 2}, {'column_1': 4, 'column_2': 5}]

    def test_constructor(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=self.content_as_dict, listing_index='column_1', row_selected=None)
        rl.compose()

    def test_setter_listing_index(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=self.content_as_dict, listing_index='column_1', row_selected=None)
        assert rl.listing_index == ('column_1',)

    def test_constructor_empty_content(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=None, listing_index='column_1', row_selected=None)
        rl.compose()

    def test_multiple_index(self):
        html_form = HtmlForm(id_html='form_id')
        rl = html_form.result_choice(content=self.content_as_dict, listing_index=['column_1', 'column_2'],
                                     row_selected={})
        rl.compose()
        print(rl)  # todo elaborate

    def test_indirect_format_id(self):
        # Fixme
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

    def test_with_alchemy(self):
        from sqlalchemy import create_engine
        con = create_engine('sqlite://').connect()
        meta = MetaData(bind=con)
        tab = Table("test_table", meta,
                    Column("column_a", Integer),
                    Column("column_b", String))
        meta.create_all()
        con.execute(tab.insert().values((1, "a")))
        result = con.execute(select([tab.c.column_b])).fetchall()

        html_form = HtmlForm(id_html='form_id')
        rc: ResultChoice = html_form.result_choice(content=result, listing_index='not_there')
        assert "column_b" in str(rc)




if __name__ == '__main__':
    unittest.main()
