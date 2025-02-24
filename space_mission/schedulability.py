from pacti.contracts import PolyhedralIoContract
from pacti_instrumentation.pacti_counters import PactiInstrumentationData
import functools
import numpy as np
from contract_utils import *
from generators import *
from typing import Tuple


def make_op_requirement_constraints5(reqs: np.ndarray) -> named_contracts_t:
    cs1: named_contracts_t = [
        (
            "durations",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[var],
                        output_vars=[], 
                        assumptions=[f"{var} >= {reqs[2]}"], 
                        guarantees=[]
                    )
                    for var in [
                        "duration_dsn1",
                        "duration_charging2",
                        "duration_sbo3",
                        "duration_tcm_h4",
                        "duration_tcm_dv5",
                    ]
                ],
            ),
        )
    ]
    cs2: named_contracts_t = [
        (
            "initial",
            PolyhedralIoContract.from_strings(
                input_vars=["soc1_entry", "c1_entry", "d1_entry", "u1_entry", "r1_entry"],
                output_vars=[],
                assumptions=[
                    f"soc1_entry = {reqs[0]}",
                    f"c1_entry = 0",
                    f"d1_entry = {reqs[3]}",
                    f"u1_entry = {reqs[4]}",
                    f"r1_entry = {reqs[5]}",
                ],
                guarantees=[],
            ),
        )
    ]
    cs3: named_contracts_t = [
        (
            "output_soc",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"output_soc{i} >= {reqs[1]}"],
                    )
                    for i in range(1, 6)
                ],
            ),
        )
    ]
    return cs1 + cs2 + cs3


def schedulability_analysis5(
    scenario_reqs: Tuple[Tuple[list[tuple2float], PolyhedralIoContract], np.ndarray]
) -> Tuple[PactiInstrumentationData, schedule_result_t]:
    scenario = scenario_reqs[0]
    reqs = scenario_reqs[1]
    op_reqs: named_contracts_t = make_op_requirement_constraints5(reqs)
    result: merge_result_t = perform_merges_seq(scenario[1], op_reqs)
    if isinstance(result, PolyhedralIoContract):
        return PactiInstrumentationData().update_counts(), Schedule(scenario=scenario[0], reqs=reqs, contract=result)
    return PactiInstrumentationData().update_counts(), result

def schedulability_analysis5_grouped(samples_group: Tuple[Tuple[Tuple[list[tuple2float], PolyhedralIoContract], np.ndarray], ...]) -> List[Tuple[PactiInstrumentationData, schedule_result_t]]:
    return [schedulability_analysis5(sample) for sample in samples_group]

def make_op_requirement_constraints20(reqs: np.ndarray) -> named_contracts_t:
    cs1: named_contracts_t = [
        (
            "durations",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[var],
                        output_vars=[], 
                        assumptions=[f"{var} >= {reqs[2]}"], 
                        guarantees=[]
                    )
                    for var in [
                        "duration_dsn1",
                        "duration_charging2",
                        "duration_sbo3",
                        "duration_tcm_h4",
                        "duration_tcm_dv5",
                        "duration_dsn6",
                        "duration_charging7",
                        "duration_sbo8",
                        "duration_tcm_h9",
                        "duration_tcm_dv10",
                        "duration_dsn11",
                        "duration_charging12",
                        "duration_sbo13",
                        "duration_tcm_h14",
                        "duration_tcm_dv15",
                        "duration_dsn16",
                        "duration_charging17",
                        "duration_sbo18",
                        "duration_tcm_h19",
                        "duration_tcm_dv20",
                    ]
                ],
            ),
        )
    ]
    cs2: named_contracts_t = [
        (
            "initial",
            PolyhedralIoContract.from_strings(
                input_vars=["soc1_entry", "c1_entry", "d1_entry", "u1_entry", "r1_entry"],
                output_vars=[],
                assumptions=[
                    f"soc1_entry = {reqs[0]}",
                    f"c1_entry = 0",
                    f"d1_entry = {reqs[3]}",
                    f"u1_entry = {reqs[4]}",
                    f"r1_entry = {reqs[5]}",
                ],
                guarantees=[],
            ),
        )
    ]
    cs3: named_contracts_t = [
        (
            "output_soc1-5",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"output_soc{i} >= {reqs[1]}"],
                    )
                    for i in range(1, 6)
                ],
            ),
        )
    ]
    cs4: named_contracts_t = [
        (
            "output_soc6-10",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"output_soc{i} >= {reqs[1]}"],
                    )
                    for i in range(5, 11)
                ],
            ),
        )
    ]
    cs5: named_contracts_t = [
        (
            "output_soc11-15",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"output_soc{i} >= {reqs[1]}"],
                    )
                    for i in range(10, 16)
                ],
            ),
        )
    ]
    cs6: named_contracts_t = [
        (
            "output_soc16-20",
            functools.reduce(
                PolyhedralIoContract.merge,
                [
                    PolyhedralIoContract.from_strings(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"output_soc{i} >= {reqs[1]}"],
                    )
                    for i in range(15, 21)
                ],
            ),
        )
    ]
    return cs1 + cs2 + cs3 + cs4 + cs5 + cs6


def schedulability_analysis20(
    scenario_reqs: Tuple[Tuple[list[tuple2float], PolyhedralIoContract], np.ndarray]
) -> Tuple[PactiInstrumentationData, schedule_result_t]:
    scenario = scenario_reqs[0]
    reqs = scenario_reqs[1]
    op_reqs: named_contracts_t = make_op_requirement_constraints20(reqs)
    result: merge_result_t = perform_merges_seq(scenario[1], op_reqs)
    if isinstance(result, PolyhedralIoContract):
        return PactiInstrumentationData().update_counts(), Schedule(scenario=scenario[0], reqs=reqs, contract=result)
    return PactiInstrumentationData().update_counts(), result


def schedulability_analysis20_grouped(samples_group: Tuple[Tuple[Tuple[list[tuple2float], PolyhedralIoContract], np.ndarray], ...]) -> List[Tuple[PactiInstrumentationData, schedule_result_t]]:
    return [schedulability_analysis20(sample) for sample in samples_group]
