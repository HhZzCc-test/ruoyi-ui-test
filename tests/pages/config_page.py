"""系统管理-参数设置页 Page Object"""
from tests.pages.crud_page import CrudPage


class ConfigPage(CrudPage):
    path = "/system/config"
    search_placeholder = "请输入参数名称"
    add_button_text = "新增"
    dialog_title_keyword = "添加"

    def fill_config_name(self, value):
        self.fill_form_field("参数名称", value)

    def fill_config_key(self, value):
        self.fill_form_field("参数键名", value)

    def fill_config_value(self, value):
        self.fill_form_field("参数键值", value)

    def search_config_name(self, name):
        self.search(name)