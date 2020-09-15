""" Streamlit app for portfolio analysis and capital requirements """

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title("Credit risk portfolio analysis and capital requirements")


@st.cache
def load_portfolio():
    """
        Load portfolio data
    """
    data = pd.read_csv("tests/test_data_excel_csv.csv")
    return data


data_load_state = st.text("Loading data...")
data = load_portfolio()
data_load_state.text("Portfolio data has been loaded")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

st.subheader("PD distribution")
plt.hist(data["PD"] * 100, bins=20)
plt.xlabel("PD - Probability of defaults")
plt.ylabel("Number of obligors")
st.pyplot()
