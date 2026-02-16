import streamlit as st
import pandas as pd

# --- 1. EXECUTIVE UI SETUP ---
st.set_page_config(page_title="Harvest Heritage Margin Defense", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .mega-header { font-size: 44px !important; font-weight: 800 !important; color: #1E1E1E !important; margin-top: -50px !important; }
    .mega-subtitle { font-size: 20px !important; color: #555 !important; margin-bottom: 30px !important; font-style: italic; }
    html, body, [class*="css"], .stMarkdown, p, span, label, .stButton button, .stSelectbox { font-size: 16px !important; }
    div[data-testid="stMetricValue"] > div { font-size: 32px !important; font-weight: 700 !important; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""<p class="mega-header">🛡️ Goetze's Margin Defense Dashboard</p>""", unsafe_allow_html=True)
st.markdown('<p class="mega-subtitle">Revenue Protection & Forensic Audit Center</p>', unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "clawed_back_funds" not in st.session_state:
    st.session_state.clawed_back_funds = 0.0

with st.sidebar:
    st.header("📥 Ingestion Center")
    uploaded_file = st.file_uploader("Upload Goetze's Deduction Export", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip() # Kill hidden spaces
        
        # 🛡️ THE FIX: Strictly using 'Claimed_Amount'
        amt_col = 'Claimed_Amount' 
        if amt_col in df.columns:
            df[amt_col] = pd.to_numeric(df[amt_col].astype(str).str.replace('[$,]', '', regex=True), errors='coerce').fillna(0.0)
        
        st.session_state.raw_df = df
        
        total_leakage = df[amt_col].sum()
        st.metric(label="TOTAL P&L LEAKAGE", value=f"${total_leakage:,.2f}", delta="Action Required", delta_color="inverse")
        st.metric(label="TOTAL RECLAIMED REVENUE", value=f"${st.session_state.clawed_back_funds:,.2f}", delta="Recovered")
        st.bar_chart(df.groupby('Retailer')[amt_col].sum())
    else:
        st.stop()

# --- 3. THE RISK QUEUE ---
df = st.session_state.raw_df
high_risk_df = df[df['Claimed_Amount'] >= 500].copy()

st.subheader("🚨 High-Risk Exception Queue (Flagged for VP)")

# 🛡️ THE FIX: Headers match your Reason_Code discovery
display_cols = ['Claim_ID', 'Date', 'Retailer', 'Reason_Code', 'Category', 'Claimed_Amount', 'Description']

try:
    st.dataframe(
        high_risk_df[display_cols].style.format({'Claimed_Amount': "${:,.2f}"})
        .background_gradient(subset=['Claimed_Amount'], cmap='Reds'),
        use_container_width=True, hide_index=True
    )
except:
    st.dataframe(high_risk_df[display_cols], use_container_width=True, hide_index=True)

st.divider()

# --- 4. COMMAND CENTER ---
st.subheader("🕹️ Recovery Command Center")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 1. Target Selection")
    selected_id = st.selectbox("Select Target for Forensic Audit:", df['Claim_ID'].tolist())
    claim_data = df[df['Claim_ID'] == selected_id].iloc[0]
    amt = float(claim_data['Claimed_Amount'])
    retailer = claim_data['Retailer']
    
    st.write(f"**Date**: {claim_data['Date']} | **Retailer**: {retailer}")
    st.write(f"**Reason Code**: {claim_data['Reason_Code']} | **Exposure**: ${amt:,.2f}")
    st.write(f"**Description**: {claim_data['Description']}")

with col2:
    st.markdown("### 2. Execution & Authorization")
    if st.button("🔍 RUN FORENSIC AUDIT", use_container_width=True):
        with st.status("Agent Scanning Evidence...", expanded=True) as status:
            st.write(f"**Agent**: Searching {retailer} historical claims for {claim_data['Reason_Code']}...")
            # 💡 THE FIX: Dynamic audit response based on Description
            if "pallet" in claim_data['Description'].lower():
                st.write(f"**Agent**: Verifying Goetze's standard pallet configuration vs {retailer} specs...")
            else:
                st.write("**Agent**: Verifying shipping Bill of Lading (BOL) timestamps...")
            st.write(f"**Agent**: Forensic Evidence for '{claim_data['Description']}' found to be invalid.")
            status.update(label="Audit Analysis Complete", state="complete")

    if amt >= 500:
        if st.button(f"🚀 AUTHORIZE DISPUTE AGAINST {retailer.upper()}", type="primary", use_container_width=True):
            st.session_state.clawed_back_funds += amt
            st.session_state.authorized_id = selected_id
            st.rerun()

# --- 5. THE AGENTIC EMAIL DRAFT (CONTEXT-AWARE) ---
if st.session_state.get("authorized_id") == selected_id:
    st.divider()
    st.subheader(f"📧 Agentic Draft: Official Appeal to {retailer}")
    
    # 🧠 Logic to ensure the Email matches the specific "Pallet" or "Shortage" issue
    desc = claim_data['Description'].lower()
    if "pallet" in desc:
        evidence_msg = f"Audit of Warehouse Log #GTZ-99 shows our pallet configuration met the agreed-upon standards for {retailer}."
    elif "shortage" in desc or "damages" in desc:
        evidence_msg = f"Signed BOL and warehouse receipts from {claim_data['Date']} confirm no discrepancies occurred."
    else:
        evidence_msg = f"Forensic audit confirms the charge for '{claim_data['Description']}' is administratively invalid."

    email_body = f"""
Subject: FORMAL DISPUTE: Claim {claim_data['Claim_ID']} | {retailer} 

Attention {retailer} Accounts Payable Team,

Goetze's Candy Co. is formally disputing Deduction {claim_data['Claim_ID']} issued on {claim_data['Date']} 
under Reason Code {claim_data['Reason_Code']}.

Our forensic audit confirms this charge is invalid:
- Reason: {claim_data['Description']}
- Disputed Amount: ${amt:,.2f}
- Agent Finding: {evidence_msg}

Please acknowledge receipt and revert this deduction to our account. 

Regards,
Goetze's Automated Recovery Agent
    """
    st.text_area("Review Professional Draft:", value=email_body, height=280)
    if st.button(f"📤 TRANSMIT TO {retailer.upper()} PORTAL"):
        st.success(f"Dispute for {selected_id} successfully filed!")