from contextlib import contextmanager
from multiprocessing.managers import BaseManager


# Manager
class Client(BaseManager):

    @contextmanager
    def write_cursor(self):
        lock = self.get_lock()
        lock.acquire()
        try:
            self.execute('BEGIN TRANSACTION')
            yield self
        except Exception as e:
            print(f'ERROR {e}')
            self.get_conn().rollback()
        else:
            self.get_conn().commit()
        finally:
            lock.release()


Client.register('execute')
Client.register('executemany')
Client.register('get_conn')
Client.register('get_lock')
Client.register('set_db')


if __name__ == '__main__':
    ...
    # import threading
    # print(threading.get_native_id())

    # client = Client(address=('', 50000), authkey=b"123")
    # client.connect()
    # import random

    # while True:
    #     print('pre enter')
    #     with client.write_cursor() as cursor:
    #         print(cursor.execute('INSERT INTO test_table(value) VALUES (?) RETURNING value', (random.randint(0, 100),)))
    #         print(cursor.execute('SELECT COUNT(*) FROM test_table'))
    #         print('----')
    #         time.sleep(1)
    #     print('exited')
    #     # time.sleep(random.random())
