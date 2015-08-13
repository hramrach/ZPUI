#!/usr/bin/env python

from input import input
from menu.menu import Menu
from output import output
from wm import window_manager

import logging
from time import sleep
from subprocess import call

level = logging.INFO

logging.basicConfig(level=level)

def start_io()
    logging.info("Starting IO drivers.")
    global listener
    global screen
    listener = input.listener
    screen = output.screen
    listener.listen_direct()

def run_wm():
    wmr = window_manager.WindowManagerRunner(listener, screen)
    wmr.run()

if __name__ == "__main__":
    try:
        start_io()
        run_wm()
    except:
        input.driver.deactivate()

