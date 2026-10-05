#!/usr/bin/env python3
"""Phase 2 D-0028 ontology/lineage parity proof.

This proof intentionally separates:
1. native Dazzle state-machine legality checks; and
2. canonical master-repo transition requirement evaluation.

The canonical requirements are transition inputs in SixB, not Work properties.
We therefore do not fake them as Work fields just to obtain native `requires`
guards. That remaining adapter/runtime gap is reported explicitly.
"""

from __future__ import annotations

import json
from pathlib import Path

from dazzle.cli.utils import load_project_appspec
from dazzle.http.runtime.state_machine import InvalidTransitionError, TransitionValidator
from dazzle.http.specs.entity import StateMachineSpec as RuntimeStateMachineSpec


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "d0028_parity.json"


def field_map(entity):
    return {field.name: field for field in entity.fields}


def requirement_result(fixture: dict, from_state: str, to_state: str, provided: set[str]):
    transition = next(
        (
            item
            for item in fixture["lifecycle"]["transitions"]
            if item["from"] == from_state and item["to"] == to_state
        ),
        None,
    )
    if transition is None:
        return {"legal": False, "missing": []}
    missing = [item for item in transition["requires"] if item not in provided]
    return {"legal": True, "missing": missing}


def main() -> None:
    fixture = json.loads(FIXTURE.read_text())
    appspec = load_project_appspec(ROOT)
    entities = {entity.name: entity for entity in appspec.domain.entities}

    expected_entities = set(fixture["expected_entities"])
    missing_entities = sorted(expected_entities - set(entities))
    assert not missing_entities, f"missing entities: {missing_entities}"

    # Relationship/type parity for the bounded D-0028 graph.
    checked_refs: dict[str, dict[str, str]] = {}
    for entity_name, expected in fixture["expected_refs"].items():
        fields = field_map(entities[entity_name])
        checked_refs[entity_name] = {}
        for field_name, target in expected.items():
            assert field_name in fields, f"{entity_name}.{field_name} missing"
            actual = fields[field_name].type.ref_entity
            assert actual == target, f"{entity_name}.{field_name}: {actual} != {target}"
            checked_refs[entity_name][field_name] = actual

    work = entities["Work"]
    sm = work.state_machine
    assert sm is not None, "Work must compile to a Dazzle state machine"

    normalize = fixture["normalization"]
    expected_states = [normalize[state] for state in fixture["lifecycle"]["states"]]
    assert sm.states == expected_states, (sm.states, expected_states)

    expected_transitions = {
        (normalize[item["from"]], normalize[item["to"]])
        for item in fixture["lifecycle"]["transitions"]
    }
    actual_transitions = {(item.from_state, item.to_state) for item in sm.transitions}
    assert actual_transitions == expected_transitions, {
        "missing": sorted(expected_transitions - actual_transitions),
        "extra": sorted(actual_transitions - expected_transitions),
    }

    runtime_sm = RuntimeStateMachineSpec.model_validate(sm.model_dump(mode="json"))
    validator = TransitionValidator(runtime_sm)

    case_results: dict[str, dict[str, object]] = {}
    for case in fixture["sixb_proof_cases"]:
        source_from = case["from"]
        source_to = case["to"]
        normalized_from = normalize[source_from]
        normalized_to = normalize[source_to]

        native = validator.validate_transition(
            normalized_from,
            normalized_to,
            {},
        )
        requirements = requirement_result(
            fixture,
            source_from,
            source_to,
            set(case["provided"]),
        )

        if case["expected"] == "illegal":
            assert not native.is_valid
            assert isinstance(native.error, InvalidTransitionError)
            assert requirements["legal"] is False
        elif case["expected"] == "blocked":
            # The transition is legal in Dazzle's native graph, but the
            # canonical SixB transition-input requirements are incomplete.
            assert native.is_valid
            assert requirements["legal"] is True
            assert requirements["missing"] == case["missing"]
        elif case["expected"] == "allowed":
            assert native.is_valid
            assert requirements["legal"] is True
            assert requirements["missing"] == []
        else:
            raise AssertionError(f"unknown expected case: {case['expected']}")

        case_results[case["name"]] = {
            "native_dazzle_legal": native.is_valid,
            "canonical_requirements_legal": requirements["legal"],
            "missing_requirements": requirements["missing"],
            "expected": case["expected"],
        }

    # Authority split must stay visible in the model.
    runtime_transition = entities["RuntimeTransition"]
    transition_fields = field_map(runtime_transition)
    for required in [
        "work_id",
        "from_state",
        "to_state",
        "status",
        "legal",
        "evaluation_reason",
        "missing_requirements_json",
        "requested_at",
        "evaluated_at",
        "executed_at",
        "for_work",
        "produced_run",
        "produced_evidence",
        "verified_by",
    ]:
        assert required in transition_fields, f"RuntimeTransition.{required} missing"

    # No Dazzle transition effect mutates an external/canonical source. The
    # state machine here is an experimental projection only.
    assert all(not item.effects and item.invoke_flow is None for item in sm.transitions)

    result = {
        "status": "passed",
        "source": fixture["source"],
        "entities_checked": sorted(expected_entities),
        "relationship_refs_checked": checked_refs,
        "canonical_state_tokens": fixture["lifecycle"]["states"],
        "dazzle_state_tokens": sm.states,
        "normalization": normalize,
        "transition_graph_parity": "exact_after_explicit_token_normalization",
        "cases": case_results,
        "authority": fixture["authority"],
        "requirement_enforcement": {
            "native_dazzle_graph": True,
            "canonical_transition_requirements": "evaluated_by_parity_adapter",
            "reason": (
                "SixB requirements are transition inputs, not Work properties; "
                "the spike does not invent Work fields to fake native requires guards"
            ),
        },
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
