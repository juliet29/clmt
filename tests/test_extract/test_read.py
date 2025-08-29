from clmt.dataframes.interfaces import CarbonSummary
from clmt.examples import SampleData
from clmt.extract.read_html import extract_data
from clmt.dataframes.process import (
    calculate_net_emissions,
    get_emissions_df,
)


def test_getting_a_valid_df():
    df = extract_data(path=SampleData.SAMPLE_HTML)
    assert not df.is_empty()


def test_extracted_data_is_correct():
    df = extract_data(path=SampleData.SAMPLE_HTML).pipe(get_emissions_df)
    expected_summary = CarbonSummary(
        emissions=SampleData.TOTAL_EMBODIED_EMISSIONS,
        biogenic=SampleData.TOTAL_BIOGENIC,
    )
    summary = calculate_net_emissions(df)
    assert summary == expected_summary


if __name__ == "__main__":
    test_extracted_data_is_correct()
    # df = extract_data(path=Pier6Data.SAMPLE_HTML)
    # d = get_emissions_df(df)
    # e = calculate_net_emissions(d)
    # print(d)
    # print(e)
