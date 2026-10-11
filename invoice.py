import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Corporate Interactive Invoicing System",
    page_icon="💼",
    layout="wide"
)

# Initialize Session States for Users and System History
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

# Custom CSS for Professional Enterprise Look
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
    .box-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
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
    # ================= 2. MAIN DASHBOARD (As per Wireframe) =================
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

    # Tabs based on roles
    if st.session_state.user_role == "Administrator":
        tab_main, tab_admin, tab_audit = st.tabs(["📊 Manual Invoice Generator", "🛡️ Admin User Rights", "📜 Audit Logs"])
    else:
        tab_main, tab_audit = st.tabs(["📊 Manual Invoice Generator", "📜 Audit Logs"])

    with tab_main:
        # Top Search & Filter Bar (Matching Wireframe Top Row)
        with st.container(border=True):
            col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns([1.2, 1.2, 1, 1, 1.2, 0.8])
            
            with col_s1:
                # Month Selector for Backend File mapping (e.g. October 2026)
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

        # Layout: Left side Format Selection & Checklists | Right side Output / Preview
        left_col, right_col = st.columns([1, 2], gap="large")

        with left_col:
            with st.container(border=True):
                st.markdown("### 🎨 Format Selection")
                # Format selection radio buttons (Format 1, 2, 3 as shown in image)
                invoice_format = st.radio(
                    "Select Desired Invoice Format:", 
                    ["Format 1 (Standard)", "Format 2 (Detailed)", "Format 3 (Executive Ledger)"]
                )
                
                st.markdown("---")
                st.markdown("### ☑️ Field Checklists (Add / Remove)")
                st.caption("Select fields to populate in the invoice:")
                
                # Checklists matching the wireframe column
                f_mob = st.checkbox("Mobile Number", value=True)
                f_sub = st.checkbox("Subscriber Name", value=True)
                f_comp = st.checkbox("Company Customer Name", value=True)
                f_plan = st.checkbox("Plan Name", value=False)
                f_act = st.checkbox("Activation Date", value=False)
                f_month = st.checkbox("Bill Month", value=True)
                f_rent = st.checkbox("Line Rent", value=True)
                f_usage = st.checkbox("Usage Bill", value=True)
                f_tot = st.checkbox("Total Bill Amount", value=True)
                f_fed = st.checkbox("FED (Sales Tax)", value=True)
                f_pay = st.checkbox("Payable", value=True)
                f_inv = st.checkbox("Invoice ID", value=True)

        with right_col:
            with st.container(border=True):
                st.markdown("### 📄 Populated Bill Information & Preview")
                
                if search_clicked:
                    # Backend simulation: Look for local monthly file e.g., "October_2026.xlsx"
                    file_name = f"{selected_month.replace(' ', '_')}.xlsx"
                    
                    # For demonstration/testing: If file exists locally, read it, otherwise create sample structured view
                    if os.path.exists(file_name):
                        df_backend = pd.read_excel(file_name)
                    else:
                        # Fallback sample dataset representing backend local file
                        df_backend = pd.DataFrame({
                            "Mobile Number": ["0300-1234567", "0321-9876543", "0333-5554433"],
                            "Subscriber Name": ["Ali Khan", "Ahmed Raza", "Sara Bilal"],
                            "Company Customer Name": ["ABC Pvt Ltd", "XYZ Corp", "Tech Solutions"],
                            "Bill Month": [selected_month, selected_month, selected_month],
                            "Line Rent": [1500, 2500, 3000],
                            "Usage Bill": [450, 1200, 800],
                            "Total Bill Amount": [1950, 3700, 3800],
                            "FED": [312, 592, 608],
                            "Payable": [2262, 4292, 4408],
                            "Invoice ID": ["INV-101", "INV-102", "INV-103"],
                            "NTN": ["0711579", "0822680", "0933791"]
                        })
                    
                    # Filter based on user query inputs
                    filtered_df = df_backend.copy()
                    if ntn_query:
                        filtered_df = filtered_df[filtered_df['NTN'].str.contains(ntn_query, na=False)]
                    if mob_query:
                        filtered_df = filtered_df[filtered_df['Mobile Number'].str.contains(mob_query, na=False)]
                    if cust_query:
                        filtered_df = filtered_df[filtered_df['Company Customer Name'].str.contains(cust_query, case=False, na=False)]

                    # Keep only columns that user selected via checkboxes
                    selected_columns = []
                    if f_mob: selected_columns.append("Mobile Number")
                    if f_sub: selected_columns.append("Subscriber Name")
                    if f_comp: selected_columns.append("Company Customer Name")
                    if f_month: selected_columns.append("Bill Month")
                    if f_rent: selected_columns.append("Line Rent")
                    if f_usage: selected_columns.append("Usage Bill")
                    if f_tot: selected_columns.append("Total Bill Amount")
                    if f_fed: selected_columns.append("FED")
                    if f_pay: selected_columns.append("Payable")
                    if f_inv: selected_columns.append("Invoice ID")

                    if not filtered_df.empty:
                        final_view_df = filtered_df[selected_columns] if all(col in filtered_df.columns for col in selected_columns) else filtered_df
                        st.success(f"✨ Record found successfully using **{invoice_format}** for `{selected_month}`!")
                        st.dataframe(final_view_df, use_container_width=True)
                        
                        # Log action in audit trail
                        st.session_state.audit_logs.append({
                            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.current_user,
                            "Month": selected_month,
                            "Format": invoice_format,
                            "Status": "Success Search"
                        })
                        
                        # Export Button
                        csv_export = final_view_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Generated Invoice Sheet",
                            data=csv_export,
                            file_name=f"Invoice_{selected_month}_{invoice_format.split()[0]}.csv",
                            mime="text/csv",
                            type="primary"
                        )
                    else:
                        st.warning("⚠️ No matching records found for your search parameters in this month's file.")
                else:
                    st.info("💡 Select your Format, choose Month, enter search filters on top, and click **Search** to populate the bill information here.")

    # ================= ADMIN USER RIGHTS TAB =================
    if st.session_state.user_role == "Administrator":
        with tab_admin:
            st.markdown("### 🛡️ Administrator User Rights Management")
            st.markdown("Create new operators and manage system privileges securely.")
            
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
            st.info("No activity logged yet.")
