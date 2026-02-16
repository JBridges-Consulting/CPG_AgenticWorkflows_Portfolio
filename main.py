import os
import sqlite3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# --- Agentic AI Stack Imports ---
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 🛡️ Ensure schema.py exists in your directory with DeductionState defined
from schema import DeductionState 

load_dotenv()

# --- 1. NODE LOGIC (The "Human Agent" Actions) ---

def ingest_node(state: DeductionState) -> dict:
    """Simulates the 'Perception' layer - ingesting the data."""
    print(f"--- [INGEST] Claim ID: {state.get('claim_id')} ---")
    return {"status": "INGESTED", "audit_date": datetime.now().strftime("%Y-%m-%d")}

def audit_node(state: DeductionState) -> dict:
    """The 'Reasoning' layer - forensic analysis via GPT-4o."""
    print("--- [AUDIT] Performing Forensic Reasoning ---")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = f"""
    Analyze Claim {state.get('claim_id')} (${state.get('amount')}). 
    Retailer Contract Rule: "{state.get('contract_text')}"
    Task: Identify if a 12h delay violates the 48h grace period. 
    Format: VIOLATION: [TRUE/FALSE] | REASON: [Evidence summary]
    """
    
    res = llm.invoke([HumanMessage(content=prompt)]).content
    violation = "VIOLATION: TRUE" in res.upper()
    evidence = res.split("REASON:")[-1].strip() if "REASON:" in res else res
    
    return {"violation_found": violation, "evidence": evidence}

def draft_email_node(state: DeductionState) -> dict:
    """Prepares the dispute for the retailer portal."""
    if not state.get("violation_found"): 
        print("--- [DRAFT] No violation found, skipping draft. ---")
        return {"email_draft": "N/A"}
    
    print("--- [DRAFT] Creating Dispute Documentation ---")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = f"Draft a professional dispute for {state.get('claim_id')} using evidence: {state.get('evidence')}"
    return {"email_draft": llm.invoke([HumanMessage(content=prompt)]).content}

def action_node(state: DeductionState) -> dict:
    """The 'Execution' layer - filing the claim or logging for review."""
    print("--- [ACTION] Finalizing Transaction ---")
    amount = float(state.get("amount", 0))
    is_approved = state.get("human_approved", False) or (amount < 500)
    outcome = "FILED" if is_approved else "PENDING_REVIEW"
    
    log_entry = {
        "Claim_ID": state.get('claim_id'),
        "Amount": amount,
        "Status": outcome,
        "Evidence": state.get('evidence', 'N/A')[:100],
        "Audit_Date": datetime.now().strftime("%Y-%m-%d")
    }
    pd.DataFrame([log_entry]).to_csv("audit_report.csv", mode='a', header=not os.path.exists("audit_report.csv"), index=False)
    return {"status": outcome, "human_approved": is_approved}

# --- 2. GRAPH BUILDER (The 'Agentic' Workflow) ---

builder = StateGraph(DeductionState)
builder.add_node("ingest", ingest_node)
builder.add_node("audit", audit_node)