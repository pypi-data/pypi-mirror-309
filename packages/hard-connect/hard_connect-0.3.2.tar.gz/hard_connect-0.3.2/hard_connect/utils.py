#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：dequeue.py
@Author  ：KING
@Date    ：2024/6/11 12:49 
"""
import logging
import copy
import logging.config
from typing import Union, Generator
from collections import deque
from abc import ABC, abstractmethod


class BaseConn(ABC):

    def __init__(
            self,
            send_lf='\r\n',
            receive_lf='\r\n',
            queue_max_length=500,
            timeout: int = 1,
            end_of_msg='🔚',
            keep_line_feed=False,
            logging_level=logging.INFO,
            logging_filename=None,
            receive_generator: Generator = None,
    ):
        """
        Base class for communication, including serial, socket, etc.
        :param send_lf:            # send line feed, default: '\r\n'
        :param receive_lf:         # receive line feed, default: '\r\n'
        :param queue_max_length:   # queue max length, default: 500
        :param timeout:            # Send and receive timeout, default: 1s
        :param end_of_msg:         #  special tag data, Set the tag end_of_msg, which is not stored in the queue. Default  🔚
        :param keep_line_feed:     # Write queue data to preserve line breaks  default: False
        :param logging_level:      # Logging level, default: logging.INFO, DEBUG: write file and console, INFo: write console  # noqa
        :param logging_filename:   # Logging file name, default: None, if set, write log to file. If not set use default log setting
        :param receive_generator:  # Generator for receiving data, default: None, if set, use this generator to receive data
        """
        self.conn = None
        self.send_lf = send_lf
        self.receive_lf = receive_lf
        self.end_of_msg = end_of_msg
        self.keep_line_feed = keep_line_feed
        self.timeout = timeout
        self.queue = DequeWithMaxLen(queue_max_length)
        self.logging_filename = logging_filename
        self.receive_generator = receive_generator
        self.logger_name = f"hard_conn_{id(self)}" # dynmic generate logger
        self.init_logging(logging_level)
        self.logger = logging.getLogger(self.logger_name)
        
        super().__init__()

    def __del__(self):
        """
        close socket connection when object is destroyed
        :return:
        """
        self.receive_generator and self.receive_generator.close()
        self.disconnect()
        
        logger = logging.getLogger(self.logger_name)

        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)

        logging.Logger.manager.loggerDict.pop(self.logger_name, None)

    def __enter__(self):
        not self.conn and self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.receive_generator and self.receive_generator.close()
        self.disconnect()

    def init_logging(self, logging_level):
        """
        init logging
        :return:
        """

        from hard_connect.log import DEFAULT_LOGGING
        custom_logging_config = copy.deepcopy(DEFAULT_LOGGING)
        defined_handlers = list(custom_logging_config.get('handlers', {}).keys())    
        if self.logging_filename:
            custom_logging_config['handlers']['file']['filename'] = self.logging_filename
            
        custom_logging_config['loggers'][self.logger_name] = {
            'handlers': defined_handlers,
            'level': logging_level,
            'propagate': False,
        }

        logging.config.dictConfig(custom_logging_config)


    @abstractmethod
    def connect(self):
        """
        connect to the server
        :return:
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        disconnect from the server
        :return:
        """
        pass

    @abstractmethod
    def send(self, send_str: Union[str, bytes]):
        """
        send message to the server
        :param send_str:
        :return:
        """
        pass

    @abstractmethod
    def receive(self):
        """
        receive message from the server
        :return:
        """
        pass

    def put_queue(self, bytes_recv_line: bytes = None, bytes_recv_multi_lines: list = None):
        """
        sub thread receive data, put data to queue

        :param bytes_recv_line:
        :param bytes_recv_multi_lines:
        :return:
        """
        try:
            if bytes_recv_line is not None:
                bytes_recv_multi_lines = [bytes_recv_line]

            lines = [line.decode() for line in bytes_recv_multi_lines if len(line)]
            if not len(lines):
                return

            # discard end_of_msg
            if self.end_of_msg:
                lines = [line for line in lines if line != self.end_of_msg]

            # keep line feed
            if self.keep_line_feed:
                lines = [line + self.receive_lf for line in lines]

            self.logger.info(f'recv_data: {lines}')
            self.queue.extend_items(lines)

        except UnicodeDecodeError as e:
            self.logger.debug(f'Decode error: {e}', ' Resource Bytes:', repr(bytes_recv_line))
        pass

    def new_value(self, value_index=-1):
        """

        :param value_index: get value from queue, default: -1, get last value
        :return:
        """
        if self.queue.__len__() == 0:
            return None
        return self.queue.get_new_value(value_index)


class DequeWithMaxLen(deque):
    """
    FIFO queue with a maximum length. Default is 500

    If the queue is full, the oldest item will be removed.

    put: Put a new value in the queue
    popleft: Remove and return the leftmost item
    get: Alias of popleft
    get_new_value: Get Queue right value, but not remove it
    clear(): Clear the queue
    copy(): Return a shallow copy of the queue
    count(x): Return the number of items in the queue
    extend(iterable): Extend the right side of the queue by appending elements from the iterable
    """
    def __init__(
            self, max_length=500
    ):
        self.max_length = max_length
        super().__init__(maxlen=self.max_length)

    def put(self, item):
        if len(self) == self.max_length:
            self.popleft()
        self.append(item)

    def extend_items(self, iterable):
        new_len = len(self) + len(iterable)
        if new_len >= self.max_length:
            for _ in range(new_len - self.max_length):
                self.popleft()
        self.extend(iterable)

    def popleft(self):
        """
        Remove and return the leftmost item.
        :return:
        """
        return super().popleft()
    
    def get(self):
        return self.popleft()

    def get_new_value(self, value_index=-1):
        """
        Get Queue right value, but not remove it
        :return:
        """
        if len(self) == 0:
            return None
        return self[value_index]
