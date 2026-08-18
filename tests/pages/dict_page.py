"""系统管理-字典管理页 Page Object"""
from tests.pages.crud_page import CrudPage


class DictPage(CrudPage):
    path = "/system/dict"
    search_placeholder = "请输入字典名称"
    add_button_text = "新增"
    dialog_title_keyword = "添加"

    def fill_dict_name(self, value):
        self.fill_form_field("字典名称", value)

    def fill_dict_type(self, value):
        self.fill_form_field("字典类型", value)

    def search_dict_name(self, name):
        self.search(name)