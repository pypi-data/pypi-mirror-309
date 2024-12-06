## wikixml
A Python Library to process wiki dumps xml.

![](https://img.shields.io/pypi/v/wikixml?label=wikixml&color=blue&cacheSeconds=60)

## Install

```sh
pip install wikixml --upgrade
```

## Usage

Run example:

```sh
python example.py
```

See: [example.py](https://github.com/Hansimov/wikixml/blob/main/example.py)

```python
from wikixml import ZhWikiBz2Parser

if __name__ == "__main__":
    wiki_xml_bz2 = "zhwiki-20241101-pages-meta-current.xml.bz2"
    file_path = Path(__file__).parent / "data" / wiki_xml_bz2
    parser = ZhWikiBz2Parser(file_path)
    parser.preview_lines(100)
    # parser.preview_pages(max_pages=10000)
```