from pathlib import Path

import petab.v1 as petab
from more_itertools import one
from petab.v1.C import ESTIMATE, NOMINAL_VALUE

from .constants import PETAB_ESTIMATE_FALSE, TYPE_PARAMETER_DICT, TYPE_PATH


class PetabMixin:
    """Useful things for classes that contain a PEtab problem.

    All attributes/methods are prefixed with `petab_`.

    Attributes:
        petab_yaml:
            The location of the PEtab problem YAML file.
        petab_problem:
            The PEtab problem.
        petab_parameters:
            The parameters from the PEtab parameters table, where keys are
            parameter IDs, and values are either :obj:`ESTIMATE` if the
            parameter is set to be estimated, else the nominal value.
    """

    def __init__(
        self,
        petab_yaml: TYPE_PATH | None = None,
        petab_problem: petab.Problem | None = None,
        parameters_as_lists: bool = False,
    ):
        if petab_yaml is None and petab_problem is None:
            raise ValueError(
                "Please supply at least one of either the location of the "
                "PEtab problem YAML file, or an instance of the PEtab problem."
            )
        self.petab_yaml = petab_yaml
        if self.petab_yaml is not None:
            self.petab_yaml = Path(self.petab_yaml)

        self.petab_problem = petab_problem
        if self.petab_problem is None:
            self.petab_problem = petab.Problem.from_yaml(str(petab_yaml))

        self.petab_parameters = {
            parameter_id: (
                row[NOMINAL_VALUE]
                if row[ESTIMATE] == PETAB_ESTIMATE_FALSE
                else ESTIMATE
            )
            for parameter_id, row in self.petab_problem.parameter_df.iterrows()
        }
        if parameters_as_lists:
            self.petab_parameters = {
                k: [v] for k, v in self.petab_parameters.items()
            }

    @property
    def petab_parameter_ids_estimated(self) -> list[str]:
        """Get the IDs of all estimated parameters.

        Returns:
            The parameter IDs.
        """
        return [
            parameter_id
            for parameter_id, parameter_value in self.petab_parameters.items()
            if parameter_value == ESTIMATE
        ]

    @property
    def petab_parameter_ids_fixed(self) -> list[str]:
        """Get the IDs of all fixed parameters.

        Returns:
            The parameter IDs.
        """
        estimated = self.petab_parameter_ids_estimated
        return [
            parameter_id
            for parameter_id in self.petab_parameters
            if parameter_id not in estimated
        ]

    @property
    def petab_parameters_singular(self) -> TYPE_PARAMETER_DICT:
        """TODO deprecate and remove?"""
        return {
            parameter_id: one(parameter_value)
            for parameter_id, parameter_value in self.petab_parameters
        }
