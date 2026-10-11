import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Executive Digital Invoicing Dashboard",
    page_icon="🎨",
    layout="wide"
)

# Initialize Session State for Audit History Log
if 'invoice_history' not in st.session_state:
    st.session_state.invoice_history = []

# Custom CSS for Colorful Digital Dashboard Styling
st.markdown("""
    <style>
    .dash-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .dash-header h1 {
        color: #ffffff;
        font-size: 30px;
        margin-bottom: 8px;
    }
    .dash-header p {
        color: #b0bec5;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f3f6;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #203a43 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard Banner
st.markdown("""
    <div class="dash-header">
        <h1>🎨 Executive Digital Invoicing Dashboard & Audit Trail</h1>
        <p>Advanced Corporate Billing, Filter Parameters, Manual Invoices & Real-Time Activity Tracking</p>
    </div>
""", unsafe_allow_html=True)

# Top Metrics Counters Row
total_generated = len(st.session_state.invoice_history)
m1, m2, m3, m4 = st.columns(4)
m1.metric("📊 Generated Batches", str(total_generated), "Live Tracked")
m2.metric("🏢 Formats Available", "3 Templates", "Ready")
m3.metric("⚡ Processing Mode", "Real-Time", "1-Click")
m4.metric("🛡️ System Status", "Online & Secure", "Logged")

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs: Dashboard vs Audit Log
tab1, tab2 = st.tabs(["⚡ Invoicing Dashboard", "📜 Activity Audit Log & History"])

with tab1:
    # ================= 1. OPERATOR & FILTER SECTION =================
    with st.container(border=True):
        st.markdown("### 👤 Operator & Filter Parameters")
        op_col1, op_col2 = st.columns(2)
        with op_col1:
            operator_name = st.text_input("👨‍💼 Operator / User Name:", placeholder="e.g. Moise / Billing Officer")
        with op_col2:
            client_search = st.text_input("🏢 Target Client / Reference:", placeholder="e.g. ABC Corp / Specific ID")

        st.markdown("---")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            start_date = st.date_input("Start Date", value=datetime(2022, 12, 1))
        with f2:
            end_date = st.date_input("End Date", value=datetime(2022, 12, 30))
        with f3:
            ntn_input = st.text_input("NTN Number", placeholder="e.g. 0711579")
        with f4:
            dept_id = st.text_input("Department ID", placeholder="Dept ID")

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= 2. IMPORT, FORMAT & CHECKLISTS =================
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        with st.container(border=True):
            st.markdown("### 📥 Import & Layouts")
            uploaded_file = st.file_uploader("Upload Raw Excel / Mobile Numbers", type=["xlsx", "xls", "csv"])
            st.markdown("<small style='color: gray;'>Mobile numbers and bill details will be populated via import option.</small>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🎨 Select Bill Format")
            selected_format = st.radio("Choose Corporate Template:", ["Format 1 (Standard)", "Format 2 (Detailed)", "Format 3 (Executive)"])

    with col_right:
        with st.container(border=True):
            st.markdown("### ☑️ Required Bill Fields (Checklists)")
            st.markdown("Select fields to include in the generated invoice:")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                chk_mobile = st.checkbox("Mobile Number", value=True)
                chk_sub = st.checkbox("Subscriber Name", value=True)
                chk_comp = st.checkbox("Company Customer Name", value=True)
                chk_plan = st.checkbox("Plan Name")
                chk_act = st.checkbox("Activation Date")
                chk_status = st.checkbox("Subscriber Status")
            with c2:
                chk_month = st.checkbox("Bill Month", value=True)
                chk_rent = st.checkbox("Line Rent", value=True)
                chk_gprs = st.checkbox("GPRS / Blackberry")
                chk_sms = st.checkbox("SMS / Voice Bundle")
                chk_vas = st.checkbox("VAS")
                chk_usage = st.checkbox("Usage Bill", value=True)
                chk_total_bill = st.checkbox("Total Bill Amount", value=True)
            with c3:
                chk_lr_disc = st.checkbox("Line Rent Discount")
                chk_promo = st.checkbox("Billing Discount", value=True)
                chk_adj = st.checkbox("Adjustment")
                chk_fed = st.checkbox("FED (Sales Tax)", value=True)
                chk_ait = st.checkbox("AIT")
                chk_payable = st.checkbox("Payable", value=True)
                chk_prev = st.checkbox("Previous Outstanding")
                chk_pay = st.checkbox("Payments")
                chk_tot_pay = st.checkbox("Total Payable", value=True)
                chk_inv_id = st.checkbox("Invoice ID", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= 3. PREVIEW & GENERATION SECTION =================
    st.markdown("### 📊 Populated Bill Information & Preview Sheet")

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        with st.container(border=True):
            st.success(f"✨ File loaded successfully! Active Template: **{selected_format}**")
            st.markdown(f"**Billing Cycle:** `{start_date}` to `{end_date}` | **NTN:** `{ntn_input or 'All'}` | **Dept ID:** `{dept_id or 'All'}`")
            st.markdown("---")
            
            st.markdown("#### 📄 Live Preview Data Table:")
            st.dataframe(df, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Registration & Generation Button
        if st.button("⚡ Register & Generate Official Invoice Batch", type="primary", use_container_width=True):
            if not operator_name.strip():
                st.warning("⚠️ Please enter the Operator / User Name before generating the invoice.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                filename = f"Manual_Invoice_{selected_format.split()[0]}_{start_date}_to_{end_date}.csv"
                
                # Save record to session state history
                st.session_state.invoice_history.append({
                    "Timestamp": timestamp,
                    "Operator": operator_name,
                    "Template": selected_format,
                    "Client_Ref": client_search or "General Batch",
                    "Billing_Period": f"{start_date} to {end_date}",
                    "File_Name": filename,
                    "Total_Records": len(df)
                })
                st.success(f"✅ Invoice batch successfully processed and logged by **{operator_name}** at `{timestamp}`!")
        
        # Download Final Sheet
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Final Populated Bill Sheet (Excel/CSV)",
            data=csv_data,
            file_name=f"Manual_Invoice_{selected_format.split()[0]}_{start_date}_to_{end_date}.csv",
            mime="text/csv",
            type="secondary",
            use_container_width=True
        )
    else:
        with st.container(border=True):
            st.info("💡 **Awaiting Data:** Please upload your raw Excel file or mobile numbers list using the **Import** section above to view and generate the populated bills.")

with tab2:
    st.markdown("### 📜 System Activity & Invoice Audit Trail")
    st.markdown("Complete log showing who generated which invoice, which template was used, and exact timestamps.")
    
    if len(st.session_state.invoice_history) > 0:
        history_df = pd.DataFrame(st.session_state.invoice_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        # Download Audit Log
        log_csv = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete Audit Log Report (CSV)",
            data=log_csv,
            file_name="Invoice_Audit_Trail_Report.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("ℹ️ No invoices generated yet in this session. Once you generate an invoice, its complete record (Operator name, timestamp, template, etc.) will appear here automatically.")
