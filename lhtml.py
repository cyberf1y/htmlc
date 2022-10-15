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

    for href, page_tree in pages.items():
        main_tree = template_tree.find('.//main')
        main_tree.clear()
        main_tree.extend(page_tree.iterfind('.*'))
        ElementTree.indent(template_tree, space='  ', level=0)
        template_tree.write(href[1:], encoding='utf-8', method='html')


if __name__ == '__main__':
    main()
