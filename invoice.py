import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Executive Digital Invoicing & Approvals",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Session States for History and Approvals
if 'invoice_history' not in st.session_state:
    st.session_state.invoice_history = []
if 'approval_queue' not in st.session_state:
    st.session_state.approval_queue = []

# Custom CSS Styling
st.markdown("""
    <style>
    .dash-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    .dash-header h1 { color: white; font-size: 28px; margin-bottom: 5px; }
    .dash-header p { color: #e0e0e0; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("""
    <div class="dash-header">
        <h1>🛡️ Corporate Invoicing Portal with Admin Approvals</h1>
        <p>Secure Billing, Role-Based Access & Automated Amount Modification Workflow</p>
    </div>
""", unsafe_allow_html=True)

# ================= SIDEBAR: USER ROLE & AUTHENTICATION =================
st.sidebar.markdown("### 🔐 Access Control")
user_role = st.sidebar.selectbox("Select User Role:", ["Operator", "Administrator"])
operator_name = st.sidebar.text_input("Operator / Admin Name:", value="Moise")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Role:** `{user_role}`")
if user_role == "Administrator":
    st.sidebar.success("🛡️ Admin Rights Active: You can approve/reject modified invoices.")
else:
    st.sidebar.info("👤 Operator Mode: Amount changes will require Admin approval.")

# Navigation Tabs based on Role
if user_role == "Administrator":
    tab1, tab2, tab3 = st.tabs(["⚡ Invoicing Dashboard", "🛡️ Admin Approvals Queue", "📜 Audit Trail & Logs"])
else:
    tab1, tab3 = st.tabs(["⚡ Invoicing Dashboard", "📜 Audit Trail & Logs"])

# ================= TAB 1: INVOICING DASHBOARD =================
with tab1:
    with st.container(border=True):
        st.markdown("### 🔍 Filter & Billing Parameters")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            start_date = st.date_input("Start Date", value=datetime(2022, 12, 1))
        with f2:
            end_date = st.date_input("End Date", value=datetime(2022, 12, 30))
        with f3:
            ntn_input = st.text_input("NTN Number", placeholder="e.g. 0711579")
        with f4:
            dept_id = st.text_input("Department ID", placeholder="Dept ID")

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        with st.container(border=True):
            st.markdown("### 📥 Import & Layouts")
            uploaded_file = st.file_uploader("Upload Raw Excel / Mobile Numbers", type=["xlsx", "xls", "csv"])
            selected_format = st.radio("Choose Corporate Template:", ["Format 1 (Standard)", "Format 2 (Detailed)", "Format 3 (Executive)"])

    with col_right:
        with st.container(border=True):
            st.markdown("### ✏️ Amount Modification & Checklists")
            st.markdown("If you modify standard amounts below differently from raw data, it will trigger an **Approval Request**.")
            
            # Manual Amount Overrides (To test modification logic)
            override_check = st.checkbox("⚠️ Override / Modify Total Bill Amount manually?")
            modified_amount = 0.0
            if override_check:
                modified_amount = st.number_input("Enter Modified Total Bill Amount (Rs.)", min_value=0.0, value=25000.0, step=500.0)

            st.markdown("---")
            st.markdown("Select fields to include in the invoice:")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.checkbox("Mobile Number", value=True)
                st.checkbox("Subscriber Name", value=True)
            with c2:
                st.checkbox("Bill Month", value=True)
                st.checkbox("Line Rent", value=True)
            with c3:
                st.checkbox("Total Payable", value=True)
                st.checkbox("Invoice ID", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        with st.container(border=True):
            st.success(f"✨ File loaded successfully! Active Template: **{selected_format}**")
            st.dataframe(df.head(), use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Process & Submit Invoice", type="primary", use_container_width=True):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if override_check:
                # Amount is changed/modified -> Send to Approval Queue
                approval_id = f"APP-{len(st.session_state.approval_queue) + 101}"
                st.session_state.approval_queue.append({
                    "Approval_ID": approval_id,
                    "Operator": operator_name,
                    "Template": selected_format,
                    "Modified_Amount": modified_amount,
                    "Status": "Pending Approval",
                    "Timestamp": timestamp
                })
                st.warning(f"⚠️ **Amount modified!** Request `{approval_id}` has been sent to Administrator for approval.")
            else:
                # Normal flow -> Direct Log
                st.session_state.invoice_history.append({
                    "Timestamp": timestamp,
                    "Operator": operator_name,
                    "Template": selected_format,
                    "Status": "Approved / Direct",
                    "Amount": "Standard Raw Data"
                })
                st.success(f"✅ Invoice successfully generated and logged by **{operator_name}**!")
    else:
        st.info("💡 Please upload your raw Excel file using the import option above.")

# ================= TAB 2: ADMIN APPROVALS QUEUE (Admin Only) =================
if user_role == "Administrator":
    with tab2:
        st.markdown("### 🛡️ Pending Invoice Amount Approvals")
        st.markdown("Review invoices where amounts were modified by operators and take action.")
        
        pending_items = [item for item in st.session_state.approval_queue if item["Status"] == "Pending Approval"]
        
        if len(pending_items) > 0:
            for idx, item in enumerate(pending_items):
                with st.container(border=True):
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    with col_a:
                        st.markdown(f"**Approval ID:** `{item['Approval_ID']}`")
                        st.markdown(f"**Operator:** `{item['Operator']}`")
                        st.markdown(f"**Template:** `{item['Template']}`")
                    with col_b:
                        st.markdown(f"**Modified Amount:** `Rs. {item['Modified_Amount']:,.2f}`")
                        st.markdown(f"**Requested At:** `{item['Timestamp']}`")
                        st.markdown(f"**Status:** 🟡 `{item['Status']}`")
                    with col_c:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("✅ Approve", key=f"app_{idx}"):
                            item["Status"] = "Approved"
                            st.session_state.invoice_history.append({
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Operator": f"{item['Operator']} (Approved by Admin: {operator_name})",
                                "Template": item['Template'],
                                "Status": "Approved via Workflow",
                                "Amount": item['Modified_Amount']
                            })
                            st.rerun()
                        if st.button("❌ Reject", key=f"rej_{idx}"):
                            item["Status"] = "Rejected"
                            st.rerun()
        else:
            st.info("✅ No pending approval requests right now.")
            
        st.markdown("#### 📋 Complete Approval History")
        if len(st.session_state.approval_queue) > 0:
            st.dataframe(pd.DataFrame(st.session_state.approval_queue), use_container_width=True, hide_index=True)

# ================= TAB 3: AUDIT TRAIL & LOGS =================
with tab3:
    st.markdown("### 📜 System Activity & Invoice Audit Trail")
    st.markdown("Complete log showing generated invoices, operator actions, and approval history.")
    
    if len(st.session_state.invoice_history) > 0:
        history_df = pd.DataFrame(st.session_state.invoice_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        csv_log = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete Audit Report (CSV)",
            data=csv_log,
            file_name="Invoice_Audit_Trail_Report.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("ℹ️ No records found in the audit trail yet.")
