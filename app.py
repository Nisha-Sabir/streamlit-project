import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set up the Streamlit app
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("📊 Data Sweeper")
st.write("Upload CSV or Excel files for cleaning, visualization, and conversion.")

# File uploader
uploaded_file = st.file_uploader("Upload your file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

    # Read file
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error(f"❌ Unsupported file type: {file_ext}")
        st.stop()

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Data Cleaning Options
    if st.checkbox("🧹 Remove Duplicates"):
        df = df.drop_duplicates()
        st.success("✅ Duplicates removed!")

    if st.checkbox("📌 Handle Missing Values"):
        df = df.fillna("N/A")
        st.success("✅ Missing values handled!")

    # Column Selection
    columns = st.multiselect("📝 Select Columns to Keep", df.columns, default=df.columns)
    df = df[columns]

    st.subheader("✅ Final Processed Data")
    st.dataframe(df.head())

    # Data Visualization
    st.subheader("📊 Data Visualization")

    # Numeric Column Histogram
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        hist_col = st.selectbox("Select a numeric column for histogram", num_cols)
        fig, ax = plt.subplots()
        df[hist_col].hist(ax=ax, bins=20, edgecolor='black')
        st.pyplot(fig)

    # Categorical Column Bar Chart
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if cat_cols:
        bar_col = st.selectbox("Select a categorical column for bar chart", cat_cols)
        fig, ax = plt.subplots()
        df[bar_col].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    # Save Processed Data
    output_file = "processed_data.csv"
    df.to_csv(output_file, index=False)
    st.download_button("💾 Download Processed Data", data=open(output_file, "rb"), file_name=output_file)

 

 
