from abc import ABC, abstractmethod

import pywinauto

import operations

class BaseEvent(ABC):
    @abstractmethod
    def prepare(self):
        """事件开始之前的准备"""

    @abstractmethod
    def doing(self):
        """执行事件操作"""

    @abstractmethod
    def check(self):
        """检测事件是否成功执行"""

    def start(self):
        self.prepare()
        self.execute()
        self.check()


class ElementClickEvent(BaseEvent):

    def __init__(self, find_img):
        self.find_img = find_img
        self.position = None

    def prepare(self):
        find = operations.Element(self.find_img)
        self.position = find.local_one(self.find_img)

    def doing(self):



