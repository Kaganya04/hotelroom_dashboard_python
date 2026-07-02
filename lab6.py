import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
if not os.path.exists("hotel_rooms.csv"):
    import random
    random.seed(42)
    room_types = ["Single", "Double", "Deluxe", "Suite", "Family"]
    statuses = ["Occupied", "Available"]
    base_price = {"Single": 1500, "Double": 2500, "Deluxe": 4000,
                   "Suite": 6000, "Family": 3500}
    rows = []
    for i in range(101, 161):
        room_type = random.choice(room_types)
        rows.append({
            "Room_ID": i,
            "Room_Type": room_type,
            "Floor": random.randint(1, 5),
            "Price_Per_Night": base_price[room_type] + random.randint(-300, 500),
            "Status": random.choice(statuses),
            "Rating": round(random.uniform(2.5, 5.0), 1),
        })
    pd.DataFrame(rows).to_csv("hotel_rooms.csv", index=False)
st.set_page_config(page_title="Hotel Room Management Dashboard", layout="wide")
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
    }
    .sub-title {
        font-size: 18px;
        color: #444444;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="main-title">Hotel Room Management Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Explore room availability, pricing, and guest ratings interactively.</div>',
    unsafe_allow_html=True,
)
df = pd.read_csv("hotel_rooms.csv")
st.sidebar.header("Filter Rooms")
room_type_filter = st.sidebar.multiselect(
    "Select Room Type",
    options=sorted(df["Room_Type"].unique()),
    default=sorted(df["Room_Type"].unique()),
)
floor_filter = st.sidebar.multiselect(
    "Select Floor",
    options=sorted(df["Floor"].unique()),
    default=sorted(df["Floor"].unique()),
)
min_price = int(df["Price_Per_Night"].min())
max_price = int(df["Price_Per_Night"].max())
price_range = st.sidebar.slider(
    "Price Per Night Range (₹)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
)
filtered_df = df[
    (df["Room_Type"].isin(room_type_filter))
    & (df["Floor"].isin(floor_filter))
    & (df["Price_Per_Night"] >= price_range[0])
    & (df["Price_Per_Night"] <= price_range[1])
]
st.subheader("Room Data")
st.dataframe(filtered_df, use_container_width=True)
st.subheader("Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rooms", len(filtered_df))
col2.metric("Available Rooms", int((filtered_df["Status"] == "Available").sum()))
col3.metric("Occupied Rooms", int((filtered_df["Status"] == "Occupied").sum()))
col4.metric("Avg. Price (₹)", round(filtered_df["Price_Per_Night"].mean(), 2) if len(filtered_df) else 0)
st.write(filtered_df.describe())
st.subheader("Visualizations")
col1, col2 = st.columns(2)
with col1:
    st.write("**Average Price by Room Type**")
    avg_price = filtered_df.groupby("Room_Type")["Price_Per_Night"].mean()
    fig1, ax1 = plt.subplots()
    avg_price.plot(kind="bar", color="#1f77b4", ax=ax1)
    ax1.set_ylabel("Average Price (₹)")
    ax1.set_xlabel("Room Type")
    st.pyplot(fig1)
with col2:
    st.write("**Room Status Distribution**")
    status_counts = filtered_df["Status"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)


col3, col4 = st.columns(2)
with col3:
    st.write("**Price Distribution**")
    fig3, ax3 = plt.subplots()
    ax3.hist(filtered_df["Price_Per_Night"], bins=10, color="#2ca02c", edgecolor="black")
    ax3.set_xlabel("Price Per Night (₹)")
    ax3.set_ylabel("Number of Rooms")
    st.pyplot(fig3)
with col4:
    st.write("**Rating vs Price**")
    fig4, ax4 = plt.subplots()
    ax4.scatter(filtered_df["Rating"], filtered_df["Price_Per_Night"], color="#d62728")
    ax4.set_xlabel("Rating")
    ax4.set_ylabel("Price Per Night (₹)")
    st.pyplot(fig4)
st.subheader("Download Filtered Data")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="filtered_hotel_rooms.csv",
    mime="text/csv",
)
