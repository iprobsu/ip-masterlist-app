import streamlit as st
import pandas as pd

st.set_page_config(page_title="📂 IP Masterlist Dashboard", layout="wide")
st.title("📂 IP Masterlist Dashboard")

# File uploader
uploaded_files = st.file_uploader("Upload Excel files (2006–2025)", accept_multiple_files=True, type=['xlsx'])

if uploaded_files:
    df_list = []
    for uploaded_file in uploaded_files:
        sheets = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
        for sheet_name, data in sheets.items():
            data['IP Type'] = sheet_name
            df_list.append(data)
    df = pd.concat(df_list, ignore_index=True)

    # Normalize Author field
    if 'Author' in df.columns:
        df['Author'] = df['Author'].astype(str).str.replace(';', ',', regex=False)
        df['Author'] = df['Author'].str.split(',')
        df['Author'] = df['Author'].apply(lambda authors: [a.strip() for a in authors])
        df = df.explode('Author').reset_index(drop=True)

    # Convert Date columns
    if 'Date Applied' in df.columns:
        df['Date Applied'] = pd.to_datetime(df['Date Applied'], errors='coerce')
    if 'Date Approved' in df.columns:
        df['Date Approved'] = pd.to_datetime(df['Date Approved'], errors='coerce')

    df.fillna('', inplace=True)
    
    st.success(f"✅ Loaded {len(df)} rows from {len(uploaded_files)} file(s).")
    st.write(df.head(15))
else:
    st.info("📎 Please upload one or more Excel files.")
