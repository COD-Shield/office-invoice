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
            <h2>Manual Invoice Tab - Summary & Detail Sheet Portal</h2>
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
                invoice_id_query = st.text_input("Invoice ID", placeholder="e.g. KPCPL-ADV-1224")
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
                    ["Standard Corporate Format", "Client A (Special Layout)", "Client B (Executive Layout)"]
                )
                
                st.markdown("---")
                st.markdown("### ☑️ Excel Detail Sheet Checklists")
                
                f_mob = st.checkbox("Mobile Number", value=True)
                f_sub = st.checkbox("Subscriber Name", value=True)
                f_comp = st.checkbox("Company Customer Name", value=True)
                f_plan = st.checkbox("Plan Name", value=True)
                f_act = st.checkbox("Activation Date", value=True)
                f_status = st.checkbox("Subscriber Status", value=True)
                f_month = st.checkbox("Bill Month", value=True)
                f_rent = st.checkbox("Line Rent", value=True)
                f_gprs = st.checkbox("GPRS/Data Usage", value=True)
                f_sms = st.checkbox("SMS/Voice Bundle", value=True)
                f_vas = st.checkbox("VAS", value=True)
                f_usage = st.checkbox("Usage Bill", value=True)
                f_lrd = st.checkbox("Line Rent Discount", value=True)
                f_bpd = st.checkbox("Promotional Discount", value=True)
                f_adj = st.checkbox("Adjustment", value=True)
                f_tot = st.checkbox("Total Bill Amount", value=True)
                f_fed = st.checkbox("FED (Sales Tax)", value=True)
                f_ait = st.checkbox("AIT", value=True)
                f_prev = st.checkbox("Previous Outstanding", value=True)
                f_pymt = st.checkbox("Payments", value=True)
                f_pay = st.checkbox("Payable Amount", value=True)

        with right_col:
            with st.container(border=True):
                st.markdown("### 📄 Sales Tax Summary Page & Excel Detail Sheet")
                
                if search_clicked:
                    df_backend = pd.DataFrame({
                        "Mobile Number": ["0300-1234567", "0300-7654321", "0321-9876543"],
                        "Subscriber Name": ["Mr. Wu", "Ali Khan", "Ahmed Raza"],
                        "Company Customer Name": ["asd Pvt Ltd", "asd Pvt Ltd", "XYZ Corp"],
                        "Plan Name": ["20 MBB New Tarif ACL 150 GB", "Corporate Gold", "Business Silver"],
                        "Activation Date": ["2024-01-15", "2024-02-10", "2023-11-10"],
                        "Subscriber Status": ["Active", "Active", "Active"],
                        "Bill Month": [selected_month, selected_month, selected_month],
                        "Line Rent": [8178, 1500, 2500],
                        "GPRS/Data Usage": [200, 300, 400],
                        "SMS/Voice Bundle": [150, 200, 250],
                        "VAS": [50, 50, 100],
                        "Usage Bill": [450, 500, 1200],
                        "Line Rent Discount": [100, 100, 150],
                        "Promotional Discount": [50, 0, 0],
                        "Adjustment": [0, 0, 0],
                        "Total Bill Amount": [8828, 1950, 4200],
                        "FED": [1412, 312, 672],
                        "AIT": [100, 50, 100],
                        "Previous Outstanding": [0, 0, 500],
                        "Payments": [0, 0, 500],
                        "Payable Amount": ["Rs.10,340/-", "Rs.2,312/-", "Rs.4,872/-"],
                        "Invoice #": ["KPCPL-ADV-1224", "KPCPL-ADV-1224", "KPCPL-ADV-1225"],
                        "NTN": ["12445", "12445", "0822680"],
                        "PNTN": ["aaw2", "aaw2", "aaw3"],
                        "Address": ["Islamabad.", "Islamabad.", "Rawalpindi."],
                        "Department ID": ["DEPT-FIN-01", "DEPT-FIN-01", "DEPT-IT-02"]
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
                        r_desc = record['Plan Name']
                        r_charges = "Rs.8,178 x 20 = 163,560/-"
                        r_pay = "Rs.163,560/-"
                        r_words = "One Hundred Sixty-Three Thousand, Five Hundred and Sixty Rupees Only"
                        r_method = "Cheque/PO to be made in favor of Corporate Billing Department."
                        current_date = datetime.now().strftime("%d-%b-%Y")

                        # 1. SUMMARY PAGE RENDER VIA components.html
                        summary_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <style>
                            .sales-tax-invoice-box {{
                                background-color: #ffffff;
                                border: 1px solid #333333;
                                padding: 30px;
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
                        components.html(summary_html, height=600, scrolling=True)
                        
                        st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

                        # 2. SEPARATE EXCEL-STYLE DETAIL SHEET
                        st.markdown("### 📊 Excel-Style Itemized Detail Sheet")
                        st.markdown("<p style='font-size:13px; color:gray;'>Subscriber-wise detailed breakdown and usage sheet:</p>", unsafe_allow_html=True)
                        
                        active_columns = []
                        if f_mob: active_columns.append("Mobile Number")
                        if f_sub: active_columns.append("Subscriber Name")
                        if f_comp: active_columns.append("Company Customer Name")
                        if f_plan: active_columns.append("Plan Name")
                        if f_act: active_columns.append("Activation Date")
                        if f_status: active_columns.append("Subscriber Status")
                        if f_month: active_columns.append("Bill Month")
                        if f_rent: active_columns.append("Line Rent")
                        if f_gprs: active_columns.append("GPRS/Data Usage")
                        if f_sms: active_columns.append("SMS/Voice Bundle")
                        if f_vas: active_columns.append("VAS")
                        if f_usage: active_columns.append("Usage Bill")
                        if f_lrd: active_columns.append("Line Rent Discount")
                        if f_bpd: active_columns.append("Promotional Discount")
                        if f_adj: active_columns.append("Adjustment")
                        if f_tot: active_columns.append("Total Bill Amount")
                        if f_fed: active_columns.append("FED")
                        if f_ait: active_columns.append("AIT")
                        if f_prev: active_columns.append("Previous Outstanding")
                        if f_pymt: active_columns.append("Payments")
                        if f_pay: active_columns.append("Payable Amount")

                        display_df = filtered_df[active_columns] if active_columns else filtered_df
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.session_state.audit_logs.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.current_user,
                            "Format": client_format,
                            "Invoice ID": r_invnum,
                            "Amount": r_pay
                        })
                        
                        # Download Buttons (Using standard CSV for Excel to prevent missing dependency errors)
                        st.markdown("#### 📥 Download Summary & Excel Detail Sheet:")
                        d_col1, d_col2, d_col3 = st.columns(3)
                        
                        csv_data = display_df.to_csv(index=False).encode('utf-8')
                        
                        word_buffer = io.BytesIO()
                        word_content = f"""
                        <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2 style="text-align: center; text-decoration: underline;">SALES TAX INVOICE</h2>
                            <p><b>Dated:</b> {current_date} &nbsp;&nbsp;&nbsp; <b>Invoice #:</b> {r_invnum}</p>
                            <p><b>Account Name:</b> {r_comp}<br><b>NTN:</b> {r_ntn} | <b>POC:</b> {r_sub}<br><b>Address:</b> {r_addr}</p>
                            <hr>
                            <h3>Invoice Details</h3>
                            <p><b>Description:</b> {r_desc}</p>
                            <p><b>Charges Details:</b> {r_charges}</p>
                            <p><b>Payable Amount:</b> {r_pay}</p>
                            <p><b>Amount in Words:</b> {r_words}</p>
                            <p><b>Payment Method:</b> {r_method}</p>
                        </body>
                        </html>
                        """
                        word_buffer.write(word_content.encode('utf-8'))
                        word_data = word_buffer.getvalue()

                        pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 380 >>
stream
BT
/F1 16 Tf
50 730 Td
(SALES TAX INVOICE) Tj
/F1 11 Tf
0 -25 Td
(Invoice #: {r_invnum} | Date: {current_date}) Tj
0 -20 Td
(Account Name: {r_comp}) Tj
0 -18 Td
(NTN: {r_ntn} | POC: {r_sub}) Tj
0 -18 Td
(Address: {r_addr}) Tj
0 -25 Td
(Description: {r_desc}) Tj
0 -18 Td
(Charges Details: {r_charges}) Tj
0 -18 Td
(Payable Amount: {r_pay}) Tj
0 -18 Td
(Amount in Words: {r_words}) Tj
0 -18 Td
(Payment Method: {r_method}) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000288 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
675
%%EOF""".encode('utf-8')

                        with d_col1:
                            st.download_button("📊 Excel Detail Sheet", data=csv_data, file_name=f"Detail_Sheet_{r_invnum}.csv", mime="text/csv", use_container_width=True)
                        with d_col2:
                            st.download_button("📝 Word Document", data=word_data, file_name=f"Invoice_{r_invnum}.doc", mime="application/msword", use_container_width=True)
                        with d_col3:
                            st.download_button("📑 PDF Document", data=pdf_content, file_name=f"Invoice_{r_invnum}.pdf", mime="application/pdf", use_container_width=True)
                    else:
                        st.warning("⚠️ No matching records found for your search parameters.")
                else:
                    st.info("💡 Select your filters and click **Search** to generate the Summary Invoice & Excel Detail Sheet.")

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
