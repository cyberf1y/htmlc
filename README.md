# lhtml
## Name
*lhtml* - link xml files into html pages

## Synopsis
```sh
py lhtml.py
```

## Description
Given a *template.xml*, follow all the hrefs in it, and generate html pages with
the *main* element replaced.

### Example:
Starting with the following files:
* [*template.xml*](example/template.xml):
```html
<html lang="en">
  <head>
    <title>site</title>
  </head>
  <body>
    <header>
      <nav>
        <ul>
          <li><a href="/index.html">Home</a></li>
          <li><a href="/about.html">About</a></li>
        </ul>
      </nav>
    </header>
    <main>
    </main>
    <footer>
      <p><small>Copyright &#169; cyberf1y 2022</small></p>
    </footer>
  </body>
</html>
```

* [*index.xml*](example/index.xml):
```html
<main>
  <p>Hi, thanks for stopping by!</p>
</main>
```

* [*about.xml*](example/about.xml):
```html
<main>
  <p>Hi, I am cyberf1y.</p>
</main>
```

*lhtml* will write the following:
* *index.html*
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>site</title>
  </head>
  <body>
    <header>
      <nav>
        <ul>
          <li>
            <a href="/index.html">Home</a>
          </li>
          <li>
            <a href="/about.html">About</a>
          </li>
        </ul>
      </nav>
    </header>
    <main>
      <p>Hi, thanks for stopping by!</p>
    </main>
    <footer>
      <p>
        <small>Copyright © cyberf1y 2022</small>
      </p>
    </footer>
  </body>
</html>
```

* *about.html*
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>site</title>
  </head>
  <body>
    <header>
      <nav>
        <ul>
          <li>
            <a href="/index.html">Home</a>
          </li>
          <li>
            <a href="/about.html">About</a>
          </li>
        </ul>
      </nav>
    </header>
    <main>
      <p>Hi, I am cyberf1y.</p>
    </main>
    <footer>
      <p>
        <small>Copyright © cyberf1y 2022</small>
      </p>
    </footer>
  </body>
</html>
```
