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

### Imports
The following syntax allows reusing parts of xml files:
```xml
<main import="path/to/file.xml" values="key1=value1;key2=value2">
  <div import-value="key1" />
  <div import-value="key2" />
</main>
```
Given *path/to/file.xml* with the following contents:
```xml
<main>
  <value1>text 1</value1>
  <value2>text 2</value2>
</main>
```
*lhtml* will produce:
```html
<main>
  <div>text 1</div>
  <div>text 2</div>
</main>
```

The values support *XPath* syntax, as described [here](https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support).

### Example:
Starting with the following files:
* [*template.xml*](example/template.xml):
```xml
<html lang="en">
  <head>
    <title>site</title>
  </head>
  <body>
    <header>
      <nav>
        <ul>
          <li><a href="/index.html">Home</a></li>
          <li><a href="/posts.html">Posts</a></li>
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
```xml
<main>
  <p>Hi, thanks for stopping by!</p>
</main>
```

* [*about.xml*](example/posts.xml):
```xml
<main import="posts/lorem-ipsum.xml" values="title=h2[1];content=p[2]">
  <h2>Posts</h2>
  <ul>
    <li>
      <a href="/posts/lorem-ipsum.html">
        <article>
          <h3 import-value="title" />
          <p import-value="content" />
        </article>
      </a>
    </li>
  </ul>
</main>
```

* [*posts/lorem-ipsum.xml*](example/posts/lorem-ipsum.xml):
```xml
<main>
  <h2>Lorem Ipsum</h2>
  <p>Laborum aut cumque dolorem corrupti consequatur amet nihil. Laboriosam dolore minima voluptatum sunt odit. Nulla delectus eum qui. Et voluptatem debitis atque voluptas et quia reiciendis.</p>
  <p>Quis ex cum fuga nesciunt laboriosam ut excepturi. Maxime aut molestias non repellat facilis debitis. In sit temporibus dolore eligendi in voluptatem odit omnis.</p>
  <p>Aliquid est dolore laudantium dolorem autem quae. In impedit rerum explicabo ipsam error sunt eum. Autem fuga voluptas est voluptates a repudiandae enim. Dolores aliquam vero ea odio et fugit minima. Est consequatur culpa iste ut minus tenetur possimus.</p>
  <p>Laudantium itaque in sunt iusto voluptas commodi. Qui officia distinctio exercitationem ipsa officiis. Ea asperiores autem ullam sunt odio soluta consequatur.</p>
  <p>Id iure est aut maxime nihil. Vero beatae qui fuga repellat iure praesentium autem eos. Pariatur ut asperiores reprehenderit repellendus. Quidem necessitatibus delectus est quibusdam ex quas qui. Quia officiis earum sapiente iste ut ut.</p>
</main>
```

*lhtml* will write the following:
* [*index.html*](example/index.html)
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
            <a href="/posts.html">Posts</a>
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

* [*posts.html*](example/posts.html)
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
            <a href="/posts.html">Posts</a>
          </li>
        </ul>
      </nav>
    </header>
    <main>
      <h2>Posts</h2>
      <ul>
        <li>
          <a href="/posts/lorem-ipsum.html">
            <article>
              <h3>Lorem Ipsum</h3>
              <p>Quis ex cum fuga nesciunt laboriosam ut excepturi. Maxime aut molestias non repellat facilis debitis. In sit temporibus dolore eligendi in voluptatem odit omnis.</p>
            </article>
          </a>
        </li>
      </ul>
    </main>
    <footer>
      <p>
        <small>Copyright © cyberf1y 2022</small>
      </p>
    </footer>
  </body>
</html>
```

* [*posts/lorem-ipsum.html*](example/posts/lorem-ipsum.html)
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
            <a href="/posts.html">Posts</a>
          </li>
        </ul>
      </nav>
    </header>
    <main>
      <h2>Lorem Ipsum</h2>
      <p>Laborum aut cumque dolorem corrupti consequatur amet nihil. Laboriosam dolore minima voluptatum sunt odit. Nulla delectus eum qui. Et voluptatem debitis atque voluptas et quia reiciendis.</p>
      <p>Quis ex cum fuga nesciunt laboriosam ut excepturi. Maxime aut molestias non repellat facilis debitis. In sit temporibus dolore eligendi in voluptatem odit omnis.</p>
      <p>Aliquid est dolore laudantium dolorem autem quae. In impedit rerum explicabo ipsam error sunt eum. Autem fuga voluptas est voluptates a repudiandae enim. Dolores aliquam vero ea odio et fugit minima. Est consequatur culpa iste ut minus tenetur possimus.</p>
      <p>Laudantium itaque in sunt iusto voluptas commodi. Qui officia distinctio exercitationem ipsa officiis. Ea asperiores autem ullam sunt odio soluta consequatur.</p>
      <p>Id iure est aut maxime nihil. Vero beatae qui fuga repellat iure praesentium autem eos. Pariatur ut asperiores reprehenderit repellendus. Quidem necessitatibus delectus est quibusdam ex quas qui. Quia officiis earum sapiente iste ut ut.</p>
    </main>
    <footer>
      <p>
        <small>Copyright © cyberf1y 2022</small>
      </p>
    </footer>
  </body>
</html>
```
