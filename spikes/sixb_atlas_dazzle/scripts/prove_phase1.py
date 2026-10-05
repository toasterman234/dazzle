#!/usr/bin/env python3
"""Phase 1 executable proof for the SixB/Atlas Dazzle spike."""

from __future__ import annotations

import json
from pathlib import Path

from dazzle.cli.utils import load_project_appspec
from dazzle.http.runtime.state_machine import (
    GuardNotSatisfiedError,
    InvalidTransitionError,
    TransitionValidator,
)
from dazzle.http.specs.entity import StateMachineSpec as RuntimeStateMachineSpec


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    appspec = load_project_appspec(project_root)

    work = next(entity for entity in appspec.domain.entities if entity.name == "Work")
    state_machine = work.state_machine
    assert state_machine is not None, "Work must compile to a state machine"

    assert state_machine.is_transition_allowed("ready", "in_progress")
    assert not state_machine.is_transition_allowed("ready", "done")
    assert state_machine.is_transition_allowed("in_progress", "verifying")

    terminal = state_machine.get_transition("verifying", "done")
    assert terminal is not None, "verifying -> done must exist"
    assert len(terminal.guards) == 1
    assert terminal.guards[0].requires_field == "verification_evidence"

    runtime_sm = RuntimeStateMachineSpec.model_validate(
        state_machine.model_dump(mode="json")
    )
    validator = TransitionValidator(runtime_sm)

    start = validator.validate_transition("ready", "in_progress", {})
    assert start.is_valid

    skip = validator.validate_transition("ready", "done", {})
    assert not skip.is_valid
    assert isinstance(skip.error, InvalidTransitionError)

    verify = validator.validate_transition("in_progress", "verifying", {})
    assert verify.is_valid

    missing_evidence = validator.validate_transition("verifying", "done", {})
    assert not missing_evidence.is_valid
    assert isinstance(missing_evidence.error, GuardNotSatisfiedError)
    assert missing_evidence.error.guard_value == "verification_evidence"

    with_evidence = validator.validate_transition(
        "verifying",
        "done",
        {"verification_evidence": "phase1-proof-evidence"},
    )
    assert with_evidence.is_valid

    result = {
        "status": "passed",
        "project": appspec.name,
        "entity": "Work",
        "states": state_machine.states,
        "cases": {
            "ready_to_in_progress": "allowed",
            "ready_to_done": "rejected_invalid_transition",
            "in_progress_to_verifying": "allowed",
            "verifying_to_done_without_evidence": "rejected_guard",
            "verifying_to_done_with_evidence": "allowed",
        },
        "terminal_guard": {
            "type": "requires_field",
            "field": "verification_evidence",
        },
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
