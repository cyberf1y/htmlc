#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter


class LHTMLError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def main():
    parser = ArgumentParser(description='link HTML files')
    parser.add_argument(dest='files', metavar='FILE', nargs='+')
    parser.add_argument('-o', '--output', metavar='DIR', default='output')
    args = parser.parse_args()

    for file, n in Counter(args.files).items():
        if n > 1:
            raise LHTMLError(f'"{file}" appears {n} times in the argument list')


if __name__ == '__main__':
    main()
