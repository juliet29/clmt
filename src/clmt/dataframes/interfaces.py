import math
from typing import NamedTuple


class CarbonSummary(NamedTuple):
    emissions: float
    biogenic: float

    def __eq__(self, other: object) -> bool:
        def compare(other):
            REL_TOL = 1e-4
            return math.isclose(
                self.emissions, other.emissions, rel_tol=REL_TOL
            ) and math.isclose(self.biogenic, other.biogenic, rel_tol=REL_TOL)

        if isinstance(other, CarbonSummary):
            result = compare(other)
            if not result:
                return compare(CarbonSummary(other.emissions, -1 * other.biogenic))
            return result
        raise TypeError(f"{object} is not a CarbonSummary!")

    @property
    def total(self):
        return self.emissions + self.biogenic
