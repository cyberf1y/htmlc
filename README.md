#
htmlc

## Installation
```sh
git clone git@github.com:cyberf1y/htmlc.git
chmod +x htmlc/htmlc.py
ln -s "$PWD/htmlc/htmlc.py" ~/.local/bin/
```

## Name
*htmlc* - HTML compiler

## Synopsis
```sh
htmlc.py [-h] [-o DIR] FILE [FILE ...]
```

## Description
*htmlc* is a tool for compiling HTML files, allowing the reuse of HTML elements,
without relying on JavaScript.

### Imports
*htmlc* can reuse HTML elements with the attribute `import`.

### `import`
Setting the attribute `import=file.html:xpath` of an HTML element replaces its
inner HTML with the inner HTML of the element in *file.html*, described by
*xpath* ([supported *XPath* syntax](
https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support)).

#### Example
Execute
```sh
cd examples
../htmlc.py index.html # or htmlc.py index.html, if htmlc.py is in the PATH
```
