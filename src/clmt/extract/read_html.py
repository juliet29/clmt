from bs4 import BeautifulSoup
from bs4.filter import SoupStrainer
from bs4.element import Tag
from clmt.extract.helpers import (
    ValueAndUnit,
    create_list_of_class_type,
    get_element_name,
    get_element_value,
    is_element_row,
)
from typing import IO, TypeAlias, Union

# from clmt.extract.project_paths import SAMPLE_CLMT_BREAKDOWN_HTML
from clmt.extract.constants import ClassNames
from pathlib import Path
import polars as pl

from collections import Counter

# just read main
MAIN_WRAPPER = "main-wrapper"
SCORECARD = "score-card"


IncomingMarkup: TypeAlias = Union[str, bytes, IO[str], IO[bytes]]


def get_soup(markup: IncomingMarkup):
    return BeautifulSoup(
        markup,
        features="html.parser",
        # features="html5lib",
        from_encoding="utf-8",
        parse_only=SoupStrainer(class_=SCORECARD),
    )


def get_rows_from_path(path: Path):
    assert path.exists(), f"{path} is invalid!"
    with open(path, "r") as file:
        soup = get_soup(file)

    all_rows = [i for i in soup.find_all("tr") if isinstance(i, Tag)]

    if not all_rows:
        raise Exception(
            f"Invalid file! `{path}` does not have a top-level class of `{SCORECARD}`: all_rows: {all_rows}"
        )

    return all_rows




# TODO seems like should be a class.. 
def extract_data(path: Path) -> pl.DataFrame:
    all_rows = get_rows_from_path(path)

    category_counter = Counter()
    elements = []
    values: list[ValueAndUnit] = []

    type_counter = Counter()
    section_counter = Counter()

    curr_category = ""
    curr_section = ""
    curr_type = ""

    for row in all_rows:
        # type_counter = Counter()
        curr_section = create_list_of_class_type(
            ClassNames.SECTION, row, curr_section
        )  # TODO rename function ..  # TODO put in its own loop? break out to different function..
        curr_type = create_list_of_class_type(ClassNames.TYPE, row, curr_type)
        curr_category = create_list_of_class_type(
            ClassNames.CATEGORY, row, curr_category
        )

        if curr_category:
            # only update when we get to the category level
            if is_element_row(row):
                elements.append(get_element_name(row))
                values.append(get_element_value(row))

                category_counter[curr_category] += 1
                section_counter[curr_section] += 1
                type_counter[curr_type] += 1

    assert (
        section_counter.total()
        == type_counter.total()
        == category_counter.total()
        == len(elements)
    )
 

    data = {
        # TODO: swicth class names to a regular class
        ClassNames.SECTION.name: section_counter.elements(),
        ClassNames.TYPE.name: type_counter.elements(),
        ClassNames.CATEGORY.name: category_counter.elements(),
        ClassNames.ELEMENT.name: elements,
        ClassNames.VALUE.name: [i.value for i in values],
        ClassNames.UNIT.name: [i.unit for i in values],
    }
    return pl.DataFrame(data)
    # TODO maybe validate this here also.. 