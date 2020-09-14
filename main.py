#!/usr/bin/env python3
import os
import subprocess
import sys

from argparse import ArgumentParser
from getpass import getuser

task = {
    'dev': '/sys/devices/system/cpu/intel_pstate/no_turbo',
    # file : os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.split(__file__)[-1])),
    'file': sys.argv[0],
    'name': 'Turbo Boost'
}


def detect_action():
    global task

    parser = ArgumentParser(description='toggle Intel Turbo Boost or show current state')
    parser.add_argument('action', choices=['on', 'off', 'show'])
    parser.add_argument('-e', '--exit', action='store_true', help='exit on missing permissions')

    args = parser.parse_args()
    task['action'] = args.action
    task['exit'] = args.exit


def detect_env():
    global task

    task['user'] = getuser()


def get_state():
    with open(task['dev'], 'r') as f:
        state = not bool(int(f.read().strip()))

        return state, 'on' if state else 'off'


def run_task():
    global task

    if task['action'] != 'show':
        set_state()
    show()


def set_state():
    state = not get_state()[0]
    val = None

    if not state and task['action'] == 'off':
        val = '1'
    elif state and task['action'] == 'on':
        val = '0'

    if os.access(task['dev'], os.O_RDWR):
        if val is not None:
            f = os.open(task['dev'], os.O_RDWR)
            os.write(f, bytes(val, 'utf-8'))
            os.close(f)
    elif val is not None:
        if task['exit']:
            sys.exit('missing rights to save new state, try sudo [command] instead')
        else:
            args = list()
            args.append('sudo')
            args.append(task['file'])
            args.append(sys.argv[-1])
            r = subprocess.run(args)
            sys.exit(r.returncode)


def show():
    print(f'{task["name"]} is {get_state()[1]}')


if __name__ == '__main__':
    detect_action()
    detect_env()
    # print(task)

    run_task()
