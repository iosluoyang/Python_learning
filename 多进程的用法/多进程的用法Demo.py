# import multiprocessing
#
# def process(num):
#     print 'process:',num
#
# if __name__ =='__main__':
#     for i in range(5):
#         p = multiprocessing.Process(target=process,args=(i,))
#         p.start()




# import multiprocessing
# import time
#
# def process(num):
#     time.sleep(num)
#     print 'process:',num
#
# if __name__ =='__main__':
#     for i in range(5):
#         p = multiprocessing.Process(target=process,args=(i,))
#         p.start()
#
#     print ('CPU number:'+ str(multiprocessing.cpu_count()))
#
#     for p in multiprocessing.active_children():
#         print ('Child process name :' + p.name + 'id:' + str(p.pid))
#
#
#     print 'Process Ended'




# from multiprocessing import  Process
# import  time
#
# class MyProcess(Process):
#     def __init__(self,loop):
#         Process.__init__(self)
#         self.loop = loop
#
#     def run(self):
#         for count in range(self.loop):
#             time.sleep(1)
#             print ('Pid:' + str(self.pid) + 'LoopCount:' + str(count))
#
# if __name__ == '__main__':
#     for i in range(2,5):
#         p = MyProcess(i)
#         p.start()


# from multiprocessing import  Process,Lock
# import  time
#
# class MyProcess(Process):
#     def __init__(self,loop,lock):
#         Process.__init__(self)
#         self.loop = loop
#         self.lock = lock
#
#     def run(self):
#         for count in range(self.loop):
#             time.sleep(0.1)
#             self.lock.acquire()
#             print ('Pid:' + str(self.pid) + 'LoopCount:' + str(count))
#             self.lock.release()
#
# if __name__ == '__main__':
#     lock = Lock()
#     for i in range(10,15):
#         p = MyProcess(i,lock)
#         # p.daemon = True
#         p.start()
#         # p.join()
#
#     print 'Main process Ended'





# from multiprocessing import  Process,Semaphore,Lock,Queue
# import time
#
# buffer = Queue(10)
# empty = Semaphore(2)
# full = Semaphore(0)
# lock = Lock()
#
# class Consumer(Process):
#     def run(self):
#         global  buffer,empty,full,lock
#         while True:
#             full.acquire()
#             lock.acquire()
#             buffer.get()
#             print 'Consumer pop an element'
#             time.sleep(1)
#             lock.release()
#             empty.release()
#
# class Producer(Process):
#     def run(self):
#         global buffer,empty,full,lock
#         while True:
#             empty.acquire()
#             lock.acquire()
#             buffer.put(1)
#             print  'Producer append an element'
#             time.sleep(1)
#             lock.release()
#             full.release()
#
#
# if __name__ == '__main__':
#     p = Producer()
#     c = Consumer()
#     p.daemon = c.daemon = True
#     p.start()
#     c.start()
#     p.join()
#     c.join()
#     print 'Ended'




# from multiprocessing import Process, Semaphore, Lock, Queue
# import time
# from random import random
#
# buffer = Queue(10)
# empty = Semaphore(2)
# full = Semaphore(0)
# lock = Lock()
#
# class Consumer(Process):
#
#     def run(self):
#         global buffer, empty, full, lock
#         while True:
#             full.acquire()
#             lock.acquire()
#             print 'Consumer get', buffer.get()
#             time.sleep(1)
#             lock.release()
#             empty.release()
#
#
# class Producer(Process):
#     def run(self):
#         global buffer, empty, full, lock
#         while True:
#             empty.acquire()
#             lock.acquire()
#             num = random()
#             print 'Producer put ', num
#             buffer.put(num)
#             time.sleep(1)
#             lock.release()
#             full.release()
#
#
# if __name__ == '__main__':
#     p = Producer()
#     c = Consumer()
#     p.daemon = c.daemon = True
#     p.start()
#     c.start()
#     p.join()
#     c.join()
#     print 'Ended!'




# from multiprocessing import Process, Pipe
#
#
# class Consumer(Process):
#     def __init__(self, pipe):
#         Process.__init__(self)
#         self.pipe = pipe
#
#     def run(self):
#         self.pipe.send('Consumer Words')
#         print 'Consumer Received:', self.pipe.recv()
#
#
# class Producer(Process):
#     def __init__(self, pipe):
#         Process.__init__(self)
#         self.pipe = pipe
#
#     def run(self):
#         self.pipe.send('Producer Words')
#         print 'Producer Received:', self.pipe.recv()
#
#
# if __name__ == '__main__':
#     pipe = Pipe()
#     p = Producer(pipe[0])
#     c = Consumer(pipe[1])
#     p.daemon = c.daemon = True
#     p.start()
#     c.start()
#     p.join()
#     c.join()
#     print 'Ended!'



# from multiprocessing import Lock, Pool
# import time
#
#
# def function(index):
#     print 'Start process: ', index
#     time.sleep(3)
#     print 'End process', index
#
#
# if __name__ == '__main__':
#     pool = Pool(processes=3)
#     for i in xrange(4):
#         pool.apply_async(function, (i,))
#
#     print "Started processes"
#     pool.close()
#     pool.join()
#     print "Subprocess done."




# from multiprocessing import Lock, Pool
# import time
#
#
# def function(index):
#     print 'Start process: ', index
#     time.sleep(3)
#     print 'End process', index
#
#
# if __name__ == '__main__':
#     pool = Pool(processes=3)
#     for i in xrange(4):
#         pool.apply(function, (i,))
#
#     print "Started processes"
#     pool.close()
#     pool.join()
#     print "Subprocess done."



from multiprocessing import Pool
import requests
from requests.exceptions import ConnectionError


def scrape(url):
    try:
        print requests.get(url)
    except ConnectionError:
        print 'Error Occured ', url
    finally:
        print 'URL ', url, ' Scraped'


if __name__ == '__main__':
    pool = Pool(processes=3)
    urls = [
        'https://www.baidu.com',
        'http://www.meituan.com/',
        'http://blog.csdn.net/'
    ]
    pool.map(scrape, urls)





























