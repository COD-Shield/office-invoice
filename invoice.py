import streamlit as st
import pandas as pd
from datetime import datetime
import io
import streamlit.components.v1 as components

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
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
            <h2>Manual Invoice Tab - Sales Tax Invoice Portal</h2>
            <p>Logged in as: <b>{st.session_state.current_user}</b> ({st.session_state.user_role})</p>
        </div>
    """, unsafe_allow_html=True)
    
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
        with st.container(border=True):
            col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns([1, 1, 1, 1, 1, 0.8])
            
            with col_s1:
                selected_month = st.selectbox("Billing Month", ["October 2026", "September 2026", "August 2026"])
            with col_s2:
                invoice_id_query = st.text_input("Invoice ID", placeholder="e.g. KPCPL-MBBADV-1224")
            with col_s3:
                ntn_query = st.text_input("NTN Number", placeholder="e.g. 12445")
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
                st.markdown("### 🏛️ Client Format Settings")
                client_format = st.selectbox(
                    "Select Client Custom Format:",
                    ["CMPAK Standard Sales Tax Format", "Client A (Special Layout)", "Client B (Executive Layout)"]
                )
                
                st.markdown("---")
                st.markdown("### ☑️ Field Checklists")
                f_mob = st.checkbox("Mobile Number", value=True)
                f_sub = st.checkbox("Subscriber Name", value=True)
                f_comp = st.checkbox("Company Customer Name", value=True)
                f_plan = st.checkbox("Plan / Description", value=True)
                f_inv = st.checkbox("Invoice #", value=True)
                f_charges = st.checkbox("Charges Breakdown", value=True)
                f_pay = st.checkbox("Payable Amount", value=True)
                f_words = st.checkbox("Amount in Words", value=True)
                f_method = st.checkbox("Payment Method", value=True)

        with right_col:
            with st.container(border=True):
                st.markdown("### 📄 Sales Tax Invoice Preview")
                
                if search_clicked:
                    df_backend = pd.DataFrame({
                        "Mobile Number": ["0300-1234567", "0321-9876543"],
                        "Subscriber Name": ["Mr. Wu", "Ahmed Raza"],
                        "Company Customer Name": ["asd", "XYZ Corp"],
                        "Plan / Description": ["20 MBB New Tarif ACL 150 GB", "Business Silver"],
                        "Invoice #": ["KPCPL-MBBADV-1224", "KPCPL-MBBADV-1225"],
                        "Charges Breakdown": ["Rs.8,178 x 20 = 163,560/-", "Rs.5,000 x 10 = 50,000/-"],
                        "Payable Amount": ["Rs.163,560/-", "Rs.50,000/-"],
                        "Amount in Words": ["One Hundred Sixty-Three Thousand, Five Hundred and Sixty Rupees Only", "Fifty Thousand Rupees Only"],
                        "Payment Method": ["Cheque/PO to be made in favor of CMPAK Ltd.", "Cheque/PO to be made in favor of CMPAK Ltd."],
                        "NTN": ["12445", "0822680"],
                        "PNTN": ["aaw2", "aaw3"],
                        "Address": ["Islamabad.", "Rawalpindi."],
                        "Department ID": ["DEPT-FIN-01", "DEPT-IT-02"]
                    })
                    
                    filtered_df = df_backend.copy()
                    if invoice_id_query:
                        filtered_df = filtered_df[filtered_df['Invoice #'].str.contains(invoice_id_query, case=False, na=False)]
                    if ntn_query:
                        filtered_df = filtered_df[filtered_df['NTN'].str.contains(ntn_query, na=False)]
                    if dept_query:
                        filtered_df = filtered_df[filtered_df['Department ID'].str.contains(dept_query, case=False, na=False)]
                    if cust_query:
                        filtered_df = filtered_df[filtered_df['Company Customer Name'].str.contains(cust_query, case=False, na=False)]

                    if not filtered_df.empty:
                        record = filtered_df.iloc[0]
                        
                        r_comp = record['Company Customer Name']
                        r_sub = record['Subscriber Name']
                        r_ntn = record['NTN']
                        r_pntn = record['PNTN']
                        r_addr = record['Address']
                        r_invnum = record['Invoice #']
                        r_desc = record['Plan / Description']
                        r_charges = record['Charges Breakdown']
                        r_pay = record['Payable Amount']
                        r_words = record['Amount in Words']
                        r_method = record['Payment Method']
                        current_date = datetime.now().strftime("%d-%b-%Y")

                        # Using components.html for 100% robust HTML/CSS rendering without markdown interference
                        invoice_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <style>
                            .sales-tax-invoice-box {{
                                background-color: #ffffff;
                                border: 1px solid #333333;
                                padding: 35px;
                                border-radius: 4px;
                                color: #000000;
                                font-family: Arial, sans-serif;
                            }}
                            .invoice-title {{
                                text-align: center;
                                font-size: 18px;
                                font-weight: bold;
                                text-decoration: underline;
                                margin-bottom: 20px;
                            }}
                            .invoice-table {{
                                width: 100%;
                                border-collapse: collapse;
                                margin-top: 15px;
                                margin-bottom: 15px;
                                font-size: 13px;
                            }}
                            .invoice-table th, .invoice-table td {{
                                border: 1px solid #333333;
                                padding: 8px 12px;
                                text-align: left;
                            }}
                            .invoice-table th {{
                                background-color: #f2f2f2;
                            }}
                            .invoice-footer-note {{
                                font-size: 10px;
                                color: #444444;
                                margin-top: 15px;
                                border-top: 1px solid #ddd;
                                padding-top: 8px;
                            }}
                        </style>
                        </head>
                        <body>
                            <div class="sales-tax-invoice-box">
                                <div style="text-align: right; font-size: 12px; margin-bottom: 10px;">
                                    <b>Dated:</b> {current_date}
                                </div>
                                <div class="invoice-title">SALES TAX INVOICE</div>
                                
                                <div style="font-size: 13px; line-height: 1.6; margin-bottom: 20px;">
                                    <b>Account Name:</b> &nbsp;&nbsp;&nbsp; {r_comp}<br>
                                    <b>NTN:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {r_ntn}<br><br>
                                    <b>POC:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {r_sub}<br>
                                    <b>Address:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {r_addr}<br>
                                    <b>Contact:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {record['Mobile Number']}<br><br>
                                    <b>BY</b><br>
                                    <b>Company information:</b> {r_comp}<br>
                                    <b>PNTN:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {r_pntn}<br>
                                    <b>Address:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {r_addr}
                                </div>

                                <table class="invoice-table">
                                    <tr>
                                        <th colspan="2" style="text-align: center;">Invoice Details</th>
                                    </tr>
                                    <tr>
                                        <td><b>Description of Services/Product</b></td>
                                        <td>{r_desc}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Invoice #</b></td>
                                        <td>{r_invnum}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Charges Details</b></td>
                                        <td>{r_charges}</td>
                                    </tr>
                                    <tr>
                                        <td><b>Payable</b></td>
                                        <td><b>{r_pay}</b></td>
                                    </tr>
                                    <tr>
                                        <td><b>Amount in Words</b></td>
                                        <td><b>{r_words}</b></td>
                                    </tr>
                                    <tr>
                                        <td><b>Payment Method</b></td>
                                        <td>{r_method}</td>
                                    </tr>
                                </table>

                                <div class="invoice-footer-note">
                                    <b>Note:</b> "This is an advance invoice issued at the customer's request. Additional charges may apply throughout the month and will be included in the monthly billed invoice."<br>
                                    *Payable amount is inclusive of taxes
                                </div>
                            </div>
                        </body>
                        </html>
                        """
                        
                        components.html(invoice_html, height=650, scrolling=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.session_state.audit_logs.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.current_user,
                            "Format": client_format,
                            "Invoice ID": r_invnum,
                            "Amount": r_pay
                        })
                        
                        st.markdown("#### 📥 Download Invoice in Three Formats:")
                        d_col1, d_col2, d_col3 = st.columns(3)
                        
                        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                        txt_mock = f"SALES TAX INVOICE\nInvoice #: {r_invnum}\nPayable: {r_pay}\nAmount in Words: {r_words}".encode('utf-8')
                        
                        pdf_buffer = io.BytesIO()
                        pdf_buffer.write(f"=== SALES TAX INVOICE ===\nInvoice #: {r_invnum}\nAccount: {r_comp}\nPayable: {r_pay}\n=========================".encode('utf-8'))
                        pdf_data = pdf_buffer.getvalue()

                        with d_col1:
                            st.download_button("📊 Excel Format", data=csv_data, file_name=f"SalesTax_Invoice_{r_invnum}.xlsx", mime="text/csv", use_container_width=True)
                        with d_col2:
                            st.download_button("📝 Word Format", data=txt_mock, file_name=f"SalesTax_Invoice_{r_invnum}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                        with d_col3:
                            st.download_button("📑 PDF Format", data=pdf_data, file_name=f"SalesTax_Invoice_{r_invnum}.pdf", mime="application/pdf", use_container_width=True)
                    else:
                        st.warning("⚠️ No matching records found for your search parameters.")
                else:
                    st.info("💡 Select your filters and click **Search** to generate the official Sales Tax Invoice.")

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

    with tab_audit:
        st.markdown("### 📜 System Activity & Audit Logs")
        if st.session_state.audit_logs:
            st.dataframe(pd.DataFrame(st.session_state.audit_logs), use_container_width=True, hide_index=True)
        else:
            st.info("No activity records found yet.")
