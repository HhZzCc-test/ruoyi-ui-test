"""系统管理-角色管理页 Page Object"""
from tests.pages.crud_page import CrudPage


class RolePage(CrudPage):
    path = "/system/role"
    search_placeholder = "请输入角色名称"
    add_button_text = "新增"
    dialog_title_keyword = "添加"

    def fill_role_name(self, value):
        self.fill_form_field("角色名称", value)

    def fill_role_key(self, value):
        self.fill_form_field("权限字符", value)

    def fill_role_sort(self, value):
        self.fill_form_field("显示顺序", value)

    def fill_status(self, value):
        self.fill_form_field("状态", value)

    def search_role_name(self, name):
        self.search(name)