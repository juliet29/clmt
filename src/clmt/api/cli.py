from cyclopts import App
from pathlib import Path

from clmt.dataframes.interfaces import CarbonSummary
from clmt.extract.read_html import extract_data as extract_data_from_html
from clmt.extract.io import save_dataframe
from clmt.dataframes.process import (
    calculate_net_emissions,
    get_emissions_df,
)

app = App()


# @app.command
# def extract_data(path: Path):
#     # TODO convert to html if is .txt..
#     df = extract_data_from_html(path).pipe(get_emissions_df)
#     summary = calculate_net_emissions(df)
#     print(summary)  # TODO make a pretty print


DEFAULT_CSV_NAME = "pathfinder.csv"


@app.default
def extract_and_save_data(
    path_to_html: Path, save_directory: Path, save_name: str = DEFAULT_CSV_NAME
):
    # TODO convert to html if is .txt..
    df = extract_data_from_html(path_to_html).pipe(get_emissions_df)
    df = save_dataframe(save_directory, save_name, df)
    summary = calculate_net_emissions(df)  # TODO make a pretty print

    print(summary)

    # default behavior is to save where -> locally..


# open marimo with this path
# TODO one function that can take different flags -> save on default, make various graphs..


def main():
    app()


if __name__ == "__main__":
    main()
