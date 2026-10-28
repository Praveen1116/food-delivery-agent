# Food Delivery Help Desk Agent

A lightweight, production-style implementation of **Agentic AI Design Patterns** for a Food Delivery Help Desk, built using the **Microsoft Agent Framework** and Groq's high-speed LLM inference.

This project implements two core multi-agent architectures:
1. **The Manager Pattern (Task 1)**: Dynamic intent routing where a manager agent inspects tickets and dispatches them to domain-specific worker agents wrapped as tools (`as_tool`).
2. **The Blackboard Pattern (Task 2)**: Decentralized state sharing where autonomous workflow nodes read, update, and persist notes onto a shared blackboard without point-to-point message coupling.

---

## Architecture Overview

### 1. Manager Pattern (Task 1)
Instead of brittle keyword-based routing, an LLM-based Manager evaluates the semantics of a ticket and calls the appropriate specialist worker.

```
                  +-------------------------+
                  |     Customer Ticket     |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |      Manager Agent      |
                  +------------+------------+
                               |
             Tool Calling (function_call inspection)
                               |
             +-----------------+-----------------+
             |                                   |
             v                                   v
   +-------------------+               +-------------------+
   |  delivery_agent   |               |   payment_agent   |
   |   (ask_delivery)  |               |   (ask_payment)   |
   +-------------------+               +-------------------+
```

### 2. Blackboard Pattern (Task 2)
Agents collaborate asynchronously through a shared state (`ctx.set_state` / `ctx.get_state`) adhering strictly to the **Read → Add → Write** principle to prevent state clobbering.

```
   +-------------------------------------------------------------+
   |                       SHARED BLACKBOARD                     |
   |  ticket: "I have a nut allergy and my salad had peanuts..."  |
   |  notes:  ["allergy: ALLERGY"]                               |
   +-------------------------------------------------------------+
            ^                               ^
            | (Read & Append)               | (Read & Display)
            |                               |
     +--------------+                +--------------+
     | allergy_step | -------------> | summary_step |
     +--------------+                +--------------+
```

---

## Project Structure

```text
food-delivery-agent/
├── tasks/
│   ├── task1_manager.py           # Task 1: Manager & worker agents via as_tool
│   └── task2_blackboard.py        # Task 2: Blackboard workflow (start -> allergy -> summary)
├── notebooks/
│   └── food_delivery_helpdesk.ipynb # Interactive notebook for local experimentation
├── reference/
│   └── Manager_and_BlackBoard.ipynb # Reference implementation guide
├── main.py                        # Unified entrypoint running both tasks
├── requirements.txt               # Pinned minimal dependencies
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules for virtualenvs and secrets
└── README.md                      # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- A Groq API key ([console.groq.com/keys](https://console.groq.com/keys))

### Installation

1. **Clone the repository & navigate to workspace**:
   ```bash
   git clone <repo-url>
   cd food-delivery-agent
   ```

2. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy the example environment file and add your Groq API key:
   ```bash
   cp .env.example .env
   ```
   In `.env`:
   ```env
   GROQ_API_KEY="gsk_..."
   ```

---

## Running the Tasks

### Option A: Run Unified Script
Run both Task 1 and Task 2 sequentially:
```bash
python main.py
```

### Option B: Run Standalone Tasks
Run tasks individually from the command line:

```bash
# Task 1: Manager
python tasks/task1_manager.py

# Task 2: Blackboard
python tasks/task2_blackboard.py
```

### Option C: Interactive Jupyter Notebook
Open [`notebooks/food_delivery_helpdesk.ipynb`](notebooks/food_delivery_helpdesk.ipynb) in VS Code or JupyterLab. Select the `.venv` Python kernel to execute each step interactively with top-level `await`.

---

## Test Cases & Verification

### Task 1: Manager Routing
- **Input Ticket:** `"My food showed up an hour after the promised time"`
- **Specialists Available:** `ask_delivery`, `ask_payment`
- **Output:**
  ```text
  Task 1: ['ask_delivery']
  ```

### Task 2: Blackboard State Propagation
- **Input Ticket:** `"I have a nut allergy and my salad had peanuts in it!"`
- **Workflow:** `start` → `allergy_step` → `summary_step`
- **Output:**
  ```text
  Ticket: I have a nut allergy and my salad had peanuts in it!
  Notes: allergy: ALLERGY
  ```

---

## Key Design Principles

1. **Explicit Tool Descriptions**:
   Tool calling accuracy depends heavily on semantic clarity. The tool descriptions for `ask_delivery` and `ask_payment` provide distinct boundaries so the manager accurately delegates delivery delays versus billing disputes.

2. **Blackboard Concurrency Safety**:
   In `allergy_step`, the agent always fetches the current notes list before appending its own entry:
   ```python
   notes = ctx.get_state("notes")            # 1. READ
   notes = notes + ["allergy: " + answer]    # 2. ADD
   ctx.set_state("notes", notes)             # 3. WRITE
   ```
   This prevents state overwrites across multi-step or concurrent workflows.

3. **Zero Bloat**:
   Built cleanly on `agent-framework-core` and `agent-framework-openai` using Groq's OpenAI-compatible endpoint, minimizing package overhead while preserving type safety and asynchronous execution.
# Food Delivery Help Desk Agent

A lightweight, production-style implementation of **Agentic AI Design Patterns** for a Food Delivery Help Desk, built using the **Microsoft Agent Framework** and Groq's high-speed LLM inference.

This project implements two core multi-agent architectures:
1. **The Manager Pattern (Task 1)**: Dynamic intent routing where a manager agent inspects tickets and dispatches them to domain-specific worker agents wrapped as tools (`as_tool`).
2. **The Blackboard Pattern (Task 2)**: Decentralized state sharing where autonomous workflow nodes read, update, and persist notes onto a shared blackboard without point-to-point message coupling.

---

## Architecture Overview

### 1. Manager Pattern (Task 1)
Instead of brittle keyword-based routing, an LLM-based Manager evaluates the semantics of a ticket and calls the appropriate specialist worker.

```
                  +-------------------------+
                  |     Customer Ticket     |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |      Manager Agent      |
                  +------------+------------+
                               |
             Tool Calling (function_call inspection)
                               |
             +-----------------+-----------------+
             |                                   |
             v                                   v
   +-------------------+               +-------------------+
   |  delivery_agent   |               |   payment_agent   |
   |   (ask_delivery)  |               |   (ask_payment)   |
   +-------------------+               +-------------------+
```

### 2. Blackboard Pattern (Task 2)
Agents collaborate asynchronously through a shared state (`ctx.set_state` / `ctx.get_state`) adhering strictly to the **Read → Add → Write** principle to prevent state clobbering.

```
   +-------------------------------------------------------------+
   |                       SHARED BLACKBOARD                     |
   |  ticket: "I have a nut allergy and my salad had peanuts..."  |
   |  notes:  ["allergy: ALLERGY"]                               |
   +-------------------------------------------------------------+
            ^                               ^
            | (Read & Append)               | (Read & Display)
            |                               |
     +--------------+                +--------------+
     | allergy_step | -------------> | summary_step |
     +--------------+                +--------------+
```

---

## Project Structure

```text
food-delivery-agent/
├── tasks/
│   ├── task1_manager.py           # Task 1: Manager & worker agents via as_tool
│   └── task2_blackboard.py        # Task 2: Blackboard workflow (start -> allergy -> summary)
├── notebooks/
│   └── food_delivery_helpdesk.ipynb # Interactive notebook for local experimentation
├── reference/
│   └── Manager_and_BlackBoard.ipynb # Reference implementation guide
├── main.py                        # Unified entrypoint running both tasks
├── requirements.txt               # Pinned minimal dependencies
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules for virtualenvs and secrets
└── README.md                      # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- A Groq API key ([console.groq.com/keys](https://console.groq.com/keys))

### Installation

1. **Clone the repository & navigate to workspace**:
   ```bash
   git clone <repo-url>
   cd food-delivery-agent
   ```

2. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy the example environment file and add your Groq API key:
   ```bash
   cp .env.example .env
   ```
   In `.env`:
   ```env
   GROQ_API_KEY="gsk_..."
   ```

---

## Running the Tasks

### Option A: Run Unified Script
Run both Task 1 and Task 2 sequentially:
```bash
python main.py
```

### Option B: Run Standalone Tasks
Run tasks individually from the command line:

```bash
# Task 1: Manager
python tasks/task1_manager.py

# Task 2: Blackboard
python tasks/task2_blackboard.py
```

### Option C: Interactive Jupyter Notebook
Open [`notebooks/food_delivery_helpdesk.ipynb`](notebooks/food_delivery_helpdesk.ipynb) in VS Code or JupyterLab. Select the `.venv` Python kernel to execute each step interactively with top-level `await`.

---

## Test Cases & Verification

### Task 1: Manager Routing
- **Input Ticket:** `"My food showed up an hour after the promised time"`
- **Specialists Available:** `ask_delivery`, `ask_payment`
- **Output:**
  ```text
  Task 1: ['ask_delivery']
  ```

### Task 2: Blackboard State Propagation
- **Input Ticket:** `"I have a nut allergy and my salad had peanuts in it!"`
- **Workflow:** `start` → `allergy_step` → `summary_step`
- **Output:**
  ```text
  Ticket: I have a nut allergy and my salad had peanuts in it!
  Notes: allergy: ALLERGY
  ```

---

## Key Design Principles

1. **Explicit Tool Descriptions**:
   Tool calling accuracy depends heavily on semantic clarity. The tool descriptions for `ask_delivery` and `ask_payment` provide distinct boundaries so the manager accurately delegates delivery delays versus billing disputes.

2. **Blackboard Concurrency Safety**:
   In `allergy_step`, the agent always fetches the current notes list before appending its own entry:
   ```python
   notes = ctx.get_state("notes")            # 1. READ
   notes = notes + ["allergy: " + answer]    # 2. ADD
   ctx.set_state("notes", notes)             # 3. WRITE
   ```
   This prevents state overwrites across multi-step or concurrent workflows.

3. **Zero Bloat**:
   Built cleanly on `agent-framework-core` and `agent-framework-openai` using Groq's OpenAI-compatible endpoint, minimizing package overhead while preserving type safety and asynchronous execution.
