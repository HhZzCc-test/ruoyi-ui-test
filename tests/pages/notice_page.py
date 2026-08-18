"""系统管理-通知公告页 Page Object"""
from tests.pages.crud_page import CrudPage


class NoticePage(CrudPage):
    path = "/system/notice"
    search_placeholder = "请输入公告标题"
    add_button_text = "新增"
    dialog_title_keyword = "添加"

    def fill_notice_title(self, value):
        self.fill_form_field("公告标题", value)

    def fill_notice_content(self, value):
        self.fill_form_field("公告内容", value)

    def search_notice_title(self, title):
        self.search(title)