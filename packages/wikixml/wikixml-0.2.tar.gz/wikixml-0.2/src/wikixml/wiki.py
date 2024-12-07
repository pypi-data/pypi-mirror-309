import bz2

from lxml import etree
from pathlib import Path
from tclogger import logger, logstr, TCLogbar
from tclogger import dict_to_str, dict_get, chars_len, chars_slice, brk
from typing import Union, Generator

from .structures import ElementToDictConverter


class WikiXmlParser:
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path
        self.xmlns = "{http://www.mediawiki.org/xml/export-0.11/}"
        self.logbar = TCLogbar()
        self.converter = ElementToDictConverter()

    def preview_lines(self, max_lines: int = 10):
        with bz2.BZ2File(self.file_path, "rb") as rf:
            for idx, line in enumerate(rf):
                line_str = line.decode("utf-8").rstrip()
                logger.file(line_str)
                if idx >= max_lines:
                    break

    def preview_pages(self, max_pages: int = None):
        with bz2.BZ2File(self.file_path, "rb") as rf:
            context = etree.iterparse(rf, tag=self.xmlns + "page")
            for idx, (_, element) in enumerate(context):
                if max_pages and idx >= max_pages:
                    break
                page_dict = self.converter.convert(element)
                # logger.mesg(dict_to_str(page_dict))
                title = dict_get(page_dict, "title")
                title_part = chars_slice(title, 0, 20)
                text = dict_get(page_dict, "revision.text")
                text_len = chars_len(text)
                logger.note(f"* {title_part} : {logstr.mesg(brk(text_len))}")


class WikiPagesIterater:
    def __init__(self, file_path: Union[str, Path], max_pages: int = None):
        self.file_path = file_path
        self.max_pages = max_pages
        self.xmlns = "{http://www.mediawiki.org/xml/export-0.11/}"
        self.logbar = TCLogbar()
        self.converter = ElementToDictConverter()

    def update_logbar(self, doc: dict):
        title = dict_get(doc, "title")
        title_part = chars_slice(title, 0, 20)
        text = dict_get(doc, "revision.text")
        text_len = chars_len(text)
        text_len_str = brk(f"{text_len:>8}")
        desc = f"* {title_part} : {logstr.mesg(text_len_str)}"
        self.logbar.update(increment=1, desc=desc)

    def count_pages(self) -> int:
        count_bar = TCLogbar()
        count_bar.desc = logstr.note("> Counting pages")
        with bz2.BZ2File(self.file_path, "rb") as rf:
            context = etree.iterparse(rf, tag=self.xmlns + "page", events=("end",))
            for idx, (_, element) in enumerate(context):
                count_bar.update(increment=1)
                element.clear()
            del context
        self.logbar.total = count_bar.count
        return count_bar.count

    def __iter__(self) -> Generator[dict, None, None]:
        if self.max_pages:
            self.logbar.total = self.max_pages
        with bz2.BZ2File(self.file_path, "rb") as rf:
            context = etree.iterparse(rf, tag=self.xmlns + "page")
            for idx, (_, element) in enumerate(context):
                if self.max_pages and idx >= self.max_pages:
                    break
                page_dict = self.converter.convert(element)
                self.update_logbar(page_dict)
                yield page_dict
