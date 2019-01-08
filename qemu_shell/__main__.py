#!/usr/bin/python

#import lexer as ssp
import os
import sys
from argparse import ArgumentParser
from argparse import Action

DESCRIPTION = ''

class PathAction(argparse.Action):
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

def main(stream=None):
    parser = ArgumentParser(description=DESCRIPTION)

    parser.add_option('-L', '--loader-prefix-path',
            action=PathAction, dest='loader_prefix_path',
            help='Dynamic loader prefix path.')

    parser.add_option('-l', '--loader-search-path',
            action=PathAction, dest='loader_search_path',
            help='Path where dynamic loader search for libraries.')

    optparser.add_option('-p', '--binary-path',
            action=PathAction, dest='binary_path',
            help='Path where shell search for binaries.')

    optparser.add_option('-v', '--version',
            action='version', version='%(prog)s 0.1')

    var = input("qemu-shell$")
    print(var)
#    result = ssp.get_parser().parse('ls')

if __name__ == '__main__':
    main()
