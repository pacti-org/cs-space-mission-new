"""Helper module for the space mission case study."""
from pacti.terms.polyhedra import PolyhedralContract

from pacti import write_contracts_to_file, read_contracts_from_file
from typing import Optional, List, Tuple, Union
from functools import reduce
import numpy as np
import itertools
import json
import pathlib


tuple2float = Tuple[float, float]

here = pathlib.Path(__file__).parent.resolve()

epsilon = 0

class Schedule:
    def __init__(self, scenario: List[tuple2float], reqs: np.ndarray, contract: PolyhedralContract):
        self.scenario = scenario
        self.reqs = reqs
        self.contract = contract


numeric = Union[int, float]

tuple2 = Tuple[Optional[numeric], Optional[numeric]]

tuple2float = Tuple[float, float]

def check_tuple(t: tuple2) -> tuple2float:
    if t[0] is None:
        a = -1.0
    else:
        a = t[0]
    if t[1] is None:
        b = -1.0
    else:
        b = t[1]
    return (a, b)


def nochange_contract(s: int, name: str) -> PolyhedralContract:
    """
    Constructs a no-change contract between entry/exit variables derived from the name and step index.

    Args:
        s: step index
        name: name of the variable

    Returns:
        A no-change contract.
    """
    return PolyhedralContract.from_string(
        input_vars=[f"{name}{s}_entry"],
        output_vars=[f"{name}{s}_exit"],
        assumptions=[
            f"-{name}{s}_entry <= 0",
        ],
        guarantees=[
            # f"-{name}{s}_exit <= 0",
            f"| {name}{s}_exit - {name}{s}_entry | <= 0",
            # f"{name}{s}_exit <= 100",
        ],
    )


def scenario_sequence(
    c1: PolyhedralContract,
    c2: PolyhedralContract,
    variables: list[str],
    c1index: int,
    c2index: Optional[int] = None,
    file_name: Optional[str] = None,
) -> PolyhedralContract:
    """
    Composes c1 with a c2 modified to rename its entry variables according to c1's exit variables

    Args:
        c1: preceding step in the scenario sequence
        c2: next step in the scenario sequence
        variables: list of entry/exit variable names for renaming
        c1index: the step number for c1's variable names
        c2index: the step number for c2's variable names; defaults ti c1index+1 if unspecified

    Returns:
        c1 composed with a c2 modified to rename its c2index-entry variables
        to c1index-exit variables according to the variable name correspondences
        with a post-composition renaming of c1's exit variables to fresh outputs
        according to the variable names.
    """
    if not c2index:
        c2index = c1index + 1
    c2_inputs_to_c1_outputs = [(f"{v}{c2index}_entry", f"{v}{c1index}_exit") for v in variables]
    keep_c1_outputs = [f"{v}{c1index}_exit" for v in variables]
    renamed_c1_outputs = [(f"{v}{c1index}_exit", f"output_{v}{c1index}") for v in variables]

    c2_with_inputs_renamed = c2.rename_variables(c2_inputs_to_c1_outputs)
    # try:
    c12_with_outputs_kept = c1.compose(c2_with_inputs_renamed, vars_to_keep=keep_c1_outputs)
    # except ValueError:
    #     print(keep_c1_outputs)
    #     example=f"{here}/json/example-{uuid.uuid4()}.json"
    #     write_contracts_to_file([c1,c2_with_inputs_renamed],["c1","c2"], example, machine_representation=True)
    #     conts,_ = read_contracts_from_file(example)
    #     print("**********************")
    #     print(c1)
    #     print("**********************")
    #     print(conts[0])
    #     assert c1 == conts[0]
    #     assert c2_with_inputs_renamed == conts[1]
    #     print("Exiting on error")
    #     raise ValueError()

    c12 = c12_with_outputs_kept.rename_variables(renamed_c1_outputs)

    if file_name:
        write_contracts_to_file(
            contracts=[c1, c2_with_inputs_renamed, c12_with_outputs_kept],
            names=["c1", "c2_with_inputs_renamed", "c12_with_outputs_kept"],
            file_name=file_name)

    return c12


named_contract_t = Tuple[str, PolyhedralContract]

named_contracts_t = list[named_contract_t]

contract_names_t = list[str]

failed_merges_t = Tuple[contract_names_t, str, PolyhedralContract]

merge_result_t = Union[list[failed_merges_t], PolyhedralContract]

merge_results_t = Tuple[list[failed_merges_t], list[PolyhedralContract]]

schedule_result_t = Union[list[failed_merges_t], Schedule]
schedule_results_t = Tuple[list[failed_merges_t], list[Schedule]]


def try_merge_sequence(c: PolyhedralContract, c_seq: named_contracts_t) -> merge_result_t:
    names: contract_names_t = []
    current: PolyhedralContract = c
    for cn, cc in c_seq:
        try:
            current = current.merge(cc)
            names.append(cn)
        except ValueError:
            return [(names, cn, cc)]
    return current

# maximum number of failures.
max_failures = 1

def perform_merges_seq(c: PolyhedralContract, candidates: named_contracts_t) -> merge_result_t:
    failures: list[failed_merges_t] = []
    for c_seq in itertools.permutations(candidates):
        cl = list(c_seq)
        r = try_merge_sequence(c, cl)
        if isinstance(r, PolyhedralContract):
            return r
        elif isinstance(r, list):
            failures.append(r)
            if len(failures) >= max_failures:
                return failures
        else:
            raise ValueError(f"{type(r)} should be a merge_result_t")

    return failures

with open(f"{here}/images.json") as f:
    file_data = json.load(f)

figure_space_mission_scenario = file_data["figure_space_mission_scenario"]
figure_space_mission_segments = file_data["figure_space_mission_segments"]
figure_task_schedule_contracts = file_data["figure_task_schedule_contracts"]
pacti_interactive_scenario_plot_concept = file_data["pacti_interactive_scenario_plot_concept"]
