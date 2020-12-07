#!/usr/bin/env python3
import os
import re
import subprocess
import sys

from argparse import ArgumentParser
from getpass import getuser
from platform import system

task = {
    "dev": "/sys/devices/system/cpu/intel_pstate/no_turbo",
    "dev_governor": "/sys/devices/system/cpu/%NUM%/cpufreq/scaling_governor",
    # file : os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.split(__file__)[-1])),
    "file": sys.argv[0],
    "name": "Turbo Boost",
}


def detect_action():
    global task

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "-v"):
        task["verbose"] = True
        show()
        sys.exit(0)

    parser = ArgumentParser(description="toggle Intel Turbo Boost or show current state")
    parser.add_argument("action", choices=["on", "off"])
    parser.add_argument(
        "-e", "--exit", action="store_true", help="exit on missing permissions, don't use sudo instead"
    )
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="be quiet")

    args = parser.parse_args()
    task["action"] = args.action
    task["exit"] = args.exit
    task["verbose"] = args.verbose


def detect_env():
    global task

    task["user"] = getuser()


def detect_system():
    global task

    task["system"] = system()

    if task["system"] != "Linux":
        sys.exit("This script is only usable on a Linux based OS.")
        return

    if os.path.isfile(task["dev"]) and not os.access(task["dev"], os.O_RDONLY):
        sys.exit("Unable to find Intel Turbo Boost compatible CPU.")
        return

    cores = 0
    p = re.compile(r"cpu[0-9]+")

    for f in os.listdir(os.path.abspath(os.path.dirname(task["dev"]) + "/..")):
        if p.match(f):
            cores += 1

    task["cores"] = cores


def get_state():
    with open(task["dev"], "r") as f:
        state = not bool(int(f.read().strip()))

        return state, "on" if state else "off"


def run_task():
    global task

    if task["action"] != "show":
        set_state()
    show()


def set_governor(performance):
    device_parts = task["dev_governor"].split("/%NUM%/")
    governor = bytes("performance" if performance else "ondemand", "utf-8")

    if len(device_parts) == 2 and os.access(device_parts[0], os.O_RDWR):
        cpus = list(filter(lambda c: c.startswith("cpu"), os.listdir(device_parts[0])))

        for cpu in cpus:
            file = os.path.join(device_parts[0], cpu, device_parts[1])
            if os.access(file, os.O_RDWR):
                f = os.open(file, os.O_RDWR)
                os.write(f, governor)


def set_state():
    state = not get_state()[0]
    val = None

    if not state and task["action"] == "off":
        val = "1"
    elif state and task["action"] == "on":
        val = "0"

    if os.access(task["dev"], os.O_RDWR):
        if val is not None:
            f = os.open(task["dev"], os.O_RDWR)
            try:
                os.write(f, bytes(val, "utf-8"))
                set_governor(True if val == "0" else False)
            except PermissionError:
                sys.stderr.write("Unable to set Turbo Boost.\n")
            os.close(f)

    elif val is not None:
        if task["exit"]:
            sys.exit("missing rights to save new state, try sudo [command] instead.")
        else:
            args = list()
            args.append("sudo")
            args.append(task["file"])
            args.append(sys.argv[-1])
            r = subprocess.run(args)
            sys.exit(r.returncode)


def show():
    if task["verbose"]:
        print(f'{task["name"]} is {get_state()[1]}, running on {task["cores"]} core Intel CPU.')


if __name__ == "__main__":
    detect_system()
    detect_action()
    detect_env()
    # print(task)

    run_task()
