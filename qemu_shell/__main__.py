#!/usr/bin/python3

import lexer as ssp
import os
import sys
import subprocess
import shlex
from argparse import ArgumentParser
from argparse import Action

DESCRIPTION = ''

class PathAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(PathAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string == "-p" or option_string == "--binary-path":
            _path = os.environ['PATH']
            os.environ['PATH'] = _path + ":" + values
        elif option_string == "-L" or option_string == "--loader-prefix-path":
            os.environ['QEMU_LD_PREFIX'] = path
        elif option_string == "-l" or option_string == "--loader-search-path":
            _path = os.environ['LD_LIBRARY_PATH']
            os.environ['LD_LIBRARY_PATH'] = _path + ":" + values

def get_full_path(cmd):
    try:
        output = subprocess.check_output(["which", cmd], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return None
    return output.strip()

def get_arch(cmd):
    try:
        output = subprocess.check_output(["file", "-b", "-L", cmd], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        return None
    properties = output.split(',')
    return properties[1]

def main(stream=None):
    parser = ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-L', '--loader-prefix-path',
            action=PathAction, dest='loader_prefix_path',
            help='Dynamic loader prefix path.')

    parser.add_argument('-l', '--loader-search-path',
            action=PathAction, dest='loader_search_path',
            help='Path where dynamic loader search for libraries.')

    parser.add_argument('-p', '--binary-path',
            action=PathAction, dest='binary_path',
            help='Path where shell search for binaries.')

    parser.add_argument('-v', '--version',
            action='version', version='%(prog)s 0.1')

    args = parser.parse_args()

    final_command = ""
    while True:
        command = input("qemu-shell$ ")
        if command.startswith("exit"):
            break
        elif command == "" or command.isspace():
            continue
        result = ssp.get_parser().parse(command)
        for p in result:
            path = get_full_path(p.getCommand().getProgram())
            if path is None:
                print("{}: command not found".format(p.getCommand().getProgram()))
                break
            arch = get_arch(path)
            print(p)
            print("path:{} | arch:{}".format(path, arch))
        args = shlex.split(command)
        try:
            output = subprocess.check_output(args, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print("Cos nie tal")

if __name__ == '__main__':
    main()
