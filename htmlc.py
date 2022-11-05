#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
import os
import sys
from xml.etree import ElementTree


class HTMLCArgumentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HTMLCImportError(Exception):
    def __init__(self, file, message):
        self.file = file
        self.message = message
        super().__init__(f'{self.file}: {self.message}')


class HTMLCParseError(Exception):
    def __init__(self, file, message):
        self.message = message
        self.file = file
        super().__init__(f'{self.file}: {self.message}')


def main():
    parser = ArgumentParser(description='HTML compiler')
    parser.add_argument(dest='files', metavar='FILE', nargs='+')
    parser.add_argument('-o', '--output', metavar='DIR', default='output')
    args = parser.parse_args()

    for file, n in Counter(args.files).items():
        if n > 1:
            raise HTMLCArgumentError(f'"{file}" passed more ({n}) than once')

    loaded_file_trees = dict()
    def load_file_tree(file):
        try:
            return loaded_file_trees.setdefault(file, ElementTree.parse(file))
        except ElementTree.ParseError as e:
            raise HTMLCParseError(file, e) from e

    for file in args.files:
        file_dir = os.path.dirname(file)
        try:
            file_tree = load_file_tree(file)
        except FileNotFoundError as e:
            raise HTMLCArgumentError(f'"{file}" not found') from e

        for importee in file_tree.iterfind('.//*[@import]'):
            try:
                import_file, xpath = importee.attrib['import'].split(':')
            except ValueError as e:
                bad_syntax = f'bad syntax: "import={importee.attrib["import"]}"'
                raise HTMLCImportError(file, bad_syntax) from e

            import_path = os.path.join(file_dir, import_file)
            try:
                imported = load_file_tree(import_path).find(xpath)
            except FileNotFoundError as e:
                import_not_found = f'"{import_path}" not found'
                raise HTMLCImportError(file, import_not_found) from e

            del importee.attrib['import']
            importee.attrib.update(imported.attrib)
            importee.text = imported.text
            importee.extend(imported.iterfind('.*'))

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
