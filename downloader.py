import threading
import d_thread
import log
import time


class Downloader:

    QUEUE_NUM = 10
    THDREAD_AWAIT = 0.5
    gallery_dir = ''
    image_list = []
    count = 0
    log = log.log("threads")
    STOP_WORK = False

    def __init__(self, imgx, username):
        self.gallery_dir = './GALLERIES/' + username
        self.image_list = imgx
        self.queue_manager()

    def set_stop_work(self):
        self.STOP_WORK = True

    def queue_manager(self):
        while len(self.image_list) > 0:
            if len(self.image_list) > self.QUEUE_NUM:
                for num in range(self.QUEUE_NUM):
                    if self.STOP_WORK:
                        break
                    if threading.active_count() < self.QUEUE_NUM:
                        t = d_thread.DThread(self.gallery_dir, self.image_list[num], self.count)
                        t.start()
                        self.image_list.pop(num)
                        self.count += 1
                        print(f'COUNT: {self.count}\tWorking Threads: {threading.active_count()},\t IMG: {len(self.image_list)} \t THREAD: {t.ident}')
                    else:
                        time.sleep(self.THDREAD_AWAIT)
                        print(f'Waiting threads free ({self.THDREAD_AWAIT} sec.)')
            else:
                for num in range(len(self.image_list)):
                    if self.STOP_WORK:
                        break
                    if threading.active_count() < self.QUEUE_NUM:
                        t = d_thread.DThread(self.gallery_dir, self.image_list[num], self.count)
                        t.start()
                        self.image_list.pop(num)
                        self.count += 1
                        print(f'COUNT: {self.count}\tWorking Threads: {threading.active_count()},\t IMG: {len(self.image_list)} \t THREAD: {t.ident}')
                    else:
                        time.sleep(self.THDREAD_AWAIT)
                        print(f'Waiting threads free ({self.THDREAD_AWAIT} sec.)')
                pass
        self.STOP_WORK = False
        self.count = 0


    def kill_threads(self):
        for t in self.threads:
            if t.is_alive():
                pass
            else:
                pass




