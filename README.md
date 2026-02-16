# Deduction Detective

3-layer LangGraph agent that audits deduction claims (Ingest → Audit Logic → Human Gate → Action) using GPT-4o and `interrupt_before` for human review.

## Setup

1. **Create a virtual environment (recommended):**
   ```bash
   cd 05_Deductions_Detector
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Ensure `.env` exists with `OPENAI_API_KEY=your-key`.
   - Or export: `export OPENAI_API_KEY=your-key`

## How to Run the First Audit

From the project root (or from `05_Deductions_Detector` if you have a run script there):

```bash
cd 05_Deductions_Detector
python main.py
```

### What Happens

1. **Ingest (Node A)**  
   Simulates ingesting a $5,000 Walmart claim for "Late Delivery" and sets `contract_text` (48-hour grace period).

2. **Audit Logic (Node B)**  
   GPT-4o compares the claim to the rule: *"Shipments have a 48-hour grace period."*  
   The claim is 12 hours late → within grace → **violation_found = False** and `evidence` is set.

3. **Human Gate (Node C)**  
   Execution **pauses before** this node (`interrupt_before=["human_gate"]`).  
   You see the state (claim_id, retailer, amount, violation_found, evidence).  
   The script then **resumes** with `human_approved: True`.

4. **Action (Node D)**  
   If `human_approved` is True, it prints **"Dispute Filed Successfully"**.

### Running Step-by-Step (e.g. in a REPL)

To run the graph manually and resume after human review:

```python
from main import build_graph

graph = build_graph()
config = {"configurable": {"thread_id": "my-audit-1"}}

# Run until pause before human_gate
result = graph.invoke({}, config=config)
print(result)  # review state here

# Resume with human decision
final = graph.invoke({"human_approved": True}, config=config)
```

## Files

| File           | Purpose |
|----------------|--------|
| `schema.py`    | `DeductionState` TypedDict (claim_id, retailer, amount, contract_text, violation_found, evidence, human_approved). |
| `main.py`      | Graph definition, nodes (ingest, audit, human_gate, action), `MemorySaver` checkpointer, and `run_first_audit()`. |
| `requirements.txt` | Dependencies (langgraph, langchain-openai, langchain-core, python-dotenv). |

## Technical Notes

- **Persistence:** `MemorySaver()` is used for checkpointing; state is in-memory and lost when the process exits (use a DB-backed checkpointer for production).
- **Human gate:** `interrupt_before=["human_gate"]` pauses before the human_gate node; resume with the same `thread_id` and pass `human_approved` in the invoke payload (or use `update_state` if your LangGraph version supports it).
