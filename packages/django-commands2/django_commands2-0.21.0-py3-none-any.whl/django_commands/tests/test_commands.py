#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import time

from threading import Thread
from django.test import TestCase
from django.core.management import call_command
from django_commands.management.commands.test_wait_commands import Command as TestWaitCommand


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
LOGGER = logging.getLogger("django_commands")
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)


class Test(TestCase):

    def test_wait_command(self):
        TestWaitCommand.create_task(1)
        TestWaitCommand.create_task(2)
        TestWaitCommand.create_task(3)
        thread = Thread(group=None, target=call_command, args=["test_wait_commands"])
        thread.start()
        time.sleep(0.1)
        print("创建任务")
        for i in range(4, 20):
            TestWaitCommand.create_task(i)
