import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zomato Data Analysis", layout="wide")
st.title("🍽️ Zomato Restaurant Data Analysis Dashboard")

# File upload
uploaded_file = st.file_uploader("📤 Upload Zomato CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully")

    # -----------------------------
    # Data Cleaning
    # -----------------------------
    if 'rate' in df.columns:
        df['rate'] = df['rate'].astype(str).str.split('/').str[0]
        df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

    if 'approx_cost(for two people)' in df.columns:
        df['approx_cost(for two people)'] = (
            df['approx_cost(for two people)']
            .astype(str)
            .str.replace(',', '')
        )
        df['approx_cost(for two people)'] = pd.to_numeric(
            df['approx_cost(for two people)'], errors='coerce'
        )

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Report Selection
    # -----------------------------
    reports = [
        "Select Report",
        "Total Restaurants Count",
        "Restaurants by Type",
        "Top 10 Restaurants by Votes",
        "Average Rating of Restaurants",
        "Restaurants Offering Online Order",
        "Restaurants Offering Table Booking",
        "Average Cost for Two",
        "Most Popular Restaurant Type",
        "City-wise Restaurant Count",
        "Top Rated Restaurant Types",
        "Votes by Restaurant Type",
        "Online Order vs Offline Restaurants",
        "Cost Distribution by Restaurant Type",
        "High Rated & Low Cost Restaurants"
    ]

    choice = st.selectbox("📈 Choose an analysis", reports)

    # -----------------------------
    # Reports
    # -----------------------------
    if choice == "Total Restaurants Count":
        st.metric("🍴 Total Restaurants", df.shape[0])

    elif choice == "Restaurants by Type":
        type_count = df['listed_in(type)'].value_counts().head(10)
        st.bar_chart(type_count)

    elif choice == "Top 10 Restaurants by Votes":
        top_votes = df[['name', 'votes']].sort_values(by='votes', ascending=False).head(10)
        st.dataframe(top_votes)

    elif choice == "Average Rating of Restaurants":
        st.metric("⭐ Average Rating", round(df['rate'].mean(), 2))

    elif choice == "Restaurants Offering Online Order":
        online = df['online_order'].value_counts()
        st.bar_chart(online)

    elif choice == "Restaurants Offering Table Booking":
        table = df['book_table'].value_counts()
        st.bar_chart(table)

    elif choice == "Average Cost for Two":
        st.metric(
            "💰 Avg Cost for Two",
            f"{int(df['approx_cost(for two people)'].mean())}"
        )

    elif choice == "Most Popular Restaurant Type":
        popular = df['listed_in(type)'].value_counts().idxmax()
        st.write(f"🔥 Most Popular Type: **{popular}**")

    elif choice == "City-wise Restaurant Count":
        city_count = df['listed_in(city)'].value_counts().head(10)
        st.bar_chart(city_count)

    elif choice == "Top Rated Restaurant Types":
        top_rated = df.groupby('listed_in(type)')['rate'].mean().sort_values(ascending=False)
        st.bar_chart(top_rated)

    elif choice == "Votes by Restaurant Type":
        votes_type = df.groupby('listed_in(type)')['votes'].sum().sort_values(ascending=False)
        st.bar_chart(votes_type)

    elif choice == "Online Order vs Offline Restaurants":
        online_vs_offline = df.groupby('online_order').size()
        st.bar_chart(online_vs_offline)

    elif choice == "Cost Distribution by Restaurant Type":
        cost_type = df.groupby('listed_in(type)')['approx_cost(for two people)'].mean()
        st.bar_chart(cost_type)

    elif choice == "High Rated & Low Cost Restaurants":
        avg_rate = df['rate'].mean()
        avg_cost = df['approx_cost(for two people)'].mean()

        filtered = df[
            (df['rate'] > avg_rate) &
            (df['approx_cost(for two people)'] < avg_cost)
        ][['name', 'rate', 'approx_cost(for two people)']].head(10)

        st.dataframe(filtered)

else:
    st.info("👆 Upload a Zomato CSV file to start analysis")
