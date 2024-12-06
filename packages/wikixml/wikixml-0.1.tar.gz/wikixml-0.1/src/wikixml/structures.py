from lxml import etree, objectify
from copy import deepcopy


class ElementCleaner:
    def remove_namespaces(self, element: etree._Element) -> etree._Element:
        for ele in element.getiterator():
            ele.tag = etree.QName(ele).localname
        return element

    def remove_annotations(self, element: etree._Element) -> etree._Element:
        objectify.deannotate(element, cleanup_namespaces=True)
        return element

    def clean(self, element: etree._Element) -> etree._Element:
        element = self.remove_namespaces(element)
        element = self.remove_annotations(element)
        return element


class ElementToDictConverter:
    def __init__(self):
        self.cleaner = ElementCleaner()

    def to_dict(self, element: etree._Element) -> dict:
        res = {}
        if len(element) == 0:
            return element.text
        for child in element:
            res[child.tag] = self.convert(child)
        return res

    def convert(self, element: etree._Element, use_root_tag: bool = False) -> dict:
        e = deepcopy(element)
        e = self.cleaner.clean(e)
        res = self.to_dict(e)
        if use_root_tag:
            res = {e.tag: res}
        return res
