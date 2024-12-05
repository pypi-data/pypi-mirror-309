#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.03.16 12:00:00                  #
# ================================================== #

import serial
import time

from PySide6.QtCore import Slot

from pygpt_net.plugin.base import BaseWorker, BaseSignals


class WorkerSignals(BaseSignals):
    pass  # add custom signals here


class Worker(BaseWorker):
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        self.args = args
        self.kwargs = kwargs
        self.plugin = None
        self.cmds = None
        self.ctx = None
        self.msg = None

    @Slot()
    def run(self):
        responses = []
        for item in self.cmds:
            response = None
            try:
                if item["cmd"] in self.plugin.allowed_cmds and self.plugin.has_cmd(item["cmd"]):

                    # serial: send text command
                    if item["cmd"] == "serial_send":
                        response = self.cmd_serial_send(item)

                    # serial: send raw bytes command
                    elif item["cmd"] == "serial_send_bytes":
                        response = self.cmd_serial_send_bytes(item)

                    # serial: read data from USB port
                    elif item["cmd"] == "serial_read":
                        response = self.cmd_serial_read(item)

                    if response:
                        responses.append(response)

            except Exception as e:
                responses.append({
                    "request": {
                        "cmd": item["cmd"],
                    },
                    "result": "Error {}".format(e),
                })
                self.error(e)
                self.log("Error: {}".format(e))

        # send response
        if len(responses) > 0:
            for response in responses:
                self.reply(response)

        if self.msg is not None:
            self.status(self.msg)

    def cmd_serial_send(self, item: dict) -> dict:
        """
        Send command to USB port

        :param item: command item
        :return: response item
        """
        request = self.prepare_request(item)
        port = self.plugin.get_option_value("serial_port")
        speed = self.plugin.get_option_value("serial_bps")
        timeout = self.plugin.get_option_value("timeout")
        sleep = self.plugin.get_option_value("sleep")
        self.log("Using serial port: {} @ {} bps".format(port, speed))
        try:
            self.msg = "Sending command to USB port: {}".format(
                item["params"]['command'],
            )
            self.log(self.msg)
            data = self.send_command(
                port,
                speed,
                item["params"]['command'],
                timeout=timeout,
                sleep=sleep,
            )
            self.log("Response: {}".format(data))
            response = {
                "request": request,
                "result": data,
            }
        except Exception as e:
            response = {
                "request": request,
                "result": "Error: {}".format(e),
            }
            self.error(e)
            self.log("Error: {}".format(e))
        return response

    def cmd_serial_send_bytes(self, item: dict) -> dict:
        """
        Send raw bytes to USB port

        :param item: command item
        :return: response item
        """
        request = self.prepare_request(item)
        port = self.plugin.get_option_value("serial_port")
        speed = self.plugin.get_option_value("serial_bps")
        timeout = self.plugin.get_option_value("timeout")
        sleep = self.plugin.get_option_value("sleep")
        self.log("Using serial port: {} @ {} bps".format(port, speed))
        try:
            self.msg = "Sending binary data to USB port: {}".format(
                item["params"]['bytes'],
            )
            self.log(self.msg)
            data = self.send_binary_data(
                port,
                speed,
                int(item["params"]['bytes']),
                timeout=timeout,
                sleep=sleep,
            )
            self.log("Response: {}".format(data))
            response = {
                "request": request,
                "result": data,
            }
        except Exception as e:
            response = {
                "request": request,
                "result": "Error: {}".format(e),
            }
            self.error(e)
            self.log("Error: {}".format(e))
        return response

    def cmd_serial_read(self, item: dict) -> dict:
        """
        Read data from USB port

        :param item: command item
        :return: response item
        """
        request = self.prepare_request(item)
        port = self.plugin.get_option_value("serial_port")
        speed = self.plugin.get_option_value("serial_bps")
        timeout = self.plugin.get_option_value("timeout")
        duration = int(item["params"]['duration']) \
            if "duration" in item["params"] else 3
        self.log("Using serial port: {} @ {} bps".format(port, speed))
        try:
            self.msg = "Reading data from USB port..."
            self.log(self.msg)
            data = self.read_data(
                port,
                speed,
                timeout=timeout,
                duration=duration,
            )
            self.log("Response: {}".format(data))
            response = {
                "request": request,
                "result": data,
            }
        except Exception as e:
            response = {
                "request": request,
                "result": "Error: {}".format(e),
            }
            self.error(e)
            self.log("Error: {}".format(e))
        return response

    def send_command(
            self,
            port: str,
            speed: int,
            command: str,
            timeout: int = 1,
            sleep: int = 2
    ) -> str:
        """
        Send command to USB port

        :param port: USB port name, e.g. /dev/ttyACM0
        :param speed: Port connection speed, in bps, default: 9600
        :param command: Command to send
        :param timeout: Timeout in seconds
        :param sleep: Sleep time in seconds
        :return: Response from USB port
        """
        ser = serial.Serial(port, speed, timeout=timeout)
        time.sleep(sleep)
        ser.write((command + '\n').encode())
        ser.flush()
        return ser.readline().decode().strip()

    def send_binary_data(
            self,
            port: str,
            speed: int,
            data: int,
            timeout: int = 1,
            sleep: int = 2
    ) -> str:
        """
        Send command to USB port

        :param port: USB port name, e.g. /dev/ttyACM0
        :param speed: Port connection speed, in bps, default: 9600
        :param data: Data to send
        :param timeout: Timeout in seconds
        :param sleep: Sleep time in seconds
        :return: Response from USB port
        """
        ser = serial.Serial(port, speed, timeout=timeout)
        time.sleep(sleep)
        ser.write(bytes(data))
        ser.flush()
        return ser.readline().decode().strip()

    def read_data(
            self,
            port: str,
            speed: int,
            timeout: int = 1,
            duration: int = 3
    ) -> str:
        """
        Read data from USB port

        :param port: USB port name, e.g. /dev/ttyACM0
        :param speed: Port connection speed, in bps, default: 9600
        :param timeout: Timeout in seconds
        :param duration: Duration in seconds
        :return: Response from USB port
        """
        data = ""
        ser = serial.Serial(port, speed, timeout=timeout)
        end_time = time.time() + duration
        while time.time() < end_time:
            if ser.in_waiting > 0:
                data += ser.readline().decode().strip()
        return data

    def prepare_request(self, item) -> dict:
        """
        Prepare request item for result

        :param item: item with parameters
        :return: request item
        """
        return {"cmd": item["cmd"]}
