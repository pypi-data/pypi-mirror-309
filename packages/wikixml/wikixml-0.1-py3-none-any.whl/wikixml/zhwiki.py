import bz2

from lxml import etree
from pathlib import Path
from tclogger import logger, logstr, TCLogbar
from tclogger import dict_to_str, dict_get, chars_len, chars_slice, brk
from typing import Union

from .structures import ElementToDictConverter


class ZhWikiBz2Parser:
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
