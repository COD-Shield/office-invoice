import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Manual Invoice Tab - Corporate Billing", 
    page_icon="🧾", 
    layout="wide"
)

st.title("🧾 Manual Invoice Tab - Corporate Billing System")
st.markdown("Import raw Excel data, filter by date and NTN, select your billing format, choose required checklist fields, and generate final populated bills instantly.")
st.markdown("---")

# ================= TOP FILTER & SEARCH BAR =================
st.subheader("🔍 Search & Filter Parameters")
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(6)

with f_col1:
    start_date = st.date_input("Start Date", value=datetime(2022, 12, 1))[cite: 6]
with f_col2:
    end_date = st.date_input("End Date", value=datetime(2022, 12, 30))[cite: 6]
with f_col3:
    ntn_input = st.text_input("NTN", placeholder="Enter NTN")[cite: 6]
with f_col4:
    dept_id_input = st.text_input("Department ID", placeholder="Dept ID")[cite: 6]
with f_col5:
    customer_input = st.text_input("Customer Name", placeholder="Customer Name")[cite: 6]
with f_col6:
    st.markdown("<br>", unsafe_allow_html=True)
    search_clicked = st.button("🔍 Search", type="primary")[cite: 6]

st.markdown("---")

# ================= LAYOUT SPLIT: FORMAT & CHECKLISTS =================
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📥 Import & Format")
    
    # Import Option for Mobile Numbers / Raw Excel
    uploaded_file = st.file_uploader("Upload Mobile Numbers / Raw Excel", type=["xlsx", "xls", "csv"])[cite: 6]
    st.markdown("<small><i>Mobile numbers will be uploaded through import option[cite: 6].</i></small>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🎨 Select Bill Format")
    selected_format = st.radio("Choose Layout:", ["Format 1", "Format 2", "Format 3"])[cite: 6]

with col_right:
    st.subheader("☑️ Select Required Bill Fields (Checkboxes)")
    st.markdown("Check the boxes for information you want to populate in the final bill:")
    
    chk_col1, chk_col2, chk_col3 = st.columns(3)
    
    with chk_col1:
        cb_mobile = st.checkbox("Mobile Number", value=True)[cite: 6]
        cb_sub_name = st.checkbox("Subscriber Name", value=True)[cite: 6]
        cb_comp_name = st.checkbox("Company Customer Name", value=True)[cite: 6]
        cb_plan = st.checkbox("Plan Name")[cite: 6]
        cb_act_date = st.checkbox("Activation Date")[cite: 6]
        cb_status = st.checkbox("Subscriber Status")[cite: 6]
        
    with chk_col2:
        cb_bill_month = st.checkbox("Bill Month", value=True)[cite: 6]
        cb_line_rent = st.checkbox("Line Rent", value=True)[cite: 6]
        cb_gprs = st.checkbox("GPRS/Blackberry")[cite: 6]
        cb_sms = st.checkbox("SMS/voice Bundle")[cite: 6]
        cb_vas = st.checkbox("VAS")[cite: 6]
        cb_usage = st.checkbox("Usage Bill", value=True)[cite: 6]
        cb_total_bill = st.checkbox("Total Bill Amount", value=True)[cite: 6]
        
    with chk_col3:
        cb_lr_disc = st.checkbox("Line Rent Discount")[cite: 6]
        cb_promo_disc = st.checkbox("Billing/Promotional Discount", value=True)[cite: 6]
        cb_adjustment = st.checkbox("Adjustment")[cite: 6]
        cb_fed = st.checkbox("FED", value=True)[cite: 6]
        cb_ait = st.checkbox("AIT", value=True)[cite: 6]
        cb_payable = st.checkbox("Payable", value=True)[cite: 6]
        cb_prev_out = st.checkbox("Previous Outstanding")[cite: 6]
        cb_payments = st.checkbox("Payments")[cite: 6]
        cb_total_payable = st.checkbox("Total Payable", value=True)[cite: 6]
        cb_invoice_id = st.checkbox("Invoice ID", value=True)[cite: 6]

st.markdown("---")

# ================= PREVIEW & POPULATED BILL SHEET =================
st.subheader("📊 Populated Bill Information & Preview Sheet")

if uploaded_file is not None:
    # Read uploaded file
    if uploaded_file.name.endswith('.csv'):
        raw_df = pd.read_csv(uploaded_file)
    else:
        raw_df = pd.read_excel(uploaded_file)
        
    st.success(f"File imported successfully! Showing data for selected format: **{selected_format}**[cite: 6]")
    
    with st.container(border=True):
        st.markdown(f"### 📄 Active Bill Preview ({selected_format})")
        st.markdown(f"**Billing Period:** `{start_date}` to `{end_date}` | **NTN:** `{ntn_input}` | **Dept ID:** `{dept_id_input}`")
        st.markdown("---")
        
        # Display raw data preview or filtered data
        st.dataframe(raw_df, use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download Final Populated Bill Sheet
    csv_export = raw_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Final Populated Bill Sheet (Excel/CSV)",
        data=csv_export,
        file_name=f"Manual_Invoice_{selected_format}_{start_date}_to_{end_date}.csv",
        mime="text/csv",
    )
else:
    st.info("💡 **Instructions:** Please upload your raw Excel file or mobile numbers list using the **Import** option on the left to populate the bill details automatically[cite: 6].")
