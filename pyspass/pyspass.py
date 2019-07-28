from abc import ABCMeta
from abc import abstractmethod
from logging import Logger
from logging import getLogger
from typing import Dict, List, Optional, Union, Tuple


class HtmlObject(metaclass=ABCMeta):
    TAG: str

    ALIGNMENT_MAP = {'r': 'right',
                     'right': 'right',
                     'l': 'left',
                     'left': 'left',
                     'c': 'center',
                     'center': 'center'}

    def __init__(self, id_html: str = None, class_html: str = None):
        self.tag_content: dict = {}
        self.css_styles: dict = {}
        self.id_html: str = id_html
        self.class_html: str = class_html
        self.root_app: PySpassApp = None
        self.parent: HtmlContainer = None
        self.indents: int = 0
        if self.id_html:
            self.tag_content['id'] = self.id_html  # TODO hide in setter
        if self.class_html:
            self.tag_content['class'] = self.class_html  # TODO hide in setter

    def get_form(self) -> Union['HtmlForm', None]:
        """recursive search for parent form

        Raise error if nested form is detected
        """
        if not self.parent:
            parent_form = None
        else:
            if isinstance(self.parent, HtmlForm):
                parent_form = self.parent
            else:
                parent_form = self.parent.get_form()
            if parent_form and (parent_form.get_form() or
                                isinstance(self, HtmlForm)):
                debug_str = parent_form.get_form().id_html if parent_form.get_form() else self.id_html
                raise Exception(f"Nested forms detected! {parent_form.id_html} within {debug_str}.")
        return parent_form


class HtmlContainer(HtmlObject, list, metaclass=ABCMeta):
    def add(self, content: Union[HtmlObject, str, int]) -> HtmlObject:
        self.append(content)
        if isinstance(content, HtmlObject):
            content.parent = self
            return content
        else:
            return self

    def br(self, count: int = 1):
        for i in range(count):
            self.append('<br />\n')
        return self

    def hr(self):
        self.append('<hr />\n')
        return self

    def div(self, content=None, id_html: str = None):
        print()
        div = HtmlDiv(content, id_html)
        self.add(div)
        return div

    def p(self, content=None, id_html: str = None):
        p = HtmlP(content, id_html)
        self.add(p)
        return p

    def span(self, content=None, id_html: str = None):
        span = HtmlSpan(content, id_html)
        self.add(span)
        return span

    def form(self, id_html: str = None):
        form = HtmlForm(id_html)
        self.add(form)
        return form

    def table(self) -> 'HtmlTable':
        table = HtmlTable()
        self.add(table)
        return table

    def h1(self, content=None):
        h1 = HtmlH1(content)
        self.add(h1)
        return h1

    def h2(self, content=None):
        h2 = HtmlH2(content)
        self.add(h2)
        return h2

    def h3(self, content=None):
        h3 = HtmlH3(content)
        self.add(h3)
        return h3

    def link(self, content=None):
        link = HtmlLink(**{key: value for key, value in locals().items() if key not in 'self'})
        self.add(link)
        return link

    def label(self, content: str = None, for_id: str = None) -> 'HtmlLabel':
        label = HtmlLabel(content=content, for_id=for_id)
        self.add(label)
        return label

    def hidden(self, name, value=None, id_html: str = None) -> 'HtmlHidden':
        hidden = HtmlHidden(name=name, value=value, id_html=id_html)
        self.add(hidden)
        return hidden

    def submit(self, name: str, value=None, id_html: str = None, class_html=None) -> 'HtmlSubmit':
        sub = HtmlSubmit(name=name, value=value, id_html=id_html, class_html=class_html)
        self.add(sub)
        return sub

    def button(self, name: str, value=None, id_html: str = None, class_html=None):
        sub = HtmlButton(name=name, value=value, id_html=id_html, class_html=class_html)
        self.add(sub)
        return sub

    def checkbox(self, name, value=1, label=None, var_input: Union[int, str] = None, autosubmit: bool = False,
                 id_html: str = None, class_html: str = None, label_trailing: bool = True):
        chkbx = HtmlCheckbox(name=name, value=value, var_input=var_input, autosubmit=autosubmit,
                             id_html=id_html, class_html=class_html)
        label = HtmlLabel(content=label, for_id=id_html)
        if not label_trailing:
            self.add(label)
        self.add(chkbx)
        if label_trailing:
            self.add(label)
        return chkbx

    def script(self, content: str = None, src: str = None, script_type: str = None):
        script = HtmlScript(content=content, src=src, script_type=script_type)
        self.add(script)
        return script

    def dropdown(self, name, codes_source: Union[List, Dict], var_input=None, autosubmit: bool = False,
                 missing_allowed: bool = True, multiple: bool = False, size: int = 1, optgroups: dict = None):
        return self.add(HtmlSelect(**{key: value for key, value in locals().items() if key not in 'self'}))

    def textinput(self, name, var_input=None, size: int = 20, alignment: str = None):
        return self.add(HtmlTextInput(**{key: value for key, value in locals().items() if key not in 'self'}))

    def password(self, name, var_input=None, size: int = 20):
        return self.add(HtmlPassword(**{key: value for key, value in locals().items() if key not in 'self'}))

    def textarea(self, name, var_input=None, rows: int = 4, cols: int = 50):
        return self.add(HtmlTextArea(**{key: value for key, value in locals().items() if key not in 'self'}))

    def result_listing(self, content: list, mapping=None, show_all: bool = False,
                       alignments=None) -> Union['ResultListing', HtmlObject]:
        return self.add(ResultListing(**{key: value for key, value in locals().items() if key not in 'self'}))

    def result_choice(self, content: list, listing_index: Union[str, tuple, list], row_selected=None,
                      mapping: Dict[str, str] = None, show_all: bool = False, alignments=None,
                      rowcount_max: int = 200) -> Union['ResultChoice', HtmlObject]:
        """Factory function for creation of ResultChoice"""
        return self.add(ResultChoice(**{key: value for key, value in locals().items() if key not in 'self'}))

    def result_editor(self, content: list, listing_index, row_selected=None, mapping=None, show_all: bool = False,
                      rowcount_max: int = 200, columns_protected: list = None, alignments=None):
        return self.add(ResultEditor(**{key: value for key, value in locals().items() if key not in 'self'}))

    def __str__(self):
        if self.css_styles:
            css_styles_str = ';'.join([key + ':' + value for key, value in self.css_styles.items()])
            self.tag_content['style'] = css_styles_str
        tag_content_str = ' '.join([f'{key}="{value}"' for key, value in self.tag_content.items()])
        return f"<{self.TAG}{' ' + tag_content_str if tag_content_str else ''}>" \
            f"\n{''.join([str(child) for child in self])}\n</{self.TAG}>\n"


class HtmlTable(HtmlContainer):
    TAG: str = 'table'

    column_styles = None

    def __init__(self):
        super().__init__()
        self._column_alignments = None

    def __str__(self):
        tag_content_str = ' '.join([f'{key}="{value}"' for key, value in self.tag_content.items()])
        return f'<{self.TAG} {tag_content_str}>{"".join([str(item) for item in self])}\n</{self.TAG}>\n'

    def tr(self):
        row = HtmlRow()
        self.add(row)
        return row

    def set_column_alignments(self, alignments: str):
        for row in self:
            for i, alignment in enumerate(alignments):
                if i < len(row):
                    row[i].css_styles["text-align"] = self.ALIGNMENT_MAP[alignment]
                else:
                    break


class ResultListing(HtmlContainer):
    """Display object that renders as tabular dataset (nested list) as a html table."""

    table: HtmlTable

    def __init__(self, content: list, mapping=None, show_all: bool = False, rowcount_max: int = 200,
                 alignments=None):
        super().__init__()
        self.show_all = show_all
        self.content: list = content
        self.mapping = mapping
        self.rowcount_max: int = rowcount_max
        self.columns_display: list = []

        tab = super().table()
        self.table = tab
        headrow = tab.tr()
        if content:
            self.columns_display = self._derive_columnnames_for_display()
            if isinstance(content, dict):
                headrow.th("KEY")
                headrow.th("VALUE")
                for key, value in content.items():
                    tablerow = tab.tr()
                    tablerow.td(str(key))
                    tablerow.td(str(value))
                    # FIXME implement column names
            else:
                for key in self.columns_display:
                    if isinstance(mapping, dict):
                        headrow.th(self.mapping.get(key, key))
                    else:
                        headrow.th(key)
                for rownum, row in enumerate(content):
                    if rownum < rowcount_max:  # limitation of displayed rows
                        tablerow = tab.tr()
                        for key in self.columns_display:
                            try:
                                tablerow.td(str(row.get(key, '')))
                            except AttributeError:
                                try:
                                    tablerow.td(str(row[key]))
                                except KeyError:
                                    tablerow.td("")
                    else:
                        break
            if alignments:
                tab.set_column_alignments(alignments)
        else:
            pass  # no content, no rows

    def _derive_columnnames_for_display(self) -> list:
        if isinstance(self.content, dict):
            content_keys_data = self.content.keys()
        else:
            try:
                content_keys_data = self.content[0].keys()

            except:
                raise NotImplementedError()
        if self.mapping:
            if not self.show_all:
                content_keys = [key for key in self.mapping if key in content_keys_data]
            else:
                content_keys = list(self.mapping)
                for key in content_keys_data:
                    if key not in self.mapping:
                        content_keys.append(key)
        else:
            content_keys = content_keys_data
        return list(content_keys)

    def __str__(self):
        # for row in self.table:
        #     for cell_nr, cell in enumerate(row):
        #         if cell_nr == 0:
        #             cell.css_styles['text-align'] = 'right'
        #     print (1)
        return ''.join([str(chunk) for chunk in self])


class ResultChoice(ResultListing):
    """Display object similar to ResultListing, but allows selection of rows"""

    PREFIX: str = '_rct_selected_'

    _index: Tuple = None

    def __init__(self, content: list, listing_index: str, row_selected: Union[str, Dict],
                 mapping: Dict[str, str] = None, show_all: bool = False, rowcount_max: int = 200, alignments=None):
        """

        :param content:
        :param listing_index:
        :param row_selected:
        :param mapping:
        :param show_all:
        :param rowcount_max:
        :param alignments:
        """
        super().__init__(content, mapping, show_all, rowcount_max, alignments)
        self.row_selected = row_selected or {}
        self.listing_index = listing_index
        self.columns_config: dict = {}
        self.columns_with_mappings: list = []

    @property
    def listing_index(self):
        return self._index

    @listing_index.setter
    def listing_index(self, value):
        self._index = value if not isinstance(value, str) else (value,)

    def compose(self):
        parent_form = self.get_form()
        if not isinstance(parent_form, HtmlForm):
            raise Exception('ResultChoices have to be direct or indirect children of a form with an unique ID!')
        id_html_parentform: str = parent_form.id_html
        if not id_html_parentform:
            raise Exception("Only works if parent form has unique ID")
        # FIXME: doesn't have to be parents
        content = self.content or []
        if len(content) > 0:  # FIXME test an rewrite without >0
            for index_col in self._index:
                if index_col not in content[0]:  # todo rewrite with sets, rewrite with any or all
                    raise Exception(
                        f"Listing_index '{index_col}' not in list content ({list(content[0].keys())})!")
        for i, row_dat in enumerate(content):  # TODO or list somewhere else
            if i < self.rowcount_max:
                row: HtmlRow = self.table[i + 1]  # +1 for header
                json = ",".join(f"'{index_col}':'{row_dat[index_col]}'" for index_col in self._index)
                row.tag_content["onclick"] = f"entryChoiceSetSelection('{id_html_parentform}', {{{json}}});"
                if isinstance(self.row_selected, str) and str(row_dat[self._index[0]]) == str(self.row_selected):
                    # simple input for one column index
                    # todo put string in setter
                    # FIXME put selected row in dictionary
                    self._build_selected_row(row)
                elif not isinstance(self.row_selected, (str, int)) and \
                        all(str(row_dat[index_col]) == str(self.row_selected.get(index_col))
                            for index_col in self._index):
                    self._build_selected_row(row)
                if self.columns_with_mappings:
                    for column_name in self.columns_with_mappings:
                        column_index = self.columns_display.index(column_name)
                        row[column_index][0] = self.columns_config[column_name]['codes'].get(row[column_index][0],
                                                                                             row[column_index][0])
            else:
                break
        for index_col in self._index:
            self.hidden(name=self.PREFIX + index_col, value=self.row_selected, id_html=self.PREFIX + index_col)

    def _build_selected_row(self, row):
        row.css_styles['color'] = 'white'
        row.css_styles['background'] = 'grey'

    def set_codes(self, column_name: str, codes: Union[list, dict], multichoice: bool = False, display_size: int = 1):
        """Assign a code mapping to a given column name.

        Codes/values within the column will be replaced by values from the mapping.
        All keys are converted to strings in order to simplify retrieval.

        :param column_name:
        :param codes:
        :param multichoice:
        :param display_size:
        :return:
        """
        try:
            self.columns_config.setdefault(column_name, {})['codes'] = {str(key): value for key, value in codes.items()}
            self.columns_with_mappings.append(column_name)
        except AttributeError:
            self.columns_config.setdefault(column_name, {})['codes'] = codes
        self.columns_config[column_name]['multi_choice'] = multichoice
        self.columns_config[column_name]['display_size'] = display_size
        return self


class ResultEditor(ResultChoice):
    def __init__(self, content: list, listing_index, row_selected, mapping=None, show_all: bool = False,
                 rowcount_max: int = 200, columns_protected: list = None, alignments=None):
        super().__init__(content=content, listing_index=listing_index, row_selected=row_selected,
                         mapping=mapping, show_all=show_all, rowcount_max=rowcount_max, alignments=alignments)
        self.columns_protected: list = columns_protected or []
        self.columns_protected.append(listing_index)

    def _build_selected_row(self, row):
        row.css_styles['color'] = 'white'
        row.css_styles['background'] = 'blue'
        row.tag_content.pop('onclick', None)
        for i, cell in enumerate(row):
            column_current = self.columns_display[i]
            if column_current not in self.columns_protected:
                cell_input = HtmlCell()
                if 'codes' in self.columns_config.get(column_current, {}):
                    cell_input.dropdown(name=column_current,
                                        var_input=cell[0] if cell else None,
                                        codes_source=self.columns_config[column_current]['codes'],
                                        missing_allowed=False)
                    if self.columns_config.get(column_current, {}).get('multi_choice'):
                        raise NotImplementedError
                    if self.columns_config.get(column_current, {}).get('display_size') != 1:
                        raise NotImplementedError
                else:
                    cell_input.textinput(column_current, var_input=cell[0] if cell else None)
                row[i] = cell_input
        cell_submit = row.td()
        button = cell_submit.submit('submit_save_resulteditor', 'save')  # focus on selected line
        button.tag_content['autofocus'] = 'autofocus'


class HtmlPage:
    body = None
    head = None
    root_app = None

    def __init__(self, root_app=None):
        self.root_app = root_app
        self.head = HtmlHead()
        self.body = HtmlBody()

    def render(self):
        return "</?xml version=\"1.0\" encoding=\"utf-8\" ?>\n" \
               "<!DOCTYPE html>\n" \
               "<html xmlns=\"http://www.w3.org/1999/xhtml\"" \
            f"xml:lang=\"de\" lang=\"de\">\n{self.head}\n{self.body}\n</html>\n"


class HtmlBody(HtmlContainer):
    TAG: str = 'body'


class HtmlHead(HtmlContainer):
    TAG: str = 'head'

    def resourcelink(self, rel: str, linktype: str, href: str):
        link = HtmlResource(rel=rel, linktype=linktype, href=href)
        self.add(link)
        return link


class HtmlOptgroup(HtmlContainer):
    TAG: str = 'optgroup'


class HtmlOption(HtmlContainer):
    TAG: str = 'option'


class HtmlInput(HtmlObject):
    TAG: str = 'input'

    def __str__(self):
        if self.css_styles:
            self.tag_content['style'] = ";".join([f"{key}: {value}" for key, value in self.css_styles.items()])
        tag_content_str = ' '.join([f'{key}="{value}"' for key, value in self.tag_content.items()])
        return f'<{self.TAG} {tag_content_str}/>'


class HtmlH1(HtmlContainer):
    TAG: str = 'h1'

    def __init__(self, content=None):
        super().__init__()
        if content:
            self.add(content)


class HtmlH2(HtmlH1):
    TAG: str = 'h2'


class HtmlH3(HtmlH1):
    TAG: str = 'h3'


class HtmlP(HtmlContainer):
    TAG: str = 'p'

    def __init__(self, content=None, id_html: str = None):
        super().__init__(id_html=id_html)
        if content:
            self.append(content)


class HtmlLabel(HtmlContainer):
    TAG: str = 'label'

    def __init__(self, content: str = None, for_id: str = None, id_html: str = None, class_html: str = None):
        super().__init__(id_html=id_html, class_html=class_html)
        if content:
            self.append(content)
        if for_id:
            self.tag_content['for'] = for_id


class HtmlLink(HtmlContainer):
    TAG: str = 'a'

    def __init__(self, content: str = None, href: str = None, target: str = "_blank",
                 id_html: str = None, class_html: str = None):
        """
        If content is left empty, href will be taken instead.
        """
        super().__init__(id_html=id_html, class_html=class_html)
        if content:
            self.append(content)
        self.tag_content['href'] = href or content
        if target:
            self.tag_content['target'] = target


class HtmlResource(HtmlContainer):
    TAG: str = 'link'

    def __init__(self, rel: str, linktype: str, href: str):
        super().__init__()
        self.tag_content['href'] = href
        self.tag_content['rel'] = rel
        self.tag_content['type'] = linktype


class HtmlSpan(HtmlContainer):
    TAG: str = 'span'

    def __init__(self, content=None, id_html: str = None):
        super().__init__()
        if content:
            self.append(content)
        if id_html:
            self.id_html = id_html
            self.tag_content['id'] = id_html  # Fixme hide in setter


class HtmlDiv(HtmlContainer):
    TAG: str = 'div'

    def __init__(self, content=None, id_html: str = None):
        super().__init__()
        if content:
            self.append(content)
        if id_html:
            self.id_html = id_html
            self.tag_content['id'] = id_html  # Fixme hide in setter


class HtmlForm(HtmlDiv):
    TAG: str = 'form'

    def __init__(self, id_html):
        super().__init__(id_html=id_html)
        self.tag_content['method'] = 'post'
        self.tag_content['action'] = ''


class HtmlScript(HtmlContainer):
    TAG: str = 'script'

    def __init__(self, content: str = None, src: str = None, script_type: str = None):
        super().__init__()
        self.script_type = script_type
        if content:
            self.add(content)
        if src:
            self.tag_content['src'] = src


class HtmlHidden(HtmlInput):
    def __init__(self, name: str, value: str = None, id_html: str = None):
        super().__init__()
        self.tag_content['type'] = 'hidden'
        self.tag_content['name'] = name
        if value:
            self.tag_content['value'] = value
        if id_html:
            self.tag_content['id'] = id_html


class HtmlSubmit(HtmlInput):
    def __init__(self, name, value=None, id_html: str = None, class_html=None):  # FIXME use parameter
        super().__init__()
        self.tag_content = {'type': 'submit',
                            'name': name}
        if value:
            self.tag_content['value'] = value
        if id_html:
            self.tag_content['id'] = id_html
        if class_html:
            self.tag_content['class'] = class_html


class HtmlButton(HtmlInput):
    def __init__(self, name: str, value=None, id_html: str = None, class_html=None):  # FIXME use parameter
        super().__init__()
        self.tag_content = {'type': 'button',
                            'name': name}
        if value:
            self.tag_content['value'] = value
        if id_html:
            self.tag_content['id'] = id_html
        if class_html:
            self.tag_content['class'] = class_html


class HtmlTextInput(HtmlInput):
    def __init__(self, name: str, var_input=None, size: int = 20, alignment: str = None):
        super().__init__()
        self.tag_content = {'type': 'text',
                            'name': name,
                            'size': size,
                            'id': name}
        if var_input:
            self.tag_content['value'] = var_input
        if alignment:
            if alignment in self.ALIGNMENT_MAP:
                self.css_styles['text-align'] = self.ALIGNMENT_MAP[alignment]
            else:
                pass  # todo add debugging error


class HtmlPassword(HtmlInput):
    def __init__(self, name: str, var_input=None, size=20):
        super().__init__()
        self.tag_content = {'type': 'password',
                            'name': name,
                            'size': size,
                            'id': name}
        if var_input:
            self.tag_content['value'] = var_input


class HtmlTextArea(HtmlInput):
    TAG: str = "textarea"

    def __init__(self, name: str, var_input=None, rows: int = 4, cols: int = 50):
        super().__init__()
        self.tag_content = {'name': name,
                            'cols': cols,
                            'rows': rows,
                            'id': name}
        print(self.parent)
        self.var_input: str = var_input

    def __str__(self):
        tag_content_str = ' '.join([f'{key}="{value}"' for key, value in self.tag_content.items()])
        return f'<{self.TAG} {tag_content_str}>{self.var_input}</{self.TAG}>'


class HtmlRadio(HtmlInput):
    def __init__(self, name, var_input=None):
        super().__init__()
        self.tag_content = {'type': 'radio',
                            'name': name}
        if var_input:
            self.tag_content['value'] = var_input


class HtmlCheckbox(HtmlInput):
    def __init__(self, name, value, var_input: Union[int, str] = None, autosubmit: bool = False,
                 id_html: str = None, class_html: str = None):
        super().__init__(id_html=id_html, class_html=class_html)
        self.tag_content = {'type': 'checkbox',
                            'name': name,
                            'value': value}
        if autosubmit:
            self.tag_content["onclick"] = "submit()"
        if str(var_input) == str(value):
            self.tag_content["checked"] = "checked"


class HtmlSelect(HtmlInput):
    TAG: str = "select"
    _missing_code_id = -1
    _missing_code_label = 'No Entry'

    codes_source: dict = None

    def __init__(self, name, codes_source: Union[Dict, List], var_input=None, autosubmit: bool = False,
                 missing_allowed: bool = False, multiple: bool = False, size: int = 1, optgroups: dict = None):
        """Dropdown element.

        :param codes_source:
        :param var_input:
        :param autosubmit:
        :param missing_allowed:
        :param multiple:
        :param size:
        :param optgroups:
        """
        super().__init__()
        self.tag_content = {'name': name}
        if isinstance(codes_source, list):
            self.codes_source = dict(zip(codes_source, codes_source))
        else:
            self.codes_source = codes_source
        if isinstance(var_input, list):
            self.var_input = list(map(str, var_input))
        else:
            try:
                if multiple:
                    self.var_input = var_input.get_list(name + "[]")
                else:
                    self.var_input = [str(var_input.get(name))]
            except AttributeError:
                self.var_input = [str(var_input)]
        self.autosubmit = autosubmit
        self.missing_allowed = missing_allowed
        self.multiple = multiple
        self.size = size
        self.optgroups = optgroups

    def __str__(self):
        if self.autosubmit:
            self.tag_content['onchange'] = 'submit()'
        if self.multiple:
            self.tag_content['multiple'] = 'multiple'
            self.tag_content['name'] += '[]'
            self.tag_content['size'] = self.size
        tag_content_str = ' '.join([f'{key}="{value}"' for key, value in self.tag_content.items()])

        codes_source_actual = self.codes_source if not self.missing_allowed else \
            {**{self._missing_code_id: self._missing_code_label}, **self.codes_source}

        content = []
        if self.optgroups:
            for key, value_list in self.optgroups.items():
                optgroup = HtmlOptgroup()
                optgroup.tag_content['label'] = key
                content.append(optgroup)
                for value in value_list:
                    label = codes_source_actual[value]
                    option = HtmlOption()
                    option.tag_content['value'] = value
                    if str(value) in self.var_input:
                        option.tag_content['selected'] = 'selected'
                    option.add(label)
                    optgroup.append(option)
        else:
            for code, label in codes_source_actual.items():
                option = HtmlOption()
                option.tag_content['value'] = code
                if str(code) in self.var_input:
                    option.tag_content['selected'] = 'selected'
                option.add(label)
                content.append(option)
        option_str = '\n'.join([str(obt).replace('\n', '') for obt in content])
        return f'<{self.TAG} {tag_content_str}>{option_str}\n</{self.TAG}>\n'


class HtmlCell(HtmlContainer):
    TAG: str = 'td'

    def __init__(self, content=None):
        super().__init__()
        if content:
            self.append(content)


class HtmlHeadCell(HtmlCell):
    TAG: str = 'th'


class HtmlRow(HtmlContainer):
    """Object for standard HTML row"""
    TAG: str = 'tr'

    def td(self, content=None) -> Union[HtmlObject, HtmlCell]:
        return self.add(HtmlCell(content))

    def th(self, content: Union[str, List[str], Tuple[str]] = None) -> \
            Union[Union[HtmlCell, HtmlObject], Union[List[HtmlCell], List[HtmlObject]]]:
        """Create and add a new header cell object

        :param content: May be the string contained in the cell or an object or a list of both
        :return: Returns the created cell or list of cells
        """
        if isinstance(content, list) or isinstance(content, tuple):
            return [self.add(HtmlHeadCell(content_piece)) for content_piece in content]
        else:
            return self.add(HtmlHeadCell(content))


class PySpassStorage:
    storage_object = None

    def get(self, field: str, default=None, noentry=None) -> str:
        value = self.storage_object.get(field, default)
        return value if value != noentry else ""


class PySpassRequest(PySpassStorage):

    def __init__(self, request_object, framework: str):
        self.noentry_default = "-1"
        if framework.lower() == "flask":
            self.storage_object = request_object
        else:
            raise NotImplementedError

    def get(self, request_field: str, default=None, noentry=None) -> str:
        value = self.storage_object.form.get(request_field, default)
        return value if value != noentry else ""

    def get_tuple(self, *args, default=None, noentry=None):
        return (self.get(arg, default=default, noentry=noentry) for arg in args)

    def get_int(self, request_field: str, default: int = None, noentry: int = None) -> Optional[int]:
        value = self.get(request_field, default=default, noentry=noentry)
        try:
            return int(value)
        except ValueError:
            return None

    def get_list(self, request_field: str) -> list:
        value_list = self.storage_object.form.getlist(request_field.strip("[]") + "[]")  # ensure closing brackets
        return value_list if isinstance(value_list, list) else [value_list]

    def get_float(self, request_field: str, default: float = None, noentry: float = None) -> Optional[float]:
        value = self.get(request_field, default=default, noentry=noentry)
        try:
            return float(value)
        except ValueError:
            return None


class PySpassSession(PySpassStorage):
    def __init__(self, session_object, framework: str):
        if framework.lower() == "flask":
            self.storage_object = session_object
        else:
            raise NotImplementedError

    def __setitem__(self, key, value):
        self.storage_object[key] = value


class PySpassApp(metaclass=ABCMeta):
    app_name: str
    logger: Logger = getLogger(__name__)
    page: HtmlPage
    session: PySpassSession
    request: PySpassRequest

    def __init__(self, app_name: str, request: PySpassRequest, session: PySpassSession):
        """

        :param app_name: distinct name for the action, also as seed for certain elements in form
        """
        self.app_name = app_name
        self.request = request
        self.session = session
        self.setup_page()

    def setup_page(self):
        self.logger.info("Setup page root")
        self.page = HtmlPage()
        self.page.head.script(src='static/spass_forms.js')

    def display_login_form(self):
        self.logger.info("Display login form")
        div = self.page.body.div(id_html='centerBox')
        loginform = div.form("loginform")
        loginform.add("Username")
        username_entry = loginform.textinput(self.app_name + "_username_entry")
        username_entry.tag_content['placeholder'] = "username"
        loginform.add("Password")
        loginform.br()
        password_entry = loginform.password(self.app_name + "_password_entry")
        password_entry.tag_content['placeholder'] = "password"
        loginform.submit("submit_login", "enter")

    def resolve_login(self):
        self.logger.info("Resolving login")
        if self.session.get("success_login"):
            self.logger.debug("Login already established")
            return True
        else:
            self.logger.debug("Login will be resolved")
            login_success = False
            if self.request.get("submit_login"):
                login_success: bool = self.affirm_credentials(self.request.get(self.app_name + "_username_entry"),
                                                              self.request.get(self.app_name + "_password_entry"))
            if login_success:
                self.session["success_login"] = True
                self.logger.debug("Login successful")
                return True
            else:
                self.display_login_form()
                return False

    @abstractmethod
    def affirm_credentials(self, username: str, password: str):
        self.logger.warning("Affirming credentials has to be implemented yet")
        return True
