#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：base_modbus.py
@Author  ：KING
@Date    ：2024/6/20 09:11 
"""
from pymodbus.client import ModbusTcpClient
from typing import Union
from hard_connect.utils import BaseConn


class ModbusTcpClientConn(BaseConn):
    """
    """
    def __init__(
            self,
            ip: str,
            port: int,
            timeout: int = 1,
            **kwargs
    ):
        """

        :param ip:       server ip
        :param port:     server port
        :param length:   receive data length
        :param kwargs:
        """
        super().__init__(ip, port, **kwargs)
        self.ip = ip
        self.port = port if isinstance(port, int) else int(port)
        self.timeout = timeout
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn: ModbusTcpClient = ModbusTcpClient(self.ip, self.port, timeout=self.timeout)
        except Exception as e:
            raise e

    def disconnect(self):
        self.conn and self.conn.close()
        self.conn = None

    def send(self, send_str: Union[str, bytes]):
        """
        :param send_str: message
        :return:
        """
        pass

    def receive(
            self,
            length: int = None,
            receive_data: bytes = None,
    ) -> Union[bytes, None]:
        """
        :param length:
        :param receive_data:
        :param :
        :return:
        """
        pass

    def send_receive(self, send_str: Union[str, bytes], receive_length=None) -> str:
        """
        :param send_str:
        :param receive_length:
        :return:
        """
        self.send(send_str)
        receive_data = b''
        receive_data = self.receive(
            length=receive_length,
            receive_data=receive_data
        )
        return receive_data.decode().strip() if receive_data else None
