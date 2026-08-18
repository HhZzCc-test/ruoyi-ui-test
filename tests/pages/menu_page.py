"""系统管理-菜单管理页 Page Object"""
from tests.pages.crud_page import CrudPage


class MenuPage(CrudPage):
    path = "/system/menu"
    search_placeholder = "请输入菜单名称"
    add_button_text = "新增"
    dialog_title_keyword = "添加"

    def fill_menu_name(self, value):
        self.fill_form_field("菜单名称", value)

    def fill_order_num(self, value):
        self.fill_form_field("显示排序", value)

    def search_menu_name(self, name):
        self.search(name)