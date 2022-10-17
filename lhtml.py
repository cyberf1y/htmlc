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
                page = ElementTree.parse(f'{href[1:-5]}.xml')
            except ElementTree.ParseError as err:
                raise LHTMLError(f'{href[1:-5]}.xml: {err}') from err

            hrefs.update(
                a.attrib['href'] for a in page.iterfind('.//a[@href]'))
            pages[href] = page

    template = pages.pop('/template.html')
    title = template.find('head/title')
    title_text = title.text
    template_main = template.find('.//main')

    for href, page in pages.items():
        page_attrib = page.getroot().attrib

        # fill the title
        if 'title' in page_attrib:
            title.text = f'{page_attrib["title"]} | {title_text}'
            for e in page.iterfind('.//*[@title-value="true"]'):
                del e.attrib['title-value']
                e.text = page_attrib['title']
        else:
            title.text = title_text

        # import values
        for importee in page.iterfind('.//*[@import]'):
            # load the tree only if it isn't already loaded
            imported = pages.get(
                f'/{importee.attrib["import"][:-4]}.html',
                ElementTree.parse(importee.attrib['import'])
            )
            imported_root = imported.getroot()
            for key_value in importee.attrib['values'].split(';'):
                key, value = key_value.split('=')
                for e in importee.iterfind(f'.//*[@import-value="{key}"]'):
                    del e.attrib['import-value']
                    imported_value = imported.find(value)
                    imported_value_content = list(imported_value.iterfind('.*'))

                    # if the imported value has no content, try looking at
                    # its attributes
                    if not imported_value.text and not imported_value_content:
                        if f'{key}-value' in imported_value.attrib:
                            e.text = imported_root.attrib[key]
                    else:
                        e.text = imported_value.text
                        e.extend(imported_value.iterfind('.*'))

            del importee.attrib['import']
            del importee.attrib['values']

        # fill the template's main
        template_main.clear()
        template_main.extend(page.iterfind('.*'))
        # available since python 3.9
        # ElementTree.indent(template, space='  ', level=0)
        page = ElementTree.tostring(
            template.getroot(), encoding='utf-8', method='html')

        # write the page
        with open(href[1:], 'wb') as file:
            file.write(b'<!DOCTYPE html>\n')
            file.write(page)


if __name__ == '__main__':
    main()
