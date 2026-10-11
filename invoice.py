import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Secure Corporate Invoicing Portal",
    page_icon="🔐",
    layout="wide"
)

# Initialize Session States for Authentication, Database & Approvals
if 'users_db' not in st.session_state:
    # Default Admin account pre-configured
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "Administrator", "status": "Approved"}
    }
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'invoice_history' not in st.session_state:
    st.session_state.invoice_history = []
if 'approval_queue' not in st.session_state:
    st.session_state.approval_queue = []

# Custom CSS Styling
st.markdown("""
    <style>
    .auth-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 30px;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .dash-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# ================= 1. PRE-LOGIN AUTHENTICATION GATE =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🔐 Secure Portal Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>Enter credentials or register for access.</p>", unsafe_allow_html=True)
            
            auth_mode = st.radio("Select Action:", ["Login", "Register New Account"], horizontal=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if auth_mode == "Login":
                if st.button("🔑 Login to Portal", type="primary", use_container_width=True):
                    if username in st.session_state.users_db:
                        user_info = st.session_state.users_db[username]
                        if user_info["status"] != "Approved":
                            st.warning("⚠️ Your account is pending Administrator approval.")
                        elif user_info["password"] == password:
                            st.session_state.logged_in = True
                            st.session_state.current_user = username
                            st.session_state.user_role = user_info["role"]
                            st.success("🎉 Login successful! Opening portal...")
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password.")
                    else:
                        st.error("❌ Username not found.")
            else:
                # Registration
                if st.button("📝 Register Account", type="primary", use_container_width=True):
                    if username in st.session_state.users_db:
                        st.error("❌ Username already exists.")
                    elif not username or not password:
                        st.warning("⚠️ Please fill in all fields.")
                    else:
                        # New registrations go to pending status
                        st.session_state.users_db[username] = {
                            "password": password, 
                            "role": "Operator", 
                            "status": "Pending"
                        }
                        st.success("✅ Registration successful! Please wait for Administrator access approval.")

# ================= 2. MAIN APPLICATION (POST-LOGIN) =================
else:
    # Top Header & Logout Option
    st.markdown(f"""
        <div class="dash-header">
            <h1>🏢 Corporate Invoicing & Workflow Portal</h1>
            <p>Welcome back, <b>{st.session_state.current_user}</b> ({st.session_state.user_role})</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Controls
    st.sidebar.markdown(f"### 👤 Logged In As")
    st.sidebar.info(f"**User:** {st.session_state.current_user}\n\n**Role:** {st.session_state.user_role}")
    if st.sidebar.button("🚪 Logout", type="secondary"):
        st.session_state.logged_in = False
        st.rerun()

    # Define Navigation Tabs based on Role
    if st.session_state.user_role == "Administrator":
        tab1, tab2, tab3, tab4 = st.tabs(["⚡ Invoicing Dashboard", "🛡️ Admin Approvals & User Access", "🎨 Invoice Templates (Formats)", "📜 Audit Trail"])
    else:
        tab1, tab3, tab4 = st.tabs(["⚡ Invoicing Dashboard", "🎨 Invoice Templates (Formats)", "📜 Audit Trail"])

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
                st.markdown("### 📥 Import & Formats")
                uploaded_file = st.file_uploader("Upload Raw Excel / Mobile Numbers", type=["xlsx", "xls", "csv"])
                
                # Format Selection
                selected_format = st.selectbox(
                    "🎨 Choose Corporate Format Template:", 
                    ["Format 1 (Standard Summary)", "Format 2 (Detailed Breakdown)", "Format 3 (Executive Corporate)"]
                )

        with col_right:
            with st.container(border=True):
                st.markdown("### ✏️ Amount Verification & Approvals")
                override_check = st.checkbox("⚠️ Modify / Override Raw Bill Amount manually?")
                modified_amount = 0.0
                if override_check:
                    modified_amount = st.number_input("Enter Modified Total Bill Amount (Rs.)", min_value=0.0, value=25000.0, step=500.0)

                st.markdown("---")
                st.markdown("Select required fields to include:")
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
            
            if st.button("🚀 Process & Generate Invoice", type="primary", use_container_width=True):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if override_check:
                    approval_id = f"APP-{len(st.session_state.approval_queue) + 101}"
                    st.session_state.approval_queue.append({
                        "Approval_ID": approval_id,
                        "Operator": st.session_state.current_user,
                        "Template": selected_format,
                        "Modified_Amount": modified_amount,
                        "Status": "Pending Approval",
                        "Timestamp": timestamp
                    })
                    st.warning(f"⚠️ **Amount modified!** Request `{approval_id}` sent to Administrator for approval.")
                else:
                    st.session_state.invoice_history.append({
                        "Timestamp": timestamp,
                        "Operator": st.session_state.current_user,
                        "Template": selected_format,
                        "Status": "Approved / Direct",
                        "Amount": "Standard Raw Data"
                    })
                    st.success(f"✅ Invoice successfully generated and logged!")
        else:
            st.info("💡 Please upload your raw Excel file using the import option above.")

    # ================= TAB 2: ADMIN APPROVALS & USER ACCESS (Admin Only) =================
    if st.session_state.user_role == "Administrator":
        with tab2:
            st.markdown("### 🛡️ User Access Control & Account Approvals")
            st.markdown("Approve new staff accounts or reject unauthorized sign-ups.")
            
            pending_users = {uname: data for uname, data in st.session_state.users_db.items() if data["status"] == "Pending"}
            if pending_users:
                for uname, udata in pending_users.items():
                    col_u1, col_u2, col_u3 = st.columns([2, 2, 1])
                    with col_u1:
                        st.markdown(f"**Username:** `{uname}`")
                    with col_u2:
                        st.markdown(f"**Role:** `{udata['role']}` | **Status:** 🟡 Pending")
                    with col_u3:
                        if st.button("✅ Grant Access", key=f"usr_{uname}"):
                            st.session_state.users_db[uname]["status"] = "Approved"
                            st.rerun()
            else:
                st.info("✅ No pending user account requests.")

            st.markdown("---")
            st.markdown("### 🛡️ Pending Invoice Amount Approvals")
            pending_invoices = [item for item in st.session_state.approval_queue if item["Status"] == "Pending Approval"]
            
            if pending_invoices:
                for idx, item in enumerate(pending_invoices):
                    with st.container(border=True):
                        col_a, col_b, col_c = st.columns([2, 2, 1])
                        with col_a:
                            st.markdown(f"**Approval ID:** `{item['Approval_ID']}`")
                            st.markdown(f"**Operator:** `{item['Operator']}`")
                            st.markdown(f"**Template:** `{item['Template']}`")
                        with col_b:
                            st.markdown(f"**Modified Amount:** `Rs. {item['Modified_Amount']:,.2f}`")
                            st.markdown(f"**Status:** 🟡 `{item['Status']}`")
                        with col_c:
                            if st.button("✅ Approve", key=f"app_inv_{idx}"):
                                item["Status"] = "Approved"
                                st.session_state.invoice_history.append({
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Operator": f"{item['Operator']} (Approved by Admin)",
                                    "Template": item['Template'],
                                    "Status": "Approved via Workflow",
                                    "Amount": item['Modified_Amount']
                                })
                                st.rerun()
                            if st.button("❌ Reject", key=f"rej_inv_{idx}"):
                                item["Status"] = "Rejected"
                                st.rerun()
            else:
                st.info("✅ No pending invoice amount modifications.")

    # ================= TAB 3: INVOICE TEMPLATES & FORMATS =================
    with tab3:
        st.markdown("### 🎨 Corporate Invoice Templates & Layout Mapping")
        st.markdown("Here is where your invoice formats (**Format 1, Format 2, Format 3**) are structured and mapped with raw data columns.")
        
        with st.expander("📄 Format 1: Standard Summary Template"):
            st.markdown("• **Header:** Company Logo, NTN, STRN & Bill Month")
            st.markdown("• **Core Fields:** Mobile Number, Subscriber Name, Line Rent & Total Payable")
            st.markdown("• *Best for standard consumer billing.*")
            
        with st.expander("📄 Format 2: Detailed Breakdown Template"):
            st.markdown("• **Header:** Corporate Client Details & Department ID")
            st.markdown("• **Core Fields:** Line Rent, GPRS/Blackberry, Usage Charges, VAS & Discounts")
            st.markdown("• *Best for corporate enterprise accounts.*")

        with st.expander("📄 Format 3: Executive Corporate Template"):
            st.markdown("• **Header:** Complete Billing Ledger & Tax Summary")
            st.markdown("• **Core Fields:** Previous Outstanding, Payments, FED, AIT & Net Payable")
            st.markdown("• *Best for high-value tax reconciled settlements.*")

    # ================= TAB 4: AUDIT TRAIL =================
    with tab4:
        st.markdown("### 📜 System Activity & Invoice Audit Trail")
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
