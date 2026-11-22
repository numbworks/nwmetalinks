# nwmetalinks
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2026-11-22 | numbworks | Created. |
| 2026-11-22 | numbworks | Last updated (v1.0.0). |

## Introduction

`nwmetalinks` is a library that creates MetaLink v4 strings from user-provided URLs and their corresponding filenames for delegating downloads to external applications such as JDownloader.

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

## See Also: `developerguide`

To get started with this project as a developer, please give a look to the following document:

- [docs-developerguide-python.md](SeeAlso-developerguide/docs-developerguide-python.md)

## See Also: `frameworkfreeze`

To learn more about the "framework freeze" strategy adopted by this project, please have a look at the following document:

- [docs-frameworkfreeze-python.md](SeeAlso-frameworkfreeze/docs-frameworkfreeze-python.md)

## See Also: `knownissues`

To learn more about some known issues that might have required a workaround to make this project work, please have a look at the following document:

- [docs-knownissues-python.md](SeeAlso-knownissues/docs-knownissues-python.md)

## See Also: `nwmakefiles`

This project includes portions of the `nwmakefiles` project, which is documented here:

- [docs-nwmakefiles.md](SeeAlso-nwmakefiles/docs-nwmakefiles.md)

## See Also: `nwpublishers`

To know more about the package publishing logic, please give a look to the following document:

- [docs-nwpublishers-python.md](SeeAlso-nwpublishers/docs-nwpublishers-python.md)

## See Also: `userguide`

To get started with this project as a user, please give a look to the following document:

- [docs-userguide-python.md](SeeAlso-userguide/docs-userguide-python.md)

## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)