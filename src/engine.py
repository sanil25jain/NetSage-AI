import json
from pathlib import Path
from typing import Callable, Any

import pandas as pd
from checker import check_output


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "cases.csv"
PROMPT_FILE = BASE_DIR / "prompts" / "diagnose_prompt.md"


def load_cases() -> pd.DataFrame:
    """Load all network diagnostic cases."""
    return pd.read_csv(DATA_FILE)


def get_case(case_id: str) -> dict[str, Any]:
    """Get one case using its Case ID."""
    cases = load_cases()

    result = cases[cases["case_id"] == case_id]

    if result.empty:
        raise ValueError(f"Case {case_id} not found.")

    return result.iloc[0].to_dict()


def load_prompt() -> str:
    """Load the diagnostic prompt template."""
    return PROMPT_FILE.read_text(encoding="utf-8")


def run_deterministic_check(case: dict[str, Any]) -> dict[str, Any]:
    """Run checker.py against the case's Cisco CLI output."""
    return check_output(case["show_outputs"])


def build_llm_prompt(
    case: dict[str, Any],
    checker_result: dict[str, Any]
) -> str:
    """
    Combine the base diagnostic prompt with the selected
    case and deterministic checker result.
    """

    base_prompt = load_prompt()

    case_information = f"""
# Case Information

Case ID:
{case["case_id"]}

Symptom:
{case["symptom"]}

Topology:
{case["topology_note"]}

Concept:
{case["concept_tag"]}

Severity:
{case["severity"]}

Captured Cisco CLI Output:
{case["show_outputs"]}

Expected Fault:
{case["expected_fault"]}

# Deterministic Checker Result

{json.dumps(checker_result, indent=2)}
"""

    return base_prompt + "\n\n" + case_information


def validate_diagnosis(diagnosis: dict[str, Any]) -> bool:
    """
    Validate the structure returned by the LLM.
    """

    required_fields = {
        "root_cause",
        "osi_layer",
        "confidence",
        "evidence",
        "next_command",
        "fix_steps"
    }

    # Check fields
    if set(diagnosis.keys()) != required_fields:
        return False

    # Check confidence
    if not isinstance(diagnosis["confidence"], (int, float)):
        return False

    if not 0 <= diagnosis["confidence"] <= 1:
        return False

    # Check list fields
    if not isinstance(diagnosis["evidence"], list):
        return False

    if not isinstance(diagnosis["fix_steps"], list):
        return False

    return True


def parse_llm_response(response: str) -> dict[str, Any]:
    """
    Convert the LLM's JSON response into a Python dictionary.
    """

    try:
        diagnosis = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            "LLM returned invalid JSON."
        ) from error

    if not validate_diagnosis(diagnosis):
        raise ValueError(
            "LLM response does not match the required schema."
        )

    return diagnosis


def diagnose_case(
    case_id: str,
    llm
) -> dict[str, Any]:

    # 1. Load selected case
    case = get_case(case_id)

    # 2. Run deterministic checker
    checker_result = run_deterministic_check(case)

    # 3. Build LLM prompt
    prompt = build_llm_prompt(
        case,
        checker_result
    )

    # 4. Send prompt to Groq
    llm_response = llm.generate(prompt)

    # 5. Validate and parse JSON
    diagnosis = parse_llm_response(
        llm_response
    )

    # 6. Return complete result
    return {
        "case": case,
        "checker": checker_result,
        "diagnosis": diagnosis
    }


# Simple mock LLM for testing before connecting
# a real LLM provider.
def mock_llm(prompt: str) -> str:
    """
    Temporary LLM replacement used during development.
    """

    return json.dumps({
        "root_cause": "GigabitEthernet0/0.30 is administratively down",
        "osi_layer": "Layer 3",
        "confidence": 0.98,
        "evidence": [
            "GigabitEthernet0/0.30 is administratively down",
            "The symptom indicates connectivity failure for VLAN 30"
        ],
        "next_command": (
            "show running-config interface "
            "GigabitEthernet0/0.30"
        ),
        "fix_steps": [
            "configure terminal",
            "interface GigabitEthernet0/0.30",
            "no shutdown"
        ]
    })


if __name__ == "__main__":

    result = diagnose_case(
        "NET-001",
        mock_llm
    )

    print(json.dumps(result, indent=2))