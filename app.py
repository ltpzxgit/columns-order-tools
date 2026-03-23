import streamlit as st
import pandas as pd

st.set_page_config(page_title="Column Splitter", layout="wide")

st.title("📊 Log Column Splitter (Combine Date + Time)")

uploaded_file = st.file_uploader("📥 Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Raw Data")
    st.dataframe(df.head())

    # เลือก column ที่จะ split
    column_to_split = st.selectbox("เลือก column ที่จะ split", df.columns)

    delimiter = st.text_input("Delimiter (ตัวคั่น)", value=" ")

    if st.button("🚀 Split Columns"):
        # split column
        split_df = df[column_to_split].astype(str).str.split(delimiter, expand=True)

        # รวม column 0 และ 1 → datetime
        if 0 in split_df.columns and 1 in split_df.columns:
            split_df["datetime"] = split_df[0] + " " + split_df[1]
            split_df["datetime"] = pd.to_datetime(split_df["datetime"], errors="coerce")

            # ลบ 0 กับ 1
            split_df = split_df.drop(columns=[0, 1])

            # ย้าย datetime ไปไว้หน้า
            cols = ["datetime"] + [col for col in split_df.columns if col != "datetime"]
            split_df = split_df[cols]

        # ตั้งชื่อ column ใหม่
        split_df.columns = [str(col) for col in split_df.columns]

        # รวมกับ df เดิม
        final_df = pd.concat([df, split_df], axis=1)

        st.subheader("✅ Result")
        st.dataframe(final_df.head())

        # export เป็น Excel
        output_file = "output.xlsx"
        final_df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Download Excel",
                data=f,
                file_name="split_columns.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
