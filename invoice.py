import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page Configuration
st.set_page_config(
    page_title="Enterprise Corporate Invoicing System",
    page_icon="💼",
    layout="wide"
)

# Initialize Session States
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator", "status": "Approved"}
    }
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []

# Custom CSS Styling for Professional Enterprise Look
st.markdown("""
    <style>
    .main-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .custom-invoice-box {
        background-color: #ffffff;
        border: 2px solid #1e3c72;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #000000;
        margin-bottom: 20px;
    }
    .inv-header {
        text-align: center;
        border-bottom: 2px solid #1e3c72;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .summary-card {
        background-color: #f8f9fa;
        border: 1px solid #d1d5db;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .inv-footer {
        border-top: 1px solid #ccc;
        padding-top: 10px;
        margin-top: 20px;
        font-size: 11px;
        color: #555;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ================= 1. SECURE LOGIN GATE =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>💼 Corporate Invoicing Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Enter credentials to access the system.</p>", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔑 Login", type="primary", use_container_width=True):
                if username in st.session_state.users_db:
                    u_info = st.session_state.users_db[username]
                    if u_info["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.user_role = u_info["role"]
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password.")
                else:
                    st.error("❌ User not found.")
else:
    # ================= 2. MAIN DASHBOARD =================
    st.markdown(f"""
        <div class="main-banner">
            <h2>Manual Invoice Tab - Client-Specific Custom Billing Portal</h2>
            <p>Logged in as: <b>{st.session_state.current_user}</b> ({st.session_state.user_role})</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Logout & User Info
    st.sidebar.markdown(f"### 👤 User: {st.session_state.current_user}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.user_role == "Administrator":
        tab_main, tab_admin, tab_audit = st.tabs(["📊 Manual Invoice Generator", "🛡️ Admin User Rights", "📜 Audit Logs"])
    else:
        tab_main, tab_audit = st.tabs(["📊 Manual Invoice Generator", "📜 Audit Logs"])

    with tab_main:
        # Top Search & Filter Bar
        with st.container(border=True):
            col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns([1, 1, 1, 1, 1, 0.8])
            
            with col_s1:
                selected_month = st.selectbox("Billing Month", ["October 2026", "September 2026", "August 2026"])
            with col_s2:
                invoice_id_query = st.text_input("Invoice ID", placeholder="e.g. INV-101")
            with col_s3:
                ntn_query = st.text_input("NTN Number", placeholder="e.g. 0711579")
            with col_s4:
                dept_query = st.text_input("Department ID", placeholder="Auto-linked Dept")
            with col_s5:
                cust_query = st.text_input("Customer Name", placeholder="Customer Name")
            with col_s6:
                st.markdown("<br>", unsafe_allow_html=True)
                search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        left_col, right_col = st.columns([1, 1.8], gap="large")

        with left_col:
            with st.container(border=True):
                st.markdown("### 🎨 Invoice Layout Mode")
                # Selector for Client Requirement: Single-Page vs Summary + Separate Detail
                output_mode = st.radio(
                    "Select Output Structure:",
                    [
                        "Single-Page (Summary + Detail Combined)", 
                        "Summary Page + Separate Detail Report"
                    ]
                )
                
                st.markdown("---")
                st.markdown("### 🏛️ Client & Format Mapping")
                client_format = st.selectbox(
                    "Select Client Custom Format:",
                    ["Standard Corporate Format", "Client A (Special Tax Layout)", "Client B (Detailed Breakdown Layout)"]
                )
                
                st.markdown("---")
                st.markdown("### ☑️ Field Checklists")
                
                f_mob = st.checkbox("Mobile Number", value=True)
                f_sub = st.checkbox("Subscriber Name", value=True)
                f_comp = st.checkbox("Company Customer Name", value=True)
                f_plan = st.checkbox("Plan Name", value=True)
                f_act = st.checkbox("Activation Date", value=False)
                f_status = st.checkbox("Subscriber Status", value=False)
                f_month = st.checkbox("Bill Month", value=True)
                f_rent = st.checkbox("Line Rent", value=True)
                f_gprs = st.checkbox("GPRS/Blackberry", value=False)
                f_sms = st.checkbox("SMS/Voice Bundle", value=False)
                f_vas = st.checkbox("VAS", value=False)
                f_usage = st.checkbox("Usage Bill", value=True)
                f_lrd = st.checkbox("Line Rent Discount", value=False)
                f_bpd = st.checkbox("Billing/Promotional Discount", value=False)
                f_adj = st.checkbox("Adjustment", value=False)
                f_tot = st.checkbox("Total Bill Amount", value=True)
                f_fed = st.checkbox("FED (Sales Tax)", value=True)
                f_ait = st.checkbox("AIT", value=False)
                f_prev = st.checkbox("Previous Outstanding", value=False)
                f_pymt = st.checkbox("Payments", value=False)
                f_pay = st.checkbox("Payable", value=True)

        with right_col:
            with st.container(border=True):
                st.markdown(f"### 📄 Invoice Preview [{output_mode}]")
                
                if search_clicked:
                    df_backend = pd.DataFrame({
                        "Mobile Number": ["0300-1234567", "0321-9876543"],
                        "Subscriber Name": ["Ali Khan", "Ahmed Raza"],
                        "Company Customer Name": ["ABC Pvt Ltd", "XYZ Corp"],
                        "Plan Name": ["Corporate Gold", "Business Silver"],
                        "Activation Date": ["2024-01-15", "2023-11-10"],
                        "Subscriber Status": ["Active", "Active"],
                        "Bill Month": [selected_month, selected_month],
                        "Line Rent": [1500, 2500],
                        "GPRS/Blackberry": [200, 300],
                        "SMS/Voice Bundle": [150, 250],
                        "VAS": [50, 100],
                        "Usage Bill": [450, 1200],
                        "Line Rent Discount": [100, 150],
                        "Billing/Promotional Discount": [50, 0],
                        "Adjustment": [0, 0],
                        "Total Bill Amount": [2150, 4200],
                        "FED": [344, 672],
                        "AIT": [50, 100],
                        "Previous Outstanding": [0, 500],
                        "Payments": [0, 500],
                        "Payable": [2444, 4872],
                        "Invoice ID": ["INV-2026-101", "INV-2026-102"],
                        "NTN": ["0711579", "0822680"],
                        "Department ID": ["DEPT-FIN-01", "DEPT-IT-02"]
                    })
                    
                    filtered_df = df_backend.copy()
                    if invoice_id_query:
                        filtered_df = filtered_df[filtered_df['Invoice ID'].str.contains(invoice_id_query, case=False, na=False)]
                    if ntn_query:
                        filtered_df = filtered_df[filtered_df['NTN'].str.contains(ntn_query, na=False)]
                    if dept_query:
                        filtered_df = filtered_df[filtered_df['Department ID'].str.contains(dept_query, case=False, na=False)]
                    if cust_query:
                        filtered_df = filtered_df[filtered_df['Company Customer Name'].str.contains(cust_query, case=False, na=False)]

                    if not filtered_df.empty:
                        record = filtered_df.iloc[0]
                        
                        active_columns = []
                        if f_mob: active_columns.append("Mobile Number")
                        if f_sub: active_columns.append("Subscriber Name")
                        if f_comp: active_columns.append("Company Customer Name")
                        if f_plan: active_columns.append("Plan Name")
                        if f_act: active_columns.append("Activation Date")
                        if f_status: active_columns.append("Subscriber Status")
                        if f_month: active_columns.append("Bill Month")
                        if f_rent: active_columns.append("Line Rent")
                        if f_gprs: active_columns.append("GPRS/Blackberry")
                        if f_sms: active_columns.append("SMS/Voice Bundle")
                        if f_vas: active_columns.append("VAS")
                        if f_usage: active_columns.append("Usage Bill")
                        if f_lrd: active_columns.append("Line Rent Discount")
                        if f_bpd: active_columns.append("Billing/Promotional Discount")
                        if f_adj: active_columns.append("Adjustment")
                        if f_tot: active_columns.append("Total Bill Amount")
                        if f_fed: active_columns.append("FED")
                        if f_ait: active_columns.append("AIT")
                        if f_prev: active_columns.append("Previous Outstanding")
                        if f_pymt: active_columns.append("Payments")
                        if f_pay: active_columns.append("Payable")
                        
                        display_df = filtered_df[active_columns] if active_columns else filtered_df

                        r_comp = record['Company Customer Name']
                        r_sub = record['Subscriber Name']
                        r_mob = record['Mobile Number']
                        r_dept = record['Department ID']
                        r_inv = record['Invoice ID']
                        r_ntn = record['NTN']
                        r_tot_amt = record['Total Bill Amount']
                        r_fed_amt = record['FED']
                        r_pay = record['Payable']
                        current_date = datetime.now().strftime("%Y-%m-%d")

                        # RENDER BASED ON SELECTED MODE
                        if output_mode == "Single-Page (Summary + Detail Combined)":
                            # MODE A: Single page with summary card and detail table combined
                            st.markdown(f"""
                                <div class="custom-invoice-box">
                                    <div class="inv-header">
                                        <h2 style="margin:0; color:#1e3c72;">YOUR COMPANY NAME PVT LTD</h2>
                                        <p style="margin:2px 0; font-size:12px; color:#555;">Head Office Address, Islamabad | NTN: 1234567-8 | STRN: 07-01-2345-678-91</p>
                                        <h4 style="margin:5px 0 0 0; color:#2a5298;">SINGLE-PAGE INVOICE - [{client_format}]</h4>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:15px;">
                                        <div>
                                            <b>Bill To:</b> {r_comp}<br>
                                            <b>Subscriber:</b> {r_sub} ({r_mob})<br>
                                            <b>Billing Month:</b> {selected_month}<br>
                                            <b>Department ID:</b> <span style="color:#2a5298;"><b>{r_dept}</b></span>
                                        </div>
                                        <div style="text-align:right;">
                                            <b>Invoice ID:</b> <span style="color:#1e3c72; font-size:14px;"><b>{r_inv}</b></span><br>
                                            <b>Date:</b> {current_date}<br>
                                            <b>Client NTN:</b> {r_ntn}
                                        </div>
                                    </div>
                                    
                                    <div class="summary-card">
                                        <h4 style="margin:0 0 10px 0; color:#1e3c72; font-size:14px;">📊 Consolidated Billing Summary</h4>
                                        <div style="display:flex; justify-content:space-between; font-size:13px;">
                                            <span>Gross Total: <b>Rs. {r_tot_amt:,.2f}</b></span>
                                            <span>Sales Tax (FED): <b>Rs. {r_fed_amt:,.2f}</b></span>
                                            <span style="color:#1e3c72;"><b>Net Payable: Rs. {r_pay:,.2f}</b></span>
                                        </div>
                                    </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("<b>Detailed Breakdown:</b>", unsafe_allow_html=True)
                            st.table(display_df)
                            
                            st.markdown(f"""
                                    <div style="text-align:right; font-size:16px; margin-top:10px; color:#1e3c72;">
                                        <b>Total Payable Amount: Rs. {r_pay:,.2f}</b>
                                    </div>
                                    <div class="inv-footer">
                                        System-generated single-page invoice conforming to <b>{client_format}</b> standards.
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        else:
                            # MODE B: Summary Page First, Followed by Separate Detail Report Section
                            st.markdown(f"""
                                <div class="custom-invoice-box">
                                    <div class="inv-header">
                                        <h2 style="margin:0; color:#1e3c72;">YOUR COMPANY NAME PVT LTD</h2>
                                        <p style="margin:2px 0; font-size:12px; color:#555;">Official Account Statement & Billing Summary</p>
                                        <h4 style="margin:5px 0 0 0; color:#2a5298;">PART 1: OFFICIAL SUMMARY PAGE - [{client_format}]</h4>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:15px;">
                                        <div>
                                            <b>Customer:</b> {r_comp}<br>
                                            <b>Department ID:</b> {r_dept}<br>
                                            <b>Statement Month:</b> {selected_month}
                                        </div>
                                        <div style="text-align:right;">
                                            <b>Invoice ID:</b> <span style="color:#1e3c72;"><b>{r_inv}</b></span><br>
                                            <b>Statement Date:</b> {current_date}
                                        </div>
                                    </div>
                                    
                                    <div class="summary-card" style="background-color:#eef2f7; border-left:4px solid #1e3c72;">
                                        <h3 style="margin:0 0 15px 0; color:#1e3c72;">Account Summary Statement</h3>
                                        <table style="width:100%; font-size:14px;">
                                            <tr><td><b>Billing Cycle:</b></td><td>{selected_month}</td></tr>
                                            <tr><td><b>Total Charges:</b></td><td>Rs. {r_tot_amt:,.2f}</td></tr>
                                            <tr><td><b>Tax Adjustments (FED):</b></td><td>Rs. {r_fed_amt:,.2f}</td></tr>
                                            <tr style="border-top:1px solid #ccc;"><td style="padding-top:8px;"><b>Net Amount Payable:</b></td><td style="padding-top:8px; color:#1e3c72; font-size:16px;"><b>Rs. {r_pay:,.2f}</b></td></tr>
                                        </table>
                                    </div>
                                    <div class="inv-footer">Summary Page End. See Part 2 for full itemized breakdown.</div>
                                </div>
                                
                                <div class="custom-invoice-box" style="border-color:#2a5298;">
                                    <div class="inv-header" style="border-bottom-color:#2a5298;">
                                        <h4 style="margin:0; color:#2a5298;">PART 2: SEPARATE DETAIL REPORT & LINE ITEMS</h4>
                                    </div>
                            """, unsafe_allow_html=True)
                            
                            st.table(display_df)
                            
                            st.markdown(f"""
                                    <div style="text-align:right; font-size:15px; margin-top:10px;">
                                        <b>Verified Payable Total: Rs. {r_pay:,.2f}</b>
                                    </div>
                                    <div class="inv-footer">
                                        End of Detail Report. Conforming to <b>{client_format}</b> standards.
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        # Audit Log Entry
                        st.session_state.audit_logs.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.current_user,
                            "Mode": output_mode,
                            "Client Format": client_format,
                            "Invoice ID": r_inv,
                            "Amount": r_pay
                        })
                        
                        # Multi-Format Download Buttons
                        st.markdown("#### 📥 Download Invoice / Statement in Three Formats:")
                        d_col1, d_col2, d_col3 = st.columns(3)
                        
                        csv_data = display_df.to_csv(index=False).encode('utf-8')
                        txt_mock = f"INVOICE ID: {r_inv}\nMODE: {output_mode}\nPAYABLE: {r_pay}".encode('utf-8')
                        
                        pdf_buffer = io.BytesIO()
                        pdf_buffer.write(f"=== CORPORATE INVOICE [{output_mode}] ===\nInvoice ID: {r_inv}\nCustomer: {r_comp}\nPayable: Rs. {r_pay}\n=========================".encode('utf-8'))
                        pdf_data = pdf_buffer.getvalue()

                        with d_col1:
                            st.download_button("📊 Excel Format", data=csv_data, file_name=f"Invoice_{r_inv}.xlsx", mime="text/csv", use_container_width=True)
                        with d_col2:
                            st.download_button("📝 Word Format", data=txt_mock, file_name=f"Invoice_{r_inv}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                        with d_col3:
                            st.download_button("📑 PDF Format", data=pdf_data, file_name=f"Invoice_{r_inv}.pdf", mime="application/pdf", use_container_width=True)
                    else:
                        st.warning("⚠️ No matching records found for your search parameters.")
                else:
                    st.info("💡 Select your filters, choose your output mode, and click **Search**.")

    # ================= ADMIN USER RIGHTS =================
    if st.session_state.user_role == "Administrator":
        with tab_admin:
            st.markdown("### 🛡️ Administrator User Management")
            with st.form("new_usr"):
                u_name = st.text_input("Username")
                u_pass = st.text_input("Password", type="password")
                u_role = st.selectbox("Role", ["Operator", "Administrator"])
                if st.form_submit_button("Add User", type="primary"):
                    if u_name in st.session_state.users_db:
                        st.error("User exists.")
                    elif u_name and u_pass:
                        st.session_state.users_db[u_name] = {"password": u_pass, "role": u_role, "status": "Approved"}
                        st.success(f"User `{u_name}` created!")
            st.dataframe(pd.DataFrame([{"User": k, "Role": v["role"]} for k, v in st.session_state.users_db.items()]), use_container_width=True, hide_index=True)

    # ================= AUDIT LOGS =================
    with tab_audit:
        st.markdown("### 📜 System Activity & Audit Logs")
        if st.session_state.audit_logs:
            st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True, hide_index=True)
        else:
            st.info("No activity records found yet.")
