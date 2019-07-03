from abc import ABC, abstractmethod

import pywinauto
from pywinauto import mouse

import operations


class BaseEvent(ABC):

    def __init__(self, app):
        self.app = app

    @abstractmethod
    def prepare(self):
        """事件开始之前的准备"""

    @abstractmethod
    def doing(self):
        """执行事件操作"""

    @abstractmethod
    def check(self):
        """检测事件是否成功执行"""

    def success(self):
        pass

    def failure(self):
        self.doing()


class ElementEvent(BaseEvent):

    def __init__(self, app, find_img, success_flag):
        super().__init__(app)
        self.find_img = find_img
        self.position = None
        self.success_flag = success_flag

    def prepare(self):
        finder = operations.Element(self.find_img)
        self.position = finder.local_one(self.app.window)

    def check(self):
        finder = operations.Element(self.success_flag)
        isexists = finder.local_one(self.app.window)
        return isexists


class ElementClickEvent(ElementEvent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def doing(self):
        mouse.click(self.position)
