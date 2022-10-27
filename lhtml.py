#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
import os
from xml.etree import ElementTree


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

    for file in args.files:
        file_dir = os.path.dirname(file)
        file_tree = ElementTree.parse(file)
        for importee in file_tree.iterfind('.//*[@import]'):
            file_to_import = os.path.join(file_dir, importee.attrib['import'])
            imported = ElementTree.parse(file_to_import).getroot()

            del importee.attrib['import']
            importee.attrib.update(imported.attrib)
            importee.text = imported.text
            importee.extend(imported.iterfind('.*'))

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
