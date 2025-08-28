import dataframely as dy
from dataframely.exc import ValidationError
import polars as pl
from enum import StrEnum

from clmt.dataframes.interfaces import CarbonSummary
# import pandera.polars as pa
# import pandas as pd

# from clmt.extract.constants import ClassNames


class SectionNames(StrEnum):
    CARBON_IMPACT = "Carbon Impact"


class TypeNames:
    EMBODIED_CARBON_EMISSIONS = "Embodied Carbon Emissions"
    BIOGENIC = "Biogenic (Sequestration + Emissions)"
    OPERATIONAL = "Operational Emissions"


# TODO: polars enum??


class JustExtractSchema(dy.Schema):
    SECTION = dy.String(nullable=False)
    TYPE = dy.String(nullable=False)
    CATEGORY = dy.String(nullable=False)
    ELEMENT = dy.String(nullable=False)
    VALUE = dy.Int64(nullable=False)
    UNIT = dy.String(nullable=False)

    VALUE_ALT = "VALUE_ALT"



def get_emissions_df(_df: pl.DataFrame):
    df = JustExtractSchema.validate(_df)

    d = df.filter(pl.col(JustExtractSchema.VALUE.name) != 0).filter(
        pl.col(JustExtractSchema.SECTION.name) == SectionNames.CARBON_IMPACT.value
    )

    # NOTE: sometimes
    # there are duplicate elements in pathfinder, do a groupby early on
    grouped = d.group_by(pl.col(JustExtractSchema.ELEMENT.name)).agg(
        pl.col(JustExtractSchema.VALUE.name).sum(),
    )
    d2 = (
        d.join(
            grouped,
            on=[JustExtractSchema.ELEMENT.name],
            suffix="_ALT",
        )
        .unique(subset=[JustExtractSchema.ELEMENT.name, JustExtractSchema.VALUE_ALT])
        .drop(JustExtractSchema.VALUE.name)
        .rename({JustExtractSchema.VALUE_ALT: JustExtractSchema.VALUE.name})
    )
    return d2




def calculate_net_emissions(_df: pl.DataFrame):
    df = JustExtractSchema.validate(_df)
    agg = (
        df.group_by(JustExtractSchema.TYPE.name)
        .agg(pl.sum(JustExtractSchema.VALUE.name))
        .rows()
    )
    agg_dict = {k: v for k, v in agg}

    summary = CarbonSummary(
        emissions=agg_dict[TypeNames.EMBODIED_CARBON_EMISSIONS],
        biogenic=agg_dict[TypeNames.BIOGENIC],
    )
    return summary


# def mac(a, b):
#     return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
