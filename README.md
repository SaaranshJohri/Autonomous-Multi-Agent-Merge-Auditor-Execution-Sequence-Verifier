# 🧠 MergeMind

### Autonomous Multi-Agent Semantic Merge Auditor & Execution-Sequence Verifier

> **Git tells you whether code conflicts. MergeMind tells you whether your code will still work.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![AST](https://img.shields.io/badge/Analysis-Python%20AST-orange?style=for-the-badge)](https://docs.python.org/3/library/ast.html)
[![NetworkX](https://img.shields.io/badge/Graph-NetworkX-blue?style=for-the-badge)](https://networkx.org/)
[![Docker](https://img.shields.io/badge/Sandbox-Docker-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)](https://www.docker.com/)
[![LangGraph](https://img.shields.io/badge/Agents-LangGraph-black?style=for-the-badge)](https://www.langchain.com/langgraph)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=for-the-badge)]()

---

## 🚨 The Problem

Modern software development is built around parallel collaboration.

Multiple developers can simultaneously modify:

* the same functions
* shared APIs
* database operations
* dependencies
* execution sequences
* global state
* configuration
* external service interactions

Git is extremely effective at detecting **textual conflicts**.

But textual compatibility does **not** guarantee behavioral compatibility.

Consider:

```python
# Developer A
def calculate_price(price, tax):
    return price + tax
```

and:

```python
# Developer B
def calculate_price(price):
    return price * 0.9
```

The branches may be mergeable from Git's perspective.

But elsewhere in the application:

```python
calculate_price(100, 18)
```

still exists.

The result?

```text
The merge succeeds.
The application fails.
```

### This is the gap MergeMind targets.

---

# 💡 What is MergeMind?

**MergeMind** is an autonomous software-engineering system designed to detect **semantic merge conflicts** that traditional version-control systems may fail to identify.

Instead of treating a Pull Request as a simple textual diff, MergeMind attempts to understand:

```text
Code Structure
      ↓
Dependencies
      ↓
Execution Flow
      ↓
API Contracts
      ↓
Side Effects
      ↓
Runtime Behaviour
```

It combines:

* 🧩 AST-based static analysis
* 🕸️ dependency and control-flow graphs
* 🤖 specialized AI auditing agents
* 🧠 agent orchestration
* 🐳 isolated runtime execution
* 🔍 explainable failure diagnosis
* 🛠️ automated patch suggestions
* 🔗 GitHub Pull Request integration

---

# 🎯 Core Objective

MergeMind aims to answer a question that traditional merge systems often cannot:

> **"If these changes are merged, will the resulting software still behave correctly?"**

The system ultimately produces one of two outcomes:

```text
                    MERGE AUDIT
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
            PASS                  FAIL
              │                     │
              ▼                     ▼
        Safe to Merge         Explain Why
                                      │
                                      ▼
                              Suggested Fix
```

---

# 🏗️ System Architecture

```text
                         ┌─────────────────┐
                         │    Developer    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     GitHub      │
                         │  Pull Request   │
                         └────────┬────────┘
                                  │
                              Webhook
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │    MergeMind Gateway    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Repository Manager    │
                    │                         │
                    │ Base + PR + Merge      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    STATIC ANALYSIS      │
                    │                         │
                    │ AST / Tree-sitter       │
                    │ Dependency Graph        │
                    │ Control Flow Graph      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    AGENT SUPERVISOR     │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌────────────┐     ┌────────────┐     ┌────────────┐
       │  Sequence  │     │    API     │     │ Side Effect│
       │   Agent    │     │   Agent    │     │   Agent    │
       └─────┬──────┘     └─────┬──────┘     └─────┬──────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │     DOCKER SANDBOX      │
                    │                         │
                    │ Unit Tests              │
                    │ Integration Tests       │
                    │ Runtime Verification    │
                    └────────────┬────────────┘
                                 │
                         ┌───────┴───────┐
                         │               │
                         ▼               ▼
                       PASS             FAIL
                         │               │
                         ▼               ▼
                  ┌────────────┐   ┌─────────────┐
                  │ Auto Merge │   │ XAI Engine  │
                  └────────────┘   └──────┬──────┘
                                          │
                                          ▼
                                  ┌────────────────┐
                                  │ Diagnosis +    │
                                  │ Patch Suggestion│
                                  └────────────────┘
```

---

# 🔬 How MergeMind Thinks

Traditional merge systems primarily ask:

```text
"Did the same lines change?"
```

MergeMind asks:

```text
"What changed?"
        ↓
"What depends on it?"
        ↓
"Did an API contract change?"
        ↓
"Did execution order change?"
        ↓
"Did side effects change?"
        ↓
"Does the merged program still execute?"
        ↓
"Can we explain the failure?"
```

---

# 🧩 Major Components

## 1. AST Analysis

MergeMind converts source code into an **Abstract Syntax Tree (AST)**.

For example:

```python
def calculate(a, b):
    return a + b
```

becomes conceptually:

```text
FunctionDef
│
├── name: calculate
│
├── arguments
│   ├── a
│   └── b
│
└── Return
    └── a + b
```

This allows MergeMind to reason about code structure rather than only text.

The current parser extracts:

* imports
* functions
* classes
* function calls
* variables
* source locations

---

# 🕸️ Dependency Analysis

Once code structure is understood, MergeMind builds relationships between components.

Example:

```text
main.py
   │
   ├──────────────► auth.py
   │                    │
   │                    ▼
   │               database.py
   │
   └──────────────► payment.py
                        │
                        ▼
                   database.py
```

These relationships allow MergeMind to identify potentially affected components when a developer changes one function or module.

Planned technologies:

* NetworkX
* AST
* Tree-sitter
* Control Flow Graphs

---

# 🤖 Multi-Agent Semantic Auditing

MergeMind uses specialized agents rather than asking one general-purpose model to analyze everything.

### Sequence Auditor

Checks:

* execution ordering
* prerequisite operations
* control-flow changes
* initialization dependencies

Example:

```text
authenticate()
     ↓
fetch_data()
```

becoming:

```text
fetch_data()
     ↓
authenticate()
```

can indicate a semantic conflict.

---

### API Contract Auditor

Checks:

* function signatures
* parameters
* return values
* imports
* API schemas
* callers

Example:

```text
Before:
get_user(id)

After:
get_user(id, token)

Existing caller:
get_user(42)
```

Potential result:

```text
⚠️ API CONTRACT VIOLATION
```

---

### Side-Effect Auditor

Checks potentially dangerous interactions involving:

* databases
* files
* global state
* external APIs
* shared resources
* state mutations

Example:

```text
Branch A → UPDATE users
Branch B → DELETE users
```

Potential result:

```text
⚠️ SIDE-EFFECT COLLISION
```

---

# 🧠 Agent Supervisor

The agents are coordinated through a supervisor.

```text
                 SUPERVISOR
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
   Sequence         API       Side Effect
     Agent         Agent          Agent
       │             │             │
       └─────────────┼─────────────┘
                     ▼
               Final Analysis
```

The supervisor combines their findings and determines whether deeper runtime verification is required.

---

# 🐳 Runtime Verification

Static analysis alone cannot guarantee correctness.

Therefore, MergeMind plans to execute the merged project inside an isolated Docker environment.

```text
Merged Code
     │
     ▼
Docker Container
     │
     ├── Install dependencies
     │
     ├── Run unit tests
     │
     ├── Run integration tests
     │
     └── Capture runtime logs
              │
              ▼
        PASS / FAILURE
```

This provides a second layer of verification.

---

# 🔍 Explainable AI Diagnosis

A simple:

```text
❌ Merge Failed
```

is not enough.

MergeMind aims to explain:

```text
❌ MERGE REJECTED

Reason:
Function signature mismatch

Changed Function:
calculate_price()

Expected:
calculate_price(price, tax)

Found:
calculate_price(price)

Affected File:
checkout.py

Affected Line:
42

Runtime Error:
TypeError

Suggested Action:
Restore backward compatibility or update
the affected caller.
```

This makes the system useful to developers rather than simply acting as another CI failure.

---

# 🛠️ Planned Patch Generation

When a semantic conflict is detected, MergeMind can generate a suggested patch.

Example:

```diff
- def calculate_price(price):
+ def calculate_price(price, tax=None):
```

The patch is **suggested for developer review** rather than blindly applied.

---

# 🔄 Complete Workflow

```text
1. Developer creates Pull Request
                ↓
2. GitHub triggers MergeMind
                ↓
3. MergeMind retrieves repository state
                ↓
4. Base and incoming branches are analyzed
                ↓
5. AST structures are generated
                ↓
6. Dependencies and control flow are mapped
                ↓
7. Potential semantic conflicts are identified
                ↓
8. Specialized AI agents audit the changes
                ↓
9. Merged code is executed in Docker
                ↓
10. Tests and runtime behaviour are analyzed
                ↓
11. Final merge decision is generated
                ↓
          ┌─────┴─────┐
          ▼           ▼
        PASS         FAIL
          │           │
          ▼           ▼
     Auto-Merge    XAI Report
                      │
                      ▼
               Patch Suggestion
```

---

# 🧪 Conflict Types

MergeMind is designed to detect multiple categories of semantic conflicts.

| Conflict            | Example                                        |
| ------------------- | ---------------------------------------------- |
| Function Signature  | Parameter count/type changes                   |
| Broken Dependency   | Removed function still being called            |
| Import Conflict     | Deleted or renamed module/function             |
| Execution Order     | Dependent operation executes too early         |
| API Contract        | Caller and implementation disagree             |
| Side Effect         | Conflicting database/state operations          |
| Control Flow        | Changed branch behavior                        |
| Runtime Failure     | Merged code fails during execution             |
| Integration Failure | Components work individually but fail together |

---

# 📊 Evaluation Metrics

MergeMind will be evaluated using:

### Semantic Conflict Recall

```text
Detected Semantic Conflicts
──────────────────────────── × 100
Total Semantic Conflicts
```

Measures how many real semantic conflicts the system detects.

### False Positive Rate

Measures how frequently MergeMind flags a merge that is actually safe.

### Audit Latency

Measures:

```text
PR received
     ↓
Final decision
```

### Runtime Verification Success

Measures how effectively dynamic testing catches issues missed by static analysis.

---

# 🧪 Planned Test Scenarios

The project will include intentionally problematic merge scenarios.

```text
tests/
│
├── test_signature_conflict/
├── test_removed_function/
├── test_import_conflict/
├── test_dependency_conflict/
├── test_sequence_conflict/
├── test_side_effect_conflict/
├── test_runtime_failure/
└── test_safe_merge/
```

Each scenario will contain:

```text
Base Branch
Incoming Branch
Expected Result
Actual Result
```

---

# 📁 Project Structure

Current development structure:

```text
MergeMind/
│
├── backend/
│   ├── main.py
│   ├── ast_parser.py
│   └── requirements.txt
│
├── sample_repos/
│   └── test.py
│
├── tests/
│
├── README.md
│
└── venv/
```

Planned architecture:

```text
MergeMind/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   │
│   ├── github/
│   │   └── webhook.py
│   │
│   ├── parser/
│   │   ├── ast_parser.py
│   │   ├── dependency.py
│   │   └── cfg.py
│   │
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── sequence_agent.py
│   │   ├── api_agent.py
│   │   └── side_effect_agent.py
│   │
│   ├── sandbox/
│   │   └── docker_runner.py
│   │
│   ├── xai/
│   │   ├── diagnosis.py
│   │   └── patch_generator.py
│   │
│   └── models/
│       └── schemas.py
│
├── frontend/
│   └── dashboard.py
│
├── tests/
│
├── sample_repos/
│
├── docker/
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Current Development Status

## Phase 1 — Foundation

* [x] Project initialized
* [x] Python backend
* [x] FastAPI server
* [x] AST parser
* [x] Basic code-analysis API

## Phase 2 — Static Analysis

* [ ] Advanced AST extraction
* [ ] Function signatures
* [ ] Call relationships
* [ ] Import relationships
* [ ] Dependency graph
* [ ] Control Flow Graph

## Phase 3 — Semantic Conflict Engine

* [ ] Function signature conflicts
* [ ] Dependency conflicts
* [ ] Import conflicts
* [ ] Execution-order conflicts
* [ ] Side-effect conflicts
* [ ] Risk scoring

## Phase 4 — Multi-Agent System

* [ ] LangGraph supervisor
* [ ] Sequence Auditor
* [ ] API Contract Auditor
* [ ] Side-Effect Auditor
* [ ] Agent result aggregation

## Phase 5 — Runtime Verification

* [ ] Docker sandbox
* [ ] Dependency installation
* [ ] Unit test execution
* [ ] Integration testing
* [ ] Runtime log collection

## Phase 6 — Explainability

* [ ] Failure diagnosis
* [ ] Line-level explanations
* [ ] AST difference visualization
* [ ] Runtime trace explanation
* [ ] Patch generation

## Phase 7 — GitHub Integration

* [ ] GitHub webhook
* [ ] Pull Request analysis
* [ ] Automated status checks
* [ ] Merge approval
* [ ] Automated merge

## Phase 8 — Dashboard

* [ ] Streamlit dashboard
* [ ] Conflict visualization
* [ ] Dependency graphs
* [ ] Agent reports
* [ ] Runtime reports
* [ ] Patch viewer

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd MergeMind
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

---

# ▶️ Running the Backend

Start the FastAPI development server:

```bash
cd backend
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Current API

## `GET /`

Health check.

Response:

```json
{
  "message": "MergeMind Backend is running"
}
```

---

## `POST /parse`

Accepts Python source code and performs AST analysis.

Request:

```json
{
  "code": "def hello(name):\n    print(name)"
}
```

Response:

```json
{
  "success": true,
  "ast_analysis": {
    "imports": [],
    "functions": [
      {
        "name": "hello",
        "line": 1,
        "arguments": ["name"]
      }
    ],
    "classes": [],
    "function_calls": [
      {
        "name": "print",
        "line": 2
      }
    ],
    "variables": []
  }
}
```

---

# 🧠 Design Philosophy

MergeMind follows a layered verification strategy:

```text
             ┌──────────────────┐
             │   Static Layer   │
             │                  │
             │ AST + Graphs     │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │  Reasoning Layer │
             │                  │
             │ Multi-Agent AI   │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │  Dynamic Layer  │
             │                  │
             │ Docker + Tests  │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Explainability   │
             │                  │
             │ Diagnosis + Fix │
             └──────────────────┘
```

No single layer is expected to solve the entire problem.

The goal is to combine structural analysis, reasoning, execution and explanation.

---

# 🔮 Future Scope

Potential future extensions include:

* JavaScript / TypeScript support
* Java support
* C++ support
* LLM-powered code reasoning
* repository-wide impact analysis
* learned semantic conflict classifiers
* historical PR analysis
* developer-specific conflict patterns
* automatic regression-test generation
* intelligent patch validation
* IDE integration
* GitHub/GitLab/Bitbucket support

---

# 👨‍💻 Team

### MergeMind — Research & Development Team

| Member             | Role                                 |
| ------------------ | ------------------------------------ |
| **Saaransh Johri** | Backend & Static Analysis            |
| **Aditya**         | Multi-Agent AI System                |
| **Vinit**          | Runtime Sandbox & GitHub Integration |
| **Sayali**         | Dashboard, Visualization & XAI       |

---

# 📜 Project Status

> 🚧 **MergeMind is currently under active development.**

The current implementation focuses on establishing the Python backend and AST-based source-code analysis pipeline. More advanced semantic analysis, agentic auditing, runtime verification, explainability and GitHub automation are being developed incrementally.

---

# ⭐ Vision

Merge conflicts should not be treated as purely textual problems.

Software is a system of:

```text
Functions
   +
Dependencies
   +
State
   +
Execution
   +
Contracts
   +
Side Effects
```

MergeMind aims to make version-control systems **reason about software behaviour**, not merely differences in text.

> **Don't just ask whether two branches can be merged.**
>
> **Ask whether the software can survive the merge.**

---

## Built with

Python • FastAPI • AST • Tree-sitter • NetworkX • LangGraph • LLMs • Docker • GitHub • Streamlit

---
