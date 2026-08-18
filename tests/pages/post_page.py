"""系统管理-岗位管理页 Page Object"""
from tests.pages.crud_page import CrudPage


class PostPage(CrudPage):
    path = "/system/post"
    search_placeholder = "请输入岗位编码"
    add_button_text = "新增"
    dialog_title_keyword = "添加"

    def fill_post_code(self, value):
        self.fill_form_field("岗位编码", value)

    def fill_post_name(self, value):
        self.fill_form_field("岗位名称", value)

    def fill_post_sort(self, value):
        self.fill_form_field("岗位排序", value)

    def search_post_code(self, code):
        self.search(code)