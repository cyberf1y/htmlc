#!/usr/bin/env python3
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description='link HTML files')
    parser.add_argument(dest='files', metavar='FILE', nargs='+')
    parser.add_argument('-o', '--output', metavar='DIR', default='output')
    parser.parse_args()


if __name__ == '__main__':
    main()
