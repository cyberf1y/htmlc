from xml.etree import ElementTree


class LHTMLError(Exception):
    """Add more information to ElementTree.ParseError"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def main():
    # starting with template.xml, follow the hrefs in a bfs manner
    hrefs = set(['/template.html'])
    pages = dict()
    while hrefs:
        href = hrefs.pop()
        href_is_root_relative = href.startswith('/') and href.endswith('.html')
        if href_is_root_relative and href not in pages:
            # /path/to/page.html is produced using path/to/page.xml
            try:
                page_tree = ElementTree.parse(f'{href[1:-5]}.xml')
            except ElementTree.ParseError as err:
                raise LHTMLError(f'{href[1:-5]}.xml: {err}') from err

            hrefs.update(
                a.attrib['href'] for a in page_tree.iterfind('.//a[@href]'))
            pages[href] = page_tree

    template_tree = pages.pop('/template.html')
    template_tree_root = template_tree.getroot()
    title_element = template_tree.find('head/title')
    title = title_element.text
    template_main_tree = template_tree.find('.//main')

    for href, page_tree in pages.items():
        page_tree_attrib = page_tree.getroot().attrib

        # fill the title
        if 'title' in page_tree_attrib:
            title_element.text = f'{page_tree_attrib["title"]} | {title}'
            for e in page_tree.iterfind('.//*[@title-value="true"]'):
                del e.attrib['title-value']
                e.text = page_tree_attrib['title']
        else:
            title_element.text = title

        # import values
        if 'import' in page_tree_attrib and 'values' in page_tree_attrib:
            # load the tree only if it isn't already loaded
            import_href = f'/{page_tree_attrib["import"][:-4]}.html'
            if import_href in pages:
                imported_tree = pages[import_href]
            else:
                imported_tree = ElementTree.parse(page_tree_attrib['import'])

            for key_value in page_tree_attrib['values'].split(';'):
                key, value = key_value.split('=')
                for e in page_tree.iterfind(f'.//*[@import-value="{key}"]'):
                    del e.attrib['import-value']
                    import_value_element = imported_tree.find(value)
                    if import_value_element.text:
                        e.text = import_value_element.text
                    elif f'{key}-value' in import_value_element.attrib:
                        e.text = imported_tree.getroot().attrib[key]

        # fill the template's main
        template_main_tree.clear()
        template_main_tree.extend(page_tree.iterfind('.*'))
        # available since python 3.9
        # ElementTree.indent(template_tree, space='  ', level=0)
        page = ElementTree.tostring(
            template_tree_root, encoding='utf-8', method='html')

        # write the page
        with open(href[1:], 'wb') as file:
            file.write(b'<!DOCTYPE html>\n')
            file.write(page)


if __name__ == '__main__':
    main()
