import os
import time
from typing import Dict, List

class aa():
    instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

if __name__ == "__main__":
    print(aa(), aa())
    # wrapper = window.active()
    # a = wrapper.capture_as_image()
    # a.show()
    # print(time.time()-t1)
    # async def aa(a):
    #     pyscreeze.screenshot()
    # loop = asyncio.get_event_loop()
    # t1 = time.time()
    # loop.run_until_complete(asyncio.wait([aa(1), aa(2), aa(3), aa(4)]))
    # print(time.time()-t1)
