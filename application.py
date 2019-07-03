from typing import Tuple, Generator
from events import BaseEvent


class AppExecutor(object):
    """app执行器，封装用于执行的app代码"""

    def __init__(self, app_name):
        self.app_name = app_name
        self.events = ()
        self.running_app: Generator = None

    def isrunning(self):
        """装饰器： 判断app是否在运行"""
        pass

    def execute(self, events: Tuple[BaseEvent]):
        self.events = events
        def app_generator(events: Tuple[BaseEvent]) -> Generator:
            for event in self.events:
                yield
                try:
                    event.start()
                except:
                    event.failure()
                else:
                    event.success()
        self.running_app = app_generator(events).send(None)

    @isrunning
    def next(self):
        """执行app的下一个事件"""
        next(self.running_app)

    @isrunning
    def stop(self):
        """停止app执行 """
        pass

    def pause(self):
        """暂停app执行"""
        pass
