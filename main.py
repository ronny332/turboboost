import os
import sys

from argparse import ArgumentParser
from getpass import getuser

task = {
    'dev': '/sys/devices/system/cpu/intel_pstate/no_turbo',
    'name': 'Turbo Boost'
}


def detect_action():
    global task

    parser = ArgumentParser(description='toggle Intel Turbo Boost or show current state')
    parser.add_argument('action', choices=['on', 'off', 'show'])

    task['action'] = parser.parse_args().action


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
        sys.exit('missing rights to save new state, try sudo [command] instead')


def show():
    print(f'{task["name"]} is {get_state()[1]}')


if __name__ == '__main__':
    detect_action()
    detect_env()
    # print(task)

    run_task()
