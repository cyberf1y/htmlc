#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
import os
import sys
from xml.etree import ElementTree


class HTMLCError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def main():
    parser = ArgumentParser(description='HTML compiler')
    parser.add_argument(dest='files', metavar='FILE', nargs='+')
    parser.add_argument('-o', '--output', metavar='DIR', default='output')
    args = parser.parse_args()

    for file, n in Counter(args.files).items():
        if n > 1:
            raise HTMLCError(f'"{file}" appears {n} times in the argument list')

    loaded_file_trees = dict()
    def get_loaded_file_tree(file):
        return loaded_file_trees.setdefault(file, ElementTree.parse(file))

    for file in args.files:
        file_dir = os.path.dirname(file)
        file_tree = get_loaded_file_tree(file)
        for importee in file_tree.iterfind('.//*[@import]'):
            import_file, xpath = importee.attrib['import'].split(':')
            import_path = os.path.join(file_dir, import_file)
            imported = get_loaded_file_tree(import_path).find(xpath)

            del importee.attrib['import']
            importee.attrib.update(imported.attrib)
            importee.text = imported.text
            importee.extend(imported.iterfind('.*'))

        if sys.version_info.minor >= 9:
            ElementTree.indent(file_tree, space='  ', level=0)

        file_string = ElementTree.tostring(
            file_tree.getroot(),
            encoding='utf-8',
            method='html',
        )

        os.makedirs(os.path.join(args.output, file_dir), exist_ok=True)
        with open(os.path.join(args.output, file), 'wb') as fd:
            fd.write(b'<!DOCTYPE html>\n')
            fd.write(file_string)


if __name__ == '__main__':
    main()
