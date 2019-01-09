#!/usr/bin/python3

import lexer as ssp
import os
import sys
import subprocess
from argparse import ArgumentParser
from argparse import Action

DESCRIPTION = ''

class PathAction(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(PathAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))

#def export_loader_path(path):
#    os.environ['QEMU_LD_PREFIX'] = path

#def add_libraries_path(path):
#    _path = os.environ['LD_LIBRARY_PATH']
#    _path.append(':')
#    _path.append(path)

#def add_binary_path(path):
#    _path = os.environ['PATH']
#    _path.append(':')
#    _path.append(path)

def get_full_path(cmd):
    try:
        output = subprocess.check_output(['which', cmd], shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("{}".format(e.output))
        sys.exit(1)
    return output

def get_arch(cmd):
    output = subprocess.check_output(['file', '-b', cmd])
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

    command = None
    while True:
        command = input("qemu-shell$ ")
        if command.startswith("exit"):
            break
        result = ssp.get_parser().parse(command)
        for p in result:
            path = get_full_path(p.getCommand().getProgram())
            arch = get_arch(path)
            print(p)
            print("path:{} | arch:{}".format(path, arch))

if __name__ == '__main__':
    main()
