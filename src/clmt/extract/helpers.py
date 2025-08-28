from typing import NamedTuple
from bs4.element import Tag
import re
# from rich import print as rprint
from clmt.extract.constants import ClassNames
# import numpy as np


class ValueAndUnit(NamedTuple):
    value: int
    unit: str


def is_element_row(tag: Tag):
    if tag.has_attr("class"):
        if len(tag["class"]) == 0:
            return True


def get_element_name(tag: Tag):
    td = tag.find("td", class_=ClassNames.ELEMENT.value)
    assert isinstance(td, Tag)
    return re.sub(" +", " ", td.get_text(strip=True)).replace("\n", "")




def get_element_value(tag: Tag):
    td = tag.find("td", class_=ClassNames.VALUE.value)
    assert isinstance(td, Tag)

    result = td.get_text("|", strip=True).split(" ")
    if len(result) == 2:
        integer_value = int(result[0].replace(",", ""))
        if ClassNames.SEQUESTERING.value in td["class"]:
            integer_value *= -1
        return ValueAndUnit(integer_value, result[1])
    if len(result) == 1:
        return ValueAndUnit(0, "")
    else:
        raise NotImplementedError(
            f"Invalid result: `{result}` - should have len 1 or 2, but has len {len(result)}"
        )


def is_header_of_class_type(tag: Tag, class_: ClassNames):
    if tag.has_attr("class"):
        if class_.value in tag["class"]:
            return True


def get_header_name(tag: Tag):
    assert tag.td
    return tag.td.get_text(strip=True)


def create_list_of_class_type(_class: ClassNames, row: Tag, curr_value=""):
    if is_header_of_class_type(row, _class):
        curr_value = get_header_name(row)
    return curr_value