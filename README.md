Simple Tornado Web Server
=========================

Serves semi-static pages from a Redis cache.
The simple use case involves serving a directory of HTML, Markdown, images, CSS, JavaScript, Text, Manifests, XML etc.

Text files can have [[YAML Front Matter]] to change the default page serving rules.

* document, the name of the parts page file to combine with the source file.

### Version 0.3

* Switched to Beautiful Soup 4
* Switched to html5lib for parsing
* Supporting output to filesystem
* JavaScript Libs with version awareness
