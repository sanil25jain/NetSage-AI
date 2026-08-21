# 🌐 NetSage AI

## Automated Network Diagnostic Platform

NetSage AI is an AI-assisted network troubleshooting platform designed
for Cisco IOS / Packet Tracer environments.

It combines deterministic network validation with a Groq-powered LLM
and a mandatory Human-in-the-Loop (HITL) verification gate.

---

## Features

- 30 structured Cisco networking diagnostic cases
- Deterministic rule-based network checker
- Groq LLM-powered diagnosis
- Structured JSON diagnostic output
- OSI layer identification
- Evidence extraction
- Suggested verification commands
- Remediation CLI commands
- Human approval, editing, and rejection
- Deployment simulation
- Post-deployment verification
- Audit logging
- Model evaluation

---

## Architecture

```text
                    NetSage AI
                         │
                    cases.csv
                         │
                         ▼
                Deterministic Checker
                    checker.py
                         │
                         ▼
                     engine.py
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
           Rule Findings       Groq LLM
                │                 │
                └────────┬────────┘
                         ▼
                   AI Diagnosis
                         │
                         ▼
                 Streamlit Dashboard
                         │
                  Human Review Gate
                  /       |       \
             Approve     Edit     Reject
                │          │         │
                ▼          ▼         ▼
             Deploy     Deploy     Audit
                │          │
                ▼          ▼
             Verify      Verify
                │          │
                └────┬─────┘
                     ▼
                 Audit Log
```

---

## Technology Stack

- Python
- Streamlit
- Pandas
- Groq
- JSON
- Cisco IOS / Packet Tracer target environment

---

## Project Structure

```text
NetSage AI/
│
├── data/
│   ├── cases.csv
│   ├── system_config.json
│   └── model_evaluation.csv
│
├── docs/
│   └── model_audit_log.md
│
├── prompts/
│   └── diagnose_prompt.md
│
├── src/
│   ├── app.py
│   ├── audit.py
│   ├── checker.py
│   ├── config.py
│   ├── deployer.py
│   ├── engine.py
│   ├── llm.py
│   ├── verifier.py
│   
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## How It Works

### 1. Select a case

The operator selects one of the 30 networking scenarios.

### 2. Deterministic analysis

`checker.py` searches the captured Cisco CLI output for known
configuration and status problems.

### 3. AI diagnosis

The detected findings and case context are passed to the Groq LLM.

The model returns structured diagnostic information:

```text
root_cause
osi_layer
confidence
evidence
next_command
fix_steps
```

### 4. Human verification

The engineer reviews the diagnosis and can:

- Approve the remediation
- Edit the proposed commands
- Reject the diagnosis

### 5. Deployment simulation

Approved commands are passed to the deployment simulator.

No real network device is modified.

### 6. Verification

The simulated deployment is followed by a verification step.

### 7. Audit

The decision, deployment result, and verification result are recorded
in:

```text
docs/model_audit_log.md
```

---

## Evaluation

The deterministic checker was tested against all 30 benchmark cases:

```text
Total cases : 30
Passed      : 30
Failed      : 0
```

The Groq diagnostic evaluation achieved:

```text
Total cases       : 30
Agreements        : 30
Disagreements     : 0
API errors        : 0
Agreement rate    : 100.00%
```

This represents agreement on the project's 30-case benchmark dataset,
not a claim of 100% real-world network diagnostic accuracy.

---

## Running the Project

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate it

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API key

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
streamlit run src/app.py
```

---

## Safety

NetSage AI does not directly execute AI-generated commands on a real
network device.

The current deployment layer operates in simulation mode.

Human approval is required before the simulated deployment workflow.

---

## License

For educational and demonstration purposes.