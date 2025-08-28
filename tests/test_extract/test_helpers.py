from bs4 import BeautifulSoup
from bs4.element import Tag
from clmt.extract.helpers import is_element_row, is_header_of_class_type
from clmt.extract.constants import ClassNames

def test_is_category_header():
    tag = """
        <tr class="category-header">
            <td colspan="2">Aggregate Asphalt Hardscape</td>
        </tr>
        """
    soup = BeautifulSoup(tag, features="html.parser")
    tr = soup.find("tr")
    assert isinstance(tr, Tag)
    result = is_header_of_class_type(tr, ClassNames.CATEGORY)
    assert result


def test_is_element_row():
    tag = """ 
        <tr class>
            <td class="element-name">Brick Paving</td>
            <td class="element-co2 neutral ">
                <span>0 kgCO₂e</span>
            </td>
        </tr>
    """
    soup = BeautifulSoup(tag, features="html.parser")
    tr = soup.find("tr")
    assert isinstance(tr, Tag)
    result = is_element_row(tr)
    assert result


# TESTS 
def test_can_get_soup_from_path():
    pass