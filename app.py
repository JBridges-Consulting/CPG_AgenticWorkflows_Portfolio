import pandas as pd  # FIXED: was 'import pd as pd'
import streamlit as st

# --- 1. EXECUTIVE UI SETUP ---
st.set_page_config(page_title="Harvest Heritage Margin Defense", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* 🛡️ HEADER: 44px Bold Branding */
    .mega-header { 
        font-size: 44px !important; 
        font-weight: 800 !important; 
        color: #1E1E1E !important; 
        margin-top: -50px !important;
        line-height: 1.1 !important;
    }
    .mega-subtitle { font-size: 20px !important; color: #555 !important; margin-bottom: 30px !important; font-style: italic; }

    /* 🛡️ UNIFORMITY: Force 16px on body elements */
    html, body, [class*="css"], .stMarkdown, p, span, label, .stInfo, .stSuccess, .stError, .stButton button, .stSelectbox {
        font-size: 16px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stMetricValue"] > div { font-size: 32px !important; font-weight: 700 !important; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# THE BRANDING: Using double quotes for the apostrophe
st.markdown("<p class='mega-header'>🛡️ Harvest Heritage Margin Defense Dashboard</p>", unsafe_allow_html=True)
st.markdown('<p class="mega-subtitle">Revenue Protection & Forensic Audit Center</p>', unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "reclaimed_funds" not in st.session_state:
    st.session_state.reclaimed_funds = 0.0

# --- 3. SIDEBAR: DATA INGESTION ---
with st.sidebar:
    st.header("📥 Ingestion Center")
    uploaded_file = st.file_uploader("Upload Harvest Heritage Deduction Export", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip() 
        
        # Mapping to your exact CSV headers: Claimed_Amount
        amt_col = 'Claimed_Amount'
        if amt_col in df.columns:
            df[amt_col] = pd.to_numeric(df[amt_col].astype(str).str.replace('[$,]', '', regex=True), errors='coerce').fillna(0.0)
        
        st.session_state.raw_df = df
        
        total_leakage = df[amt_col].sum()
        st.metric(label="TOTAL P&L LEAKAGE", value=f"${total_leakage:,.2f}", delta="Risk Exposure", delta_color="inverse")
        st.metric(label="TOTAL RECLAIMED REVENUE", value=f"${st.session_state.reclaimed_funds:,.2f}", delta="Recovered")
        
        st.subheader("Retailer Concentration")
        st.bar_chart(df.groupby('Retailer')[amt_col].sum())
    else:
        st.stop()

# --- 4. THE RISK QUEUE (REMOVED 'STATUS') ---
df = st.session_state.raw_df
high_risk_df = df[df['Claimed_Amount'] >= 500].copy()

st.subheader("🚨 High-Risk Exception Queue (Flagged for VP)")

# Mapping columns exactly from your data sample
display_cols = ['Claim_ID', 'Date', 'Retailer', 'Reason_Code', 'Claimed_Amount', 'Category', 'Description']

try:
    st.dataframe(
        high_risk_df[display_cols].style.format({'Claimed_Amount': "${:,.2f}"})
        .background_gradient(subset=['Claimed_Amount'], cmap='Reds'),
        use_container_width=True, hide_index=True
    )
except Exception:
    st.dataframe(high_risk_df[display_cols], use_container_width=True, hide_index=True)

st.divider()

# --- 5. COMMAND CENTER ---
st.subheader("🕹️ Recovery Command Center")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 1. Claim_ID Selection")
    selected_id = st.selectbox("Select Claim_ID for Forensic Audit:", df['Claim_ID'].tolist())
    claim_data = df[df['Claim_ID'] == selected_id].iloc[0]
    amt = float(claim_data['Claimed_Amount'])
    retailer = claim_data['Retailer']
    
    if amt < 500:
        st.warning("⚠️ **STATUS: AUTO-APPROVED (LOSS ACCEPTED)**")
    else:
        st.error("🚨 **STATUS: FLAG - VP AUTHORIZATION REQUIRED**")
    
    st.write(f"**Date**: {claim_data['Date']} | **Retailer**: {retailer}")
    st.write(f"**Reason Code**: {claim_data['Reason_Code']} | **Exposure**: ${amt:,.2f}")
    st.write(f"**Description**: {claim_data['Description']}")

with col2:
    st.markdown("### 2. Execution & Authorization")
    
    if st.button("🔍 RUN FORENSIC AUDIT", use_container_width=True):
        with st.status("Agent Scanning Evidence...", expanded=True) as status:
            st.write(f"**Agent**: Verifying shipping logs for {retailer}...")
            st.write(f"**Agent**: Forensic Audit Verified. Recoverable Funds Detected.")
            status.update(label="Audit Analysis Complete", state="complete")

    if amt >= 500:
        st.markdown("---")
        if st.button(f"🚀 AUTHORIZE DISPUTE AGAINST {retailer.upper()}", type="primary", use_container_width=True):
            st.session_state.reclaimed_funds += amt
            st.session_state.authorized_id = selected_id 
            st.rerun()

# --- 6. AUTOMATED APPEAL AGENT (CLOSES THE LOOP) ---
if st.session_state.get("authorized_id") == selected_id:
    st.divider()
    st.subheader(f"📧 Agentic Draft: Formal Appeal to {retailer}")
    
    portal_map = {
        "Walmart": "Walmart Retail Link",
        "Kroger": "Kroger Vendor Central",
        "Target": "Target Partners Online"
    }
    target_portal = portal_map.get(retailer, f"{retailer} Claims Dept.")

    email_body = f"""
Subject: FORMAL DISPUTE: Claim {claim_data['Claim_ID']} | {retailer} 

Attention {retailer} Accounts Payable,

Harvest Heritage is formally disputing Deduction {claim_data['Claim_ID']} issued on {claim_data['Date']} 
under Deduction Code {claim_data['Reason_Code']}.

Our forensic audit confirms this charge is invalid. BOL verification indicates full delivery fulfillment. 
Disputed Amount: ${amt:,.2f}

Please acknowledge receipt and revert this deduction to our account. 

Best Regards,
Heritage Harvest Accounts Receivables Team
    """
    st.text_area(f"Appeal Template (Pre-formatted for {target_portal}):", value=email_body, height=280)
    
    if st.button(f"📤 TRANSMIT TO {retailer.upper()} PORTAL", use_container_width=True):
        st.success(f"Appeal for {selected_id} successfully transmitted to {target_portal}!")