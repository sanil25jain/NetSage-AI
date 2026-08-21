from pathlib import Path
from datetime import datetime
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent.parent

AUDIT_FILE = BASE_DIR / "docs" / "model_audit_log.md"


def initialize_audit_log():
    """Create the audit log if it does not already exist."""

    AUDIT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not AUDIT_FILE.exists():

        content = """# NetSage AI Model Audit Log

This file records diagnostic decisions, engineer overrides,
deployment results, verification results, and false positives.

---

"""

        AUDIT_FILE.write_text(
            content,
            encoding="utf-8"
        )


def log_decision(
    case_id: str,
    diagnosis: dict,
    decision: str,
    edited_commands: Optional[str] = None,
    deployment_result: Optional[dict] = None,
    verification_result: Optional[dict] = None
):
    """Record the complete diagnostic lifecycle."""

    # 1. Initialize audit log
    initialize_audit_log()

    # 2. Get timestamp
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # 3. Get root cause
    root_cause = diagnosis.get(
        "root_cause",
        "Unknown"
    )

    # 4. Get confidence
    confidence = diagnosis.get(
        "confidence",
        0
    )

    # 5. Create basic entry
    entry = f"""
## Diagnostic Record

**Timestamp:** {timestamp}

**Case ID:** {case_id}

**Root Cause:** {root_cause}

**Confidence:** {confidence}

**Human Decision:** {decision}

"""

    # 6. Add evidence
    evidence = diagnosis.get(
        "evidence",
        []
    )

    if evidence:

        entry += "**Evidence:**\n\n"

        for item in evidence:

            entry += f"- {item}\n"

        entry += "\n"

    # 7. Add proposed fix
    fix_steps = diagnosis.get(
        "fix_steps",
        []
    )

    if fix_steps:

        entry += "**Proposed Fix:**\n\n"

        for step in fix_steps:

            entry += f"```text\n{step}\n```\n"

        entry += "\n"

    # 8. Add edited commands
    if edited_commands:

        entry += f"""**Edited Commands:**

```text
{edited_commands}

"""

    # 9. Add deployment result
    if deployment_result:

        deployment_status = deployment_result.get(
            "status",
            "UNKNOWN"
        )

        entry += (
            f"**Deployment Status:** "
            f"{deployment_status}\n\n"
        )

        deployment_message = deployment_result.get(
            "message",
            ""
        )

        if deployment_message:

            entry += (
                f"**Deployment Message:** "
                f"{deployment_message}\n\n"
            )

    # 10. Add verification result
    if verification_result:

        verification_status = verification_result.get(
            "status",
            "UNKNOWN"
        )

        entry += (
            f"**Verification Status:** "
            f"{verification_status}\n\n"
        )

        verification_message = verification_result.get(
            "message",
            ""
        )

        if verification_message:

            entry += (
                f"**Verification Message:** "
                f"{verification_message}\n\n"
            )

    # 11. Add audit status
    if decision == "APPROVED":

        entry += (
            "**Audit Status:** "
            "Approved for deployment\n\n"
        )

    elif decision == "EDITED":

        entry += (
            "**Audit Status:** "
            "Engineer modified proposed remediation\n\n"
        )

    elif decision == "REJECTED":

        entry += (
            "**Audit Status:** "
            "Rejected / possible false positive\n\n"
        )

    # 12. End record
    entry += "---\n"

    # 13. Write to audit log
    with AUDIT_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(entry)
