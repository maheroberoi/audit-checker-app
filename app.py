
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Audit Checker", layout="wide")

st.title("Audit Data Validator")
st.write("Upload your CSV or Excel file to check for common data issues.")

uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # Summary
        st.subheader("Basic Checks")
        st.write(f"Shape: {df.shape}")
        st.write("Column Names:", list(df.columns))

        # Missing values
        st.subheader("Missing Values")
        st.write(df.isnull().sum())

        # Duplicate rows
        st.subheader("Duplicate Rows")
        dupes = df[df.duplicated()]
        st.write(dupes)

        # Numeric outliers (basic z-score)
        st.subheader("Outlier Detection")
        num_cols = df.select_dtypes(include="number").columns
        for col in num_cols:
            z = (df[col] - df[col].mean()) / df[col].std()
            outliers = df[z.abs() > 3]
            if not outliers.empty:
                st.write(f"Outliers in `{col}`:")
                st.write(outliers[[col]])

    except Exception as e:
        st.error(f"Error: {e}")
