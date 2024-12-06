import unittest
from hard_connect import HardConnect
import logging
import threading
import socket
import time
import os


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    
    # bind port
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    
    print(f"Server started. Listening on {host}:{port}")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected with {addr}")
            message = client_socket.recv(1024)
            
            if message:
                print(f"Received: {message.decode('utf-8')}")
                client_socket.sendall(b"Hello, client")
            else:
                print("No message from client.")
            
            client_socket.close()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()


class TestHardConnect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 启动测试服务器
        cls.server_thread = threading.Thread(target=start_server, args=(6000,))
        cls.server_thread.daemon = True 
        cls.server_thread.start()
        time.sleep(2) # 确保启动成功  

    def setUp(self):
        self.hard_connect1 = HardConnect(conn_type='socket', ip='127.0.0.1', port=6000, logging_filename='test.log', logging_level=logging.INFO)
        self.hard_connect2 = HardConnect(conn_type='socket', ip='127.0.0.1', port=6000, logging_filename='test2.log', logging_level=logging.DEBUG)
        self.hard_connect3 = HardConnect(conn_type='socket', ip='127.0.0.1', port=6000, logging_filename='test3.log', logging_level=logging.INFO)

    def tearDown(self):
        # 清理操作，把生成的log文件删除
        self.hard_connect1.disconnect()
        self.hard_connect2.disconnect()
        self.hard_connect3.disconnect()
        if os.path.exists('test.log'):
            os.remove('test.log')
        if os.path.exists('test2.log'):
            os.remove('test2.log')
        if os.path.exists('test3.log'):
            os.remove('test3.log')

    def test_send(self):
        self.hard_connect1.send('hard1 send  1')
        self.hard_connect2.send('hard2 send  2')
        self.hard_connect3.send('hard3 send  3')
        # 判断对应的log 文件是否有数据
        with open('test.log', 'r') as f:
            self.assertIn('hard1 send  1', f.read())
        with open('test2.log', 'r') as f:
            self.assertIn('hard2 send  2', f.read())
        with open('test3.log', 'r') as f:
            self.assertIn('hard3 send  3', f.read())


if __name__ == '__main__':
    unittest.main()