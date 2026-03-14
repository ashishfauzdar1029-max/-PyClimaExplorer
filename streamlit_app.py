import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Climate Data Dashboard")

data = {
    "Year": [1995, 2000, 2005, 2010, 2015],
    "Temperature": [24.1, 24.5, 24.9, 25.2, 25.8]
}

df = pd.DataFrame(data)

st.write("Climate Temperature Data")
st.dataframe(df)

st.line_chart(df.set_index("Year"))
