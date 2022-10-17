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

### Titles
*lhtml* can prefix the `<title>` of a page with `Subtitle |`, if the imported
file has an attribute `title`.
#### Example:
Given the following:
* *about.xml*
```xml
<main title="About"></main>
```
* *template.xml*
```xml
<html lang="en">
  <head>
    <title>cyberf1y</title>
  </head>
  <nav><a href="/about.hml">About</a></nav>
  <body>
    <main />
  </body>
</html>
```
*lhtml* will set the title in *about.html* like this:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>About | cyberf1y</title>
  </head>
  <nav><a href="/about.hml">About</a></nav>
  <body>
    <main></main>
  </body>
</html>
```

### Imports
*lhtml* supports importing content from one xml file, into another, using the
*XPath* syntax, as described [here](
https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support).

#### Example:
Given the following:
* [*posts.xml*](example/posts.xml)
```xml
<main title="Posts">
  <h2 title-value="true" />
  <ul>
    <li>
      <a href="/posts/lorem.html">
        <article
           import="posts/lorem.xml" values="title=h2[1];content=p[1]">
          <h3 import-value="title" />
          <p import-value="content" />
        </article>
      </a>
      <a href="/posts/ipsum.html">
        <article
           import="posts/ipsum.xml" values="title=h2[1];content=p[1]">
          <h3 import-value="title" />
          <p import-value="content" />
        </article>
      </a>
    </li>
  </ul>
</main>
```
* [*lorem.xml*](example/posts/lorem.xml)
```xml
<main title="Lorem">
  <h2 title-value="true" />
  <p>Laborum aut cumque dolorem corrupti consequatur amet nihil. Laboriosam
    dolore minima voluptatum sunt odit. Nulla delectus eum qui. Et voluptatem
    debitis atque voluptas et quia reiciendis.</p>
  <p>Quis ex cum fuga nesciunt laboriosam ut excepturi. Maxime aut molestias non
    repellat facilis debitis. In sit temporibus dolore eligendi in voluptatem
    odit omnis.</p>
  <p>Aliquid est dolore laudantium dolorem autem quae. In impedit rerum
    explicabo ipsam error sunt eum. Autem fuga voluptas est voluptates a
    repudiandae enim. Dolores aliquam vero ea odio et fugit minima. Est
    consequatur culpa iste ut minus tenetur possimus.</p>
</main>
```
* [*ipsum.xml*](example/posts/ipsum.xml)
```xml
<main title="Ipsum">
  <h2 title-value="true" />
  <p>Laudantium itaque in sunt iusto voluptas commodi. Qui officia distinctio
    exercitationem ipsa officiis. Ea asperiores autem ullam sunt odio soluta
    consequatur.</p>
  <p>Id iure est aut maxime nihil. Vero beatae qui fuga repellat iure
    praesentium autem eos. Pariatur ut asperiores reprehenderit repellendus.
    Quidem necessitatibus delectus est quibusdam ex quas qui. Quia officiis
    earum sapiente iste ut ut.</p>
</main>
```
*lhtml* will produce the following part of [*posts.html*](example/posts.html):
```html
<main>
  <h2>Posts</h2>
  <ul>
    <li>
      <a href="/posts/lorem.html">
        <article>
          <h3>Lorem</h3>
          <p>Laborum aut cumque dolorem corrupti consequatur amet nihil. Laboriosam
    dolore minima voluptatum sunt odit. Nulla delectus eum qui. Et voluptatem
    debitis atque voluptas et quia reiciendis.</p>
        </article>
      </a>
      <a href="/posts/ipsum.html">
        <article>
          <h3>Ipsum</h3>
          <p>Laudantium itaque in sunt iusto voluptas commodi. Qui officia distinctio
    exercitationem ipsa officiis. Ea asperiores autem ullam sunt odio soluta
    consequatur.</p>
        </article>
      </a>
    </li>
  </ul>
</main>
```

#### Note
You can reproduce the example by running the commands:
```sh
cd example
py ../lhtml.py
```
