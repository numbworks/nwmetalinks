# nwmetalinks

## Introduction

This packages consists of the following modules:

- `nwmetalinks` is a library that creates MetaLink v4 strings from user-provided URLs and their corresponding filenames.

## Getting Started

I'll use Debian as operating system, but the concept is similar for Windows or Mac.

Procedure:

1. Install `pip` and `venv`:

```sh
sudo apt install python3-pip python3.12-venv
```

2. Create a virtual environment:

```sh
python3 -m venv /tmp/nwmetalinks
source /tmp/nwmetalinks/bin/activate
```

3. Download and install the package:

```sh
pip install nwmetalinks
```

4. Enter in the interactive Python environment:

```sh
python3
```
```
Python 3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

5. Try out if the library works:

```python
from nwmetalinks import MetaLinkFactory

metalink_factory : MetaLinkFactory = MetaLinkFactory()
```

6. Exit from the interactive Python environment:

```python
exit()
```

7. Deactivate and delete the virtual environment:

```sh
deactivate
rm -rf /tmp/nwmetalinks
```

8. Done!

## The Typical Use Case

In order to use the library, the first thing we need to do is to create a list of download URLs and a list containing their corresponding filenames, and then pass them to the `CreateMetaLink4` method of a `MetaLinkFactory` object, as shown in the following example:

```python
from nwmetalinks import MetaLinkFactory

package_name : str = "nwmetalinks"
tuples : list[tuple[str, str]] = [
    ("https://numbworks.github.io/nwmetalinks.zip", "nwmetalinks.zip"),
    ("https://numbworks.github.io/nwmetalinks.tar.gz", "NW.nwmetalinks.tar.gz")
]

metalink : str = MetaLinkFactory().create_metalink4("nwmetalinks", tuples)

with open("nwmetalinks.metalink", "w", encoding="utf-8") as f:
    f.write(metalink)
```

## MetaLink v4

Here is a minimal example of a MetaLink v4 file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metalink xmlns="urn:ietf:params:xml:ns:metalink" version="4.0">
  <identity>My Package Name</identity>

  <file name="example.bin">
    <url>https://example.com/example.bin</url>
  </file>
</metalink>
```

Even if it's a XML file under the hood, a MetaLink file is expected to have the `.metalink` extension (instead of `.xml`).

## MetaLink v4 and JDownloader

JDownloader has full support for the MetaLink v4 format, but it's worth mentioning that by default, once the user imports a MetaLink file, JDownloader will ping all the files inside it, to check for their online status. 

When importing a MetaLink file with hundreds or thousands of links inside, could flood the website and bring the provider to blacklist your IP address.

Before importing a MetaLink file, it could be a good practice to disable the `Do Link Check` feature:

1. Open JDownloader 2.
2. Go to `Settings` -> `Advanced Settings`.
3. Locate the setting: `LinkCollector: Do Link Check`
4. Untick (disable) this option.
4. Done!

## Links

- Source: https://github.com/numbworks/nwmetalinks
- License: https://github.com/numbworks/nwmetalinks/blob/master/LICENSE

## Total Downloads (PyPi)

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/nwmetalinks?period=total&units=NONE&left_color=BLACK&right_color=BLUE&left_text=TOTAL+DOWNLOADS)](https://pepy.tech/projects/nwmetalinks)