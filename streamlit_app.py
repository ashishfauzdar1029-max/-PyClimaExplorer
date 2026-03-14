import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Climate Data Dashboard")

data = {
    "Year": [1995, 2000, 2005, 2010, 2015],
    "Temperature": [24.1, 24.5, 24.9, 25.2, 25.8]
}

df = pd.DataFrame(data)

st.write("Climate Temperature Data")import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Climate Explorer Dashboard", layout="wide")

st.title("🌍 Global Climate Explorer Dashboard")
st.markdown("Analyze climate trends using an interactive global heat map and time-series visualization.")

# Sidebar
st.sidebar.header("Upload Climate Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

st.sidebar.markdown("""
### CSV format should include these columns:
- `Country`
- `Year`
- `Temperature`
- `Latitude`
- `Longitude`
""")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    required_cols = {"Country", "Year", "Temperature", "Latitude", "Longitude"}
    if not required_cols.issubset(df.columns):
        st.error("CSV file must contain: Country, Year, Temperature, Latitude, Longitude")
    else:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
        df = df.dropna(subset=["Year", "Temperature", "Latitude", "Longitude"])

        min_year = int(df["Year"].min())
        max_year = int(df["Year"].max())

        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

        countries = sorted(df["Country"].dropna().unique().tolist())
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            options=countries,
            default=countries[:10] if len(countries) > 10 else countries
        )

        filtered_df = df[
            (df["Year"] >= year_range[0]) &
            (df["Year"] <= year_range[1])
        ]

        if selected_countries:
            filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]

        if filtered_df.empty:
            st.warning("No data available for selected filters.")
        else:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📌 Dataset Preview")
                st.dataframe(filtered_df, use_container_width=True)

            with col2:
                st.subheader("📊 Summary")
                st.metric("Total Records", len(filtered_df))
                st.metric("Average Temperature", f"{filtered_df['Temperature'].mean():.2f} °C")
                st.metric("Countries", filtered_df["Country"].nunique())

            st.subheader("🗺 Global Heat Map")

            map_df = (
                filtered_df.groupby(["Country", "Latitude", "Longitude"], as_index=False)["Temperature"]
                .mean()
            )

            fig_map = px.scatter_geo(
                map_df,
                lat="Latitude",
                lon="Longitude",
                color="Temperature",
                hover_name="Country",
                size="Temperature",
                projection="natural earth",
                title="Global Temperature Heat Map",
            )

            fig_map.update_layout(height=600)
            st.plotly_chart(fig_map, use_container_width=True)

            st.subheader("📈 Time-Series Temperature Trend")

            trend_df = (
                filtered_df.groupby(["Year", "Country"], as_index=False)["Temperature"]
                .mean()
            )

            fig_line = px.line(
                trend_df,
                x="Year",
                y="Temperature",
                color="Country",
                markers=True,
                title="Temperature Trend Over Time"
            )

            fig_line.update_layout(height=500)
            st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("Please upload a climate CSV file from the sidebar to start.")
st.dataframe(df)

st.line_chart(df.set_index("Year"))
