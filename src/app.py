
import sys
from pathlib import Path

import streamlit as st

# Allow imports from src/
SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from audit import log_decision
from deployer import deploy
from verifier import verify_deployment
from engine import load_cases, diagnose_case
from llm import GroqLLM


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NetSage AI | Network Operations",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- Global ---------- */

    .stApp {
        background: #f6f8fb;
    }

    .main .block-container {
        max-width: 1480px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #101827;
        border-right: 1px solid #202c3d;
    }

    [data-testid="stSidebar"] * {
        color: #e8eef7;
    }

    [data-testid="stSidebar"] .stCaption {
        color: #8fa1b8 !important;
    }

    /* ---------- Typography ---------- */

    h1, h2, h3 {
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 750 !important;
        color: #111827 !important;
    }

    h2 {
        font-size: 1.45rem !important;
        font-weight: 720 !important;
        color: #182235 !important;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #253247 !important;
    }

    /* ---------- Hero ---------- */

    .ns-hero {
        background: linear-gradient(135deg, #101827 0%, #18273d 100%);
        border: 1px solid #26364c;
        border-radius: 20px;
        padding: 26px 30px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.10);
    }

    .ns-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .ns-logo {
        width: 46px;
        height: 46px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #dbeafe;
        color: #1d4ed8;
        font-size: 23px;
        font-weight: 800;
    }

    .ns-title {
        color: white;
        font-size: 28px;
        line-height: 1.1;
        font-weight: 760;
        margin: 0;
    }

    .ns-subtitle {
        color: #a9b8ca;
        font-size: 14px;
        margin-top: 5px;
    }

    .ns-status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(34, 197, 94, 0.12);
        color: #86efac;
        border: 1px solid rgba(134, 239, 172, 0.20);
        border-radius: 999px;
        padding: 7px 11px;
        font-size: 12px;
        font-weight: 650;
    }

    .ns-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.10);
    }

    /* ---------- Sidebar ---------- */

    .ns-side-title {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #73849a;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .ns-side-brand {
        font-size: 21px;
        font-weight: 760;
        color: white;
        margin-bottom: 2px;
    }

    .ns-side-copy {
        color: #8fa1b8;
        font-size: 12px;
        line-height: 1.5;
        margin-bottom: 22px;
    }

    /* ---------- Cards ---------- */

    .ns-card {
        background: white;
        border: 1px solid #e4e9f0;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.045);
        height: 100%;
    }

    .ns-card-label {
        color: #718096;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .ns-card-value {
        color: #182235;
        font-size: 16px;
        line-height: 1.45;
        font-weight: 650;
    }

    .ns-case-id {
        color: #1d4ed8;
        font-size: 13px;
        font-weight: 750;
        letter-spacing: 0.06em;
    }

    /* ---------- Pipeline ---------- */

    .ns-pipeline {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 8px;
        margin: 8px 0 22px;
    }

    .ns-step {
        background: white;
        border: 1px solid #e4e9f0;
        border-radius: 12px;
        padding: 10px 8px;
        text-align: center;
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
    }

    .ns-step.active {
        background: #eff6ff;
        border-color: #bfdbfe;
        color: #1d4ed8;
    }

    /* ---------- Section header ---------- */

    .ns-section {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 26px 0 12px;
    }

    .ns-section-line {
        height: 1px;
        background: #e5eaf1;
        flex: 1;
    }

    .ns-section-text {
        color: #182235;
        font-size: 15px;
        font-weight: 750;
        white-space: nowrap;
    }

    /* ---------- Finding ---------- */

    .ns-finding {
        background: #fff8ed;
        border: 1px solid #f5d7a8;
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 13px 15px;
        margin-bottom: 8px;
    }

    .ns-finding-id {
        color: #9a6700;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.05em;
    }

    .ns-finding-title {
        color: #422006;
        font-weight: 700;
        margin-top: 3px;
    }

    /* ---------- AI diagnosis ---------- */

    .ns-ai {
        background: #f8faff;
        border: 1px solid #dce7f8;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.035);
    }

    .ns-ai-label {
        color: #1d4ed8;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.09em;
    }

    .ns-root {
        color: #172033;
        font-size: 20px;
        line-height: 1.35;
        font-weight: 730;
        margin-top: 7px;
    }

    /* ---------- Confidence ---------- */

    .ns-confidence {
        background: white;
        border: 1px solid #e4e9f0;
        border-radius: 14px;
        padding: 14px 16px;
    }

    .ns-confidence-number {
        font-size: 24px;
        color: #172033;
        font-weight: 760;
    }

    .ns-confidence-label {
        color: #718096;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 750;
    }

    /* ---------- HITL ---------- */

    .ns-gate {
        background: #fff;
        border: 1px solid #dbe3ed;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 5px 20px rgba(15, 23, 42, 0.045);
    }

    .ns-gate-title {
        font-size: 18px;
        font-weight: 750;
        color: #182235;
    }

    .ns-gate-copy {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
    }

    /* ---------- Footer ---------- */

    .ns-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        padding: 30px 0 5px;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        min-height: 44px;
        border-radius: 11px;
        font-weight: 700;
        border: 1px solid #dbe3ed;
        transition: all 0.16s ease;
    }

    .stButton > button:hover {
        border-color: #93c5fd;
        transform: translateY(-1px);
        box-shadow: 0 5px 14px rgba(15, 23, 42, 0.08);
    }

    /* ---------- Code ---------- */

    [data-testid="stCode"] {
        border-radius: 13px;
    }

    /* ---------- Responsive ---------- */

    @media (max-width: 900px) {
        .ns-pipeline {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (max-width: 600px) {
        .ns-pipeline {
            grid-template-columns: repeat(2, 1fr);
        }

        .ns-hero {
            padding: 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def section_title(title: str):
    st.markdown(
        f"""
        <div class="ns-section">
            <div class="ns-section-text">{title}</div>
            <div class="ns-section-line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def clear_case_state():
    """Clear results when the operator switches cases."""
    for key in [
        "diagnosis",
        "decision",
        "deployment",
        "verification",
        "edited_commands",
    ]:
        st.session_state.pop(key, None)


# ============================================================
# LOAD DATA
# ============================================================

cases = load_cases()

case_ids = cases["case_id"].tolist()

if not case_ids:
    st.error("No diagnostic cases are available.")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="ns-side-brand">◈ NetSage AI</div>
        <div class="ns-side-copy">
            Network operations intelligence for Cisco
            troubleshooting and human-reviewed remediation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="ns-side-title">Case Control</div>',
        unsafe_allow_html=True,
    )

    selected_case_id = st.selectbox(
        "Diagnostic case",
        case_ids,
        label_visibility="collapsed",
    )

    st.caption(
        f"{len(case_ids)} diagnostic scenarios available"
    )

    st.markdown("---")

    st.markdown(
        '<div class="ns-side-title">System</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            color:#8fa1b8;
            font-size:12px;
            line-height:1.8;
        ">
            <b style="color:#dbe5f1;">Checker</b> · Deterministic<br>
            <b style="color:#dbe5f1;">LLM</b> · Groq<br>
            <b style="color:#dbe5f1;">Deployment</b> · Simulation<br>
            <b style="color:#dbe5f1;">Control</b> · Human approval
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.caption("NetSage AI · Network Diagnostic Platform")


# Clear stale results when case changes
if st.session_state.get("active_case") != selected_case_id:
    clear_case_state()
    st.session_state["active_case"] = selected_case_id


# Get selected case
case = cases[
    cases["case_id"] == selected_case_id
].iloc[0]


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="ns-hero">
        <div class="ns-brand">
            <div class="ns-logo">◈</div>
            <div style="flex:1;">
                <div class="ns-title">NetSage AI</div>
                <div class="ns-subtitle">
                    Hybrid network diagnosis · deterministic checks · AI reasoning · human control
                </div>
            </div>
            <div class="ns-status">
                <span class="ns-dot"></span>
                SYSTEM READY
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PIPELINE
# ============================================================

st.markdown(
    """
    <div class="ns-pipeline">
        <div class="ns-step active">01 · CASE</div>
        <div class="ns-step">02 · CHECK</div>
        <div class="ns-step">03 · AI</div>
        <div class="ns-step">04 · REVIEW</div>
        <div class="ns-step">05 · SIMULATE</div>
        <div class="ns-step">06 · AUDIT</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CASE OVERVIEW
# ============================================================

section_title("Incident Overview")

top1, top2, top3, top4 = st.columns(4)

with top1:
    st.markdown(
        f"""
        <div class="ns-card">
            <div class="ns-card-label">Case</div>
            <div class="ns-case-id">{selected_case_id}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top2:
    st.markdown(
        f"""
        <div class="ns-card">
            <div class="ns-card-label">Concept</div>
            <div class="ns-card-value">{case["concept_tag"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top3:
    st.markdown(
        f"""
        <div class="ns-card">
            <div class="ns-card-label">Severity</div>
            <div class="ns-card-value">{case["severity"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top4:
    st.markdown(
        f"""
        <div class="ns-card">
            <div class="ns-card-label">Analysis Mode</div>
            <div class="ns-card-value">Hybrid · AI + Rules</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


left, right = st.columns([1.35, 1])

with left:
    section_title("Observed Symptom")
    st.markdown(
        f"""
        <div class="ns-card">
            <div class="ns-card-value">
                {case["symptom"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    section_title("Topology Context")
    st.markdown(
        f"""
        <div class="ns-card">
            <div class="ns-card-value">
                {case["topology_note"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CLI EVIDENCE
# ============================================================

section_title("Cisco CLI Evidence")

with st.expander("View captured CLI output", expanded=True):
    st.code(
        case["show_outputs"],
        language="text",
    )


# ============================================================
# RUN DIAGNOSIS
# ============================================================

run_col, status_col = st.columns([1, 4])

with run_col:
    run_diagnosis = st.button(
        "🔍 Run Diagnosis",
        type="primary",
        use_container_width=True,
    )

with status_col:
    if "diagnosis" not in st.session_state:
        st.info(
            "Ready to analyze this case. "
            "The deterministic checker will run before the LLM."
        )


if run_diagnosis:

    try:
        with st.spinner(
            "Running deterministic checks and Groq diagnosis..."
        ):

            llm = GroqLLM()

            result = diagnose_case(
                selected_case_id,
                llm,
            )

            st.session_state["diagnosis"] = result
            st.session_state.pop("decision", None)
            st.session_state.pop("deployment", None)
            st.session_state.pop("verification", None)

        st.success("Diagnosis completed.")

    except Exception as error:

        st.error(
            f"Diagnostic error: {error}"
        )


# ============================================================
# DIAGNOSIS
# ============================================================

if "diagnosis" in st.session_state:

    result = st.session_state["diagnosis"]

    checker = result["checker"]
    diagnosis = result["diagnosis"]

    section_title("Diagnostic Analysis")

    # --------------------------------------------------------
    # Checker status
    # --------------------------------------------------------

    checker_col, finding_col = st.columns([1, 2.4])

    with checker_col:

        if checker["status"] == "ERRORS_DETECTED":

            st.error(
                f"CHECKER\n\n{checker['status']}"
            )

        else:

            st.success(
                f"CHECKER\n\n{checker['status']}"
            )

    with finding_col:

        st.markdown(
            f"""
            <div class="ns-card">
                <div class="ns-card-label">Deterministic Findings</div>
                <div class="ns-card-value">
                    {len(checker["flagged_issues"])} issue(s) flagged
                    by the deterministic engine.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # Findings
    # --------------------------------------------------------

    if checker["flagged_issues"]:

        for issue in checker["flagged_issues"]:

            with st.expander(
                f"⚠ {issue['check_id']} · {issue['module']}",
                expanded=False,
            ):

                f1, f2 = st.columns(2)

                with f1:
                    st.write("**Issue**")
                    st.write(issue["issue"])

                with f2:
                    st.write("**OSI Layer**")
                    st.write(issue["osi_layer"])

                st.write("**Suggested Remediation**")
                st.write(issue["remediation"])


    # --------------------------------------------------------
    # AI diagnosis
    # --------------------------------------------------------

    section_title("AI Diagnosis")

    ai_left, ai_right = st.columns([2.1, 1])

    with ai_left:

        st.markdown(
            f"""
            <div class="ns-ai">
                <div class="ns-ai-label">Root Cause</div>
                <div class="ns-root">
                    {diagnosis["root_cause"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with ai_right:

        confidence = float(diagnosis["confidence"])
        confidence = max(0.0, min(1.0, confidence))

        st.markdown(
            f"""
            <div class="ns-confidence">
                <div class="ns-confidence-label">AI Confidence</div>
                <div class="ns-confidence-number">
                    {confidence * 100:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(confidence)

        st.caption(
            f"OSI layer · {diagnosis['osi_layer']}"
        )


    # --------------------------------------------------------
    # Evidence + next command
    # --------------------------------------------------------

    ev_col, cmd_col = st.columns(2)

    with ev_col:

        section_title("Evidence")

        for evidence in diagnosis["evidence"]:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    border:1px solid #e4e9f0;
                    border-radius:10px;
                    padding:10px 13px;
                    margin-bottom:7px;
                    color:#334155;
                    font-size:13px;
                ">
                    ✓ {evidence}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with cmd_col:

        section_title("Next Verification Command")

        st.code(
            diagnosis["next_command"],
            language="text",
        )


    # --------------------------------------------------------
    # Proposed fix
    # --------------------------------------------------------

    section_title("Proposed Remediation")

    fix_commands = "\n".join(
        diagnosis["fix_steps"]
    )

    st.code(
        fix_commands,
        language="text",
    )


    # ========================================================
    # HUMAN GATE
    # ========================================================

    section_title("Human Verification Gate")

    st.markdown(
        """
        <div class="ns-gate">
            <div class="ns-gate-title">
                Review before remediation
            </div>
            <div class="ns-gate-copy">
                NetSage will never bypass the engineer.
                Choose an action below to continue.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    action1, action2, action3 = st.columns(3)

    # --------------------------------------------------------
    # APPROVE
    # --------------------------------------------------------

    with action1:

        if st.button(
            "✅ Approve & Deploy",
            use_container_width=True,
        ):

            st.session_state["decision"] = "APPROVED"

            with st.spinner(
                "Simulating approved remediation..."
            ):

                deployment_result = deploy(
                    selected_case_id,
                    diagnosis["fix_steps"],
                )

            st.session_state["deployment"] = deployment_result

            if deployment_result["status"] == "SUCCESS":

                st.success(
                    "Deployment simulation successful."
                )

                verification_result = verify_deployment(
                    selected_case_id,
                    deployment_result,
                )

                st.session_state["verification"] = (
                    verification_result
                )

                if verification_result["status"] == "VERIFIED":

                    st.success(
                        "Post-deployment verification passed."
                    )

                else:

                    st.error(
                        "Post-deployment verification failed."
                    )

                log_decision(
                    selected_case_id,
                    diagnosis,
                    "APPROVED",
                    deployment_result=deployment_result,
                    verification_result=verification_result,
                )

            else:

                st.error(
                    "Deployment simulation failed."
                )

                log_decision(
                    selected_case_id,
                    diagnosis,
                    "APPROVED",
                    deployment_result=deployment_result,
                )


    # --------------------------------------------------------
    # EDIT
    # --------------------------------------------------------

    with action2:

        if st.button(
            "✏️ Edit Commands",
            use_container_width=True,
        ):

            st.session_state["decision"] = "EDIT"


    # --------------------------------------------------------
    # REJECT
    # --------------------------------------------------------

    with action3:

        if st.button(
            "❌ Reject",
            use_container_width=True,
        ):

            st.session_state["decision"] = "REJECTED"

            log_decision(
                selected_case_id,
                diagnosis,
                "REJECTED",
            )

            st.error(
                "Diagnosis rejected and recorded as a false positive."
            )


    # ========================================================
    # EDIT WORKFLOW
    # ========================================================

    if st.session_state.get("decision") == "EDIT":

        st.markdown("### Edit Proposed Commands")

        edited_commands = st.text_area(
            "CLI Commands",
            value=st.session_state.get(
                "edited_commands",
                fix_commands,
            ),
            height=190,
            key="edited_commands_box",
            help="Modify the remediation before simulated deployment.",
        )

        st.caption(
            "Only the edited commands will be sent to the deployment simulator."
        )

        if st.button(
            "💾 Save & Deploy Edited Commands",
            type="primary",
            use_container_width=False,
        ):

            edited_steps = [
                command.strip()
                for command in edited_commands.splitlines()
                if command.strip()
            ]

            st.session_state["edited_commands"] = (
                edited_commands
            )

            if not edited_steps:

                st.error(
                    "No commands provided. Enter at least one command."
                )

            else:

                with st.spinner(
                    "Simulating edited remediation..."
                ):

                    deployment_result = deploy(
                        selected_case_id,
                        edited_steps,
                    )

                st.session_state["deployment"] = (
                    deployment_result
                )

                if deployment_result["status"] == "SUCCESS":

                    st.success(
                        "Edited commands deployed successfully."
                    )

                    verification_result = verify_deployment(
                        selected_case_id,
                        deployment_result,
                    )

                    st.session_state["verification"] = (
                        verification_result
                    )

                    if verification_result["status"] == "VERIFIED":

                        st.success(
                            "Post-deployment verification passed."
                        )

                    else:

                        st.error(
                            "Post-deployment verification failed."
                        )

                    log_decision(
                        selected_case_id,
                        diagnosis,
                        "EDITED",
                        edited_commands=edited_commands,
                        deployment_result=deployment_result,
                        verification_result=verification_result,
                    )

                else:

                    st.error(
                        "Edited deployment failed."
                    )

                    log_decision(
                        selected_case_id,
                        diagnosis,
                        "EDITED",
                        edited_commands=edited_commands,
                        deployment_result=deployment_result,
                    )


    # ========================================================
    # DEPLOYMENT / VERIFICATION RESULTS
    # ========================================================

    deployment = st.session_state.get("deployment")
    verification = st.session_state.get("verification")

    if deployment:

        section_title("Deployment Simulation")

        d1, d2 = st.columns([1, 2.5])

        with d1:

            if deployment["status"] == "SUCCESS":
                st.success("SUCCESS")
            else:
                st.error("FAILED")

        with d2:

            st.write(deployment["message"])

            for command in deployment.get("commands", []):

                if command["status"] == "SUCCESS":

                    st.write(
                        f"✓ `{command['command']}`"
                    )

                else:

                    st.write(
                        f"✗ `{command['command']}`"
                    )


    if verification:

        section_title("Post-Deployment Verification")

        if verification["status"] == "VERIFIED":

            st.success(
                verification["message"]
            )

        elif verification["status"] == "SKIPPED":

            st.info(
                verification["message"]
            )

        else:

            st.error(
                verification["message"]
            )

        for check in verification.get("checks", []):

            if check["status"] == "PASSED":

                st.write(
                    f"✓ **{check['check']}** — PASSED"
                )

            else:

                st.write(
                    f"✗ **{check['check']}** — FAILED"
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="ns-footer">
        NetSage AI · Hybrid diagnostics · Human-in-the-loop ·
        Simulation-first network remediation
    </div>
    """,
    unsafe_allow_html=True,
)
