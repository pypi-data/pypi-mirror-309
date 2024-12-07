## wikixml
A Python Library to process wiki dumps xml.

![](https://img.shields.io/pypi/v/wikixml?label=wikixml&color=blue&cacheSeconds=60)

## Install

```sh
pip install wikixml --upgrade
```

## Usage

### `WikiXmlParser`

Run example:

```sh
python example.py
```

See: [example.py](https://github.com/Hansimov/wikixml/blob/main/example.py)

```python
from wikixml import WikiXmlParser

if __name__ == "__main__":
    wiki_xml_bz2 = "zhwiki-20241101-pages-meta-current.xml.bz2"
    file_path = Path(__file__).parent / "data" / wiki_xml_bz2
    parser = WikiXmlParser(file_path)
    # parser.preview_lines(5000)
    parser.preview_pages(max_pages=100)
```

### `WikiPagesMongoWriter`

Extract wiki pages from XML and write to MongoDB

```sh
python -m wikixml.mongo -d zhwiki -f "../data/zhwiki-latest-pages-meta-current.xml.bz2"
```