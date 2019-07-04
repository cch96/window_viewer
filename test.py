import os
import time
from multiprocessing import Process, Pipe
from threading import Thread
from typing import Dict, List

def aa(conn1):
    conn1.send('123')

async def bb():
    pass


if __name__ == "__main__":
    print(type(bb()))
    # p2 = Process(target=bb, args=(conn2, ))
    # t1 = time.time()
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # print(time.time()-t1)
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
