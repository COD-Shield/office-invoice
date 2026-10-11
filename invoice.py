import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Corporate Interactive Invoicing System",
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

# Custom CSS for Professional Invoice & Enterprise Look
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
    .invoice-preview-box {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        color: #111827;
    }
    .invoice-header {
        border-bottom: 2px solid #1e3c72;
        padding-bottom: 15px;
        margin-bottom: 20px;
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
            <h2>Manual Invoice Tab - Corporate Billing Portal</h2>
            <p>Logged in as: <b>{st.session_state.current_user}</b> ({st.session_state.user_role})</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Logout & Admin Navigation
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
            col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns([1.2, 1.2, 1, 1, 1.2, 0.8])
            
            with col_s1:
                selected_month = st.selectbox("Billing Month", ["October 2026", "September 2026", "August 2026", "July 2026"])
            with col_s2:
                ntn_query = st.text_input("NTN Number", placeholder="e.g. 0711579")
            with col_s3:
                dept_query = st.text_input("Department ID", placeholder="Dept ID")
            with col_s4:
                cust_query = st.text_input("Customer Name", placeholder="Customer Name")
            with col_s5:
                mob_query = st.text_input("Mobile Number", placeholder="Mobile Number")
            with col_s6:
                st.markdown("<br>", unsafe_allow_html=True)
                search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        left_col, right_col = st.columns([1, 1.8], gap="large")

        with left_col:
            with st.container(border=True):
                st.markdown("### 🎨 Format Selection")
                invoice_format = st.radio(
                    "Select Desired Invoice Format:", 
                    ["Format 1 (Standard Summary)", "Format 2 (Detailed Breakdown)", "Format 3 (Executive Ledger)"]
                )
                
                st.markdown("---")
                st.markdown("### ☑️ Field Checklists")
                f_mob = st.checkbox("Mobile Number", value=True)
                f_sub = st.checkbox("Subscriber Name", value=True)
                f_comp = st.checkbox("Company Customer Name", value=True)
                f_month = st.checkbox("Bill Month", value=True)
                f_rent = st.checkbox("Line Rent", value=True)
                f_usage = st.checkbox("Usage Bill", value=True)
                f_tot = st.checkbox("Total Bill Amount", value=True)
                f_fed = st.checkbox("FED (Sales Tax)", value=True)
                f_pay = st.checkbox("Payable", value=True)
                f_inv = st.checkbox("Invoice ID", value=True)

        with right_col:
            with st.container(border=True):
                st.markdown("### 📄 Printable Invoice Visual Preview & Export")
                
                if search_clicked:
                    # Simulated backend data reading from monthly file
                    df_backend = pd.DataFrame({
                        "Mobile Number": ["0300-1234567", "0321-9876543"],
                        "Subscriber Name": ["Ali Khan", "Ahmed Raza"],
                        "Company Customer Name": ["ABC Pvt Ltd", "XYZ Corp"],
                        "Bill Month": [selected_month, selected_month],
                        "Line Rent": [1500, 2500],
                        "Usage Bill": [450, 1200],
                        "Total Bill Amount": [1950, 3700],
                        "FED": [312, 592],
                        "Payable": [2262, 4292],
                        "Invoice ID": ["INV-2026-101", "INV-2026-102"],
                        "NTN": ["0711579", "0822680"]
                    })
                    
                    filtered_df = df_backend.copy()
                    if ntn_query:
                        filtered_df = filtered_df[filtered_df['NTN'].str.contains(ntn_query, na=False)]
                    if mob_query:
                        filtered_df = filtered_df[filtered_df['Mobile Number'].str.contains(mob_query, na=False)]
                    if cust_query:
                        filtered_df = filtered_df[filtered_df['Company Customer Name'].str.contains(cust_query, case=False, na=False)]

                    if not filtered_df.empty:
                        record = filtered_df.iloc[0] # Pick first matched record for visual invoice
                        
                        # Visual Printable Invoice Layout Box
                        st.markdown(f"""
                            <div class="invoice-preview-box">
                                <div class="invoice-header">
                                    <h3 style="margin:0; color:#1e3c72;">🏢 CORPORATE INVOICE STATEMENT</h3>
                                    <p style="margin:2px 0; font-size:13px; color:gray;">Template: <b>{invoice_format}</b> | Cycle: <b>{selected_month}</b></p>
                                </div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:14px;">
                                    <div>
                                        <b>Invoice ID:</b> {record['Invoice ID']}<br>
                                        <b>Customer Name:</b> {record['Company Customer Name']}<br>
                                        <b>Subscriber:</b> {record['Subscriber Name']} ({record['Mobile Number']})
                                    </div>
                                    <div style="text-align:right;">
                                        <b>Date Generated:</b> {datetime.now().strftime("%Y-%m-%d")}<br>
                                        <b>NTN:</b> {record['NTN']}
                                    </div>
                                </div>
                        """, unsafe_allow_html=True)
                        
                        # Display Data Table inside preview
                        st.table(filtered_df[['Line Rent', 'Usage Bill', 'Total Bill Amount', 'FED', 'Payable']])
                        
                        st.markdown(f"""
                                <hr style="margin:10px 0;">
                                <div style="text-align:right; font-size:16px;">
                                    <b>Net Payable Amount: Rs. {record['Payable']:,.2f}</b>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Log action in audit trail
                        st.session_state.audit_logs.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.current_user,
                            "Invoice ID": record['Invoice ID'],
                            "Customer": record['Company Customer Name'],
                            "Month": selected_month,
                            "Format": invoice_format
                        })
                        
                        # Multi-Format Export Buttons (Excel, Word, PDF simulation)
                        st.markdown("#### 📥 Download Invoice in Multiple Formats:")
                        ex_col1, ex_col2, ex_col3 = st.columns(3)
                        
                        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                        txt_data = f"INVOICE ID: {record['Invoice ID']}\nCustomer: {record['Company Customer Name']}\nPayable: {record['Payable']}".encode('utf-8')
                        
                        with ex_col1:
                            st.download_button(
                                label="📊 Download Excel",
                                data=csv_data,
                                file_name=f"Invoice_{record['Invoice ID']}.xlsx" if False else f"Invoice_{record['Invoice ID']}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        with ex_col2:
                            st.download_button(
                                label="📝 Download Word",
                                data=txt_data,
                                file_name=f"Invoice_{record['Invoice ID']}.docx" if False else f"Invoice_{record['Invoice ID']}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        with ex_col3:
                            st.download_button(
                                label="📑 Download PDF",
                                data=txt_data,
                                file_name=f"Invoice_{record['Invoice ID']}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    else:
                        st.warning("⚠️ No matching records found for your search parameters.")
                else:
                    st.info("💡 Enter your search filters on top and click **Search** to generate and view the visual printable invoice.")

    # ================= ADMIN USER RIGHTS TAB =================
    if st.session_state.user_role == "Administrator":
        with tab_admin:
            st.markdown("### 🛡️ Administrator User Rights Management")
            with st.form("admin_create_user"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                new_r = st.selectbox("Assign Role", ["Operator", "Administrator"])
                
                if st.form_submit_button("Create User", type="primary"):
                    if new_user in st.session_state.users_db:
                        st.error("User already exists.")
                    elif new_user and new_pass:
                        st.session_state.users_db[new_user] = {"password": new_pass, "role": new_r, "status": "Approved"}
                        st.success(f"User `{new_user}` created successfully!")

            st.markdown("---")
            st.markdown("### 📋 Existing Users Directory")
            users_list = [{"Username": u, "Role": d["role"], "Status": d["status"]} for u, d in st.session_state.users_db.items()]
            st.dataframe(pd.DataFrame(users_list), use_container_width=True, hide_index=True)

    # ================= AUDIT LOGS TAB =================
    with tab_audit:
        st.markdown("### 📜 System Activity Audit Trail")
        if st.session_state.audit_logs:
            st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True, hide_index=True)
        else:
            st.info("No invoices generated yet.")
