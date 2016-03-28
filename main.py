#!/usr/bin/env python
import sys
#Welcome to pyLCI innards
#Here, things are about i and o, which are input and output
#And we output things for debugging, so o goes first.
from output import output

#These lines are here so that welcome screen stays on a little longer:
o = output.screen
from ui import Printer
Printer(["Welcome to", "pyLCI"], None, o, 0)

try:
    #All the LCI-related modules are imported here
    from input import input
    from ui import Menu
    #Now we init the input.
    input.init()
    i = input.listener
    i.listen()
    #from apps import app_list
except:
    #Printer("Oops. :(", "y u make mistake", i, o, 0) #Yeah, that's about all the debug data. 
    #import time;time.sleep(3) #u make mi sad i go to slip
    #o.clear()
    raise

#Here go all native Python modules. It's close to impossible to screw that up.
from subprocess import call
from time import sleep
import importlib
import argparse

#Now we go and import all the apps.
import apps
app_list = {}

def launch(name=None):
    if name != None:
        app = load_app(name)
        exception_wrapper(app.callback)
    else:
        app_menu_contents = load_all_apps()
        app_menu = Menu(app_menu_contents, i, o, "App menu", append_exit=False)
        exception_wrapper(app_menu.activate)

def exception_wrapper(callback):
    try:
        callback()
    except KeyboardInterrupt:
        Printer(["Does Ctrl+C", "hurt scripts?"], i, o, 0)
        i.stop_listen()
        sys.exit(1)
    except:
        Printer(["A wild exception", "appears!"], i, o, 0)
        i.stop_listen()
        raise
    else:
        Printer("Exiting pyLCI", i, o, 0)
        i.stop_listen()
        sys.exit(0)

def load_all_apps():
    menu_contents = []
    app_names = apps.module_names
    for app_name in app_names:
        print("Loading {}".format(app_name))
        try:
            app = load_app(app_name)
            menu_contents.append([app.menu_name, app.callback])
        except Exception as e:
            Printer(["Failed to load", app_name], i, o, 0)
            print("Failed to load {}".format(app_name))
            print(e)
            sleep(3)
            #raise
    return menu_contents

def load_app(name):
    global app_list
    app = importlib.import_module('apps.'+name+'.main')
    app.init_app(i, o)
    app_list[name] = app
    return app    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyLCI runner")
    parser.add_argument('-a', '--app', action="store", help="Launch pyLCI with a single app loaded (useful for testing)", default=None)
    args = parser.parse_args()
    launch(name=args.app)
