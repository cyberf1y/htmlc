import re
from xml.etree import ElementTree


def get_ahrefs_iter(tree):
    """Return an iterator yielding the hrefs of all anchors in the tree."""
    return (a.attrib['href'] for a in tree.iterfind('.//a[@href]'))


def main():
    template_tree = ElementTree.parse('template.xml')

    # match site root relative paths to .html files
    html_file_pattern = re.compile(r'/.+\.html')

    # start from the hrefs in template tree, and do a bfs
    pages = dict()
    hrefs = set(get_ahrefs_iter(template_tree))
    while hrefs:
        href = hrefs.pop()
        if re.match(html_file_pattern, href) and href not in pages:
            # /path/to/page.html corresponds to path/to/page.xml
            page_tree = ElementTree.parse(f'{href[1:-5]}.xml')
            hrefs.update(get_ahrefs_iter(page_tree))
            pages[href] = page_tree

    # fill in imported values
    for page_tree in pages.values():
        page_tree_attrib = page_tree.getroot().attrib
        if 'import' in page_tree_attrib and 'values' in page_tree_attrib:
            # load the tree if it isn't already loaded
            import_href = f'/{page_tree_attrib["import"][:-4]}.html'
            if import_href in pages:
                imported_tree = pages[import_href]
            else:
                imported_tree = ElementTree.parse(page_tree_attrib['import'])

            for key_value in page_tree_attrib['values'].split(';'):
                key, value = key_value.split('=')
                for e in page_tree.iterfind(f'.//*[@import-value="{key}"]'):
                    e.clear()
                    e.text = imported_tree.find(value).text

    # fill the template, and write it
    for href, page_tree in pages.items():
        main_tree = template_tree.find('.//main')
        main_tree.clear()
        main_tree.extend(page_tree.iterfind('.*'))
        ElementTree.indent(template_tree, space='  ', level=0)

        page_root = template_tree.getroot()
        page = ElementTree.tostring(page_root, encoding='utf-8', method='html')

        with open(href[1:], 'wb') as file:
            file.write(b'<!DOCTYPE html>\n')
            file.write(page)


if __name__ == '__main__':
    main()
