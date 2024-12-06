import bz2

from pathlib import Path
from tclogger import logger, TCLogbar, chars_slice
from typing import Union
from xml.etree.ElementTree import iterparse


class ZhWikiBz2Parser:
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path
        self.xmlns = "http://www.mediawiki.org/xml/export-0.11/"
        self.logbar = TCLogbar()

    def preview_lines(self, max_lines: int = 10):
        with bz2.BZ2File(self.file_path, "rb") as rf:
            for idx, line in enumerate(rf):
                line_str = line.decode("utf-8").rstrip()
                logger.file(line_str)
                if idx >= max_lines:
                    break

    def preview_pages(self, max_pages: int = None):
        with bz2.BZ2File(self.file_path, "rb") as rf:
            context = iterparse(rf, events=("start", "end"))
            _, root = next(context)
            page_count = 0
            for idx, (event, element) in enumerate(context):
                if event == "end" and element.tag == f"{{{self.xmlns}}}page":
                    title = element.findtext(f"{{{self.xmlns}}}title")
                    text = element.findtext(
                        f"{{{self.xmlns}}}revision/{{{self.xmlns}}}text"
                    )
                    title_part = chars_slice(title, end=20)
                    if title:
                        self.logbar.update(increment=1, desc=title_part)
                    page_count += 1
                    if max_pages is not None and page_count >= max_pages:
                        break
                if idx % 10000 == 0:
                    root.clear()
            title_part = chars_slice(title, end=20)
            self.logbar.update(flush=True, desc=title_part)
