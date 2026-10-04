# Import Streamlit to create the dashboard
import streamlit as st

# Import MySQL connector
import mysql.connector

# Set the dashboard title
st.title("Global Seismic Trends")

# Display the description
st.write("Data-Driven Earthquake Insights")
# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Uwais@2012",
    database="global_seismic_trends"
)

# Check whether the connection was successful
if connection.is_connected():
    st.success("MySQL database connected successfully!")
    # Create a cursor to run SQL queries
cursor = connection.cursor()

# Get the total number of earthquakes
cursor.execute("SELECT COUNT(*) FROM earthquakes")

# Get the count from MySQL
total_earthquakes = cursor.fetchone()[0]

# Display the total number on the dashboard
st.metric("Total Earthquakes", total_earthquakes)
# Get the highest earthquake magnitude
cursor.execute("SELECT MAX(mag) FROM earthquakes")

# Get the highest magnitude value
highest_magnitude = cursor.fetchone()[0]

# Display the highest magnitude on the dashboard
st.metric("Highest Magnitude", highest_magnitude)
# Get the deepest earthquake
cursor.execute("SELECT MAX(depth_km) FROM earthquakes")

# Get the maximum depth value
deepest_earthquake = cursor.fetchone()[0]

# Display the deepest earthquake depth
st.metric("Deepest Earthquake (km)", round(deepest_earthquake, 2))
# Count the number of earthquakes that triggered a tsunami
cursor.execute("SELECT COUNT(*) FROM earthquakes WHERE tsunami = 1")

# Get the tsunami event count
tsunami_events = cursor.fetchone()[0]

# Display the tsunami event count
st.metric("Tsunami Events", tsunami_events)
# Get the number of earthquakes recorded in each year
cursor.execute("""
    SELECT year, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY year
    ORDER BY year
""")

# Get the yearly results from MySQL
yearly_data = cursor.fetchall()

# Create a DataFrame for the chart
import pandas as pd
yearly_df = pd.DataFrame(
    yearly_data,
    columns=["Year", "Earthquake Count"]
)

# Display the chart title
st.subheader("Earthquakes by Year")

# Display the yearly earthquake trend
st.line_chart(
    yearly_df.set_index("Year")
)
# Get the number of earthquakes recorded in each month
cursor.execute("""
    SELECT month, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY month
    ORDER BY month
""")

# Get the monthly results from MySQL
monthly_data = cursor.fetchall()

# Create a DataFrame for the chart
monthly_df = pd.DataFrame(
    monthly_data,
    columns=["Month", "Earthquake Count"]
)

# Display the chart title
st.subheader("Earthquakes by Month")

# Display the monthly earthquake trend
st.bar_chart(
    monthly_df.set_index("Month")
)
# Get the number of shallow and deep earthquakes
cursor.execute("""
    SELECT depth_category, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY depth_category
""")

# Get the depth category results from MySQL
depth_data = cursor.fetchall()

# Create a DataFrame for the chart
depth_df = pd.DataFrame(
    depth_data,
    columns=["Depth Category", "Earthquake Count"]
)

# Display the chart title
st.subheader("Earthquakes by Depth Category")

# Display the depth category chart
st.bar_chart(
    depth_df.set_index("Depth Category")
)
# Get the top 10 countries with the most earthquakes
cursor.execute("""
    SELECT country, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY country
    ORDER BY earthquake_count DESC
    LIMIT 10
""")

# Get the country results from MySQL
country_data = cursor.fetchall()

# Create a DataFrame for the chart
country_df = pd.DataFrame(
    country_data,
    columns=["Country", "Earthquake Count"]
)

# Display the chart title
st.subheader("Top 10 Countries by Earthquake Count")

# Display the country chart
st.bar_chart(
    country_df.set_index("Country")
)
# Get the 10 strongest earthquakes
cursor.execute("""
    SELECT country, place, mag, depth_km
    FROM earthquakes
    ORDER BY mag DESC
    LIMIT 10
""")

# Get the strongest earthquake results from MySQL
strongest_data = cursor.fetchall()

# Create a DataFrame for the results
strongest_df = pd.DataFrame(
    strongest_data,
    columns=["Country", "Place", "Magnitude", "Depth (km)"]
)

# Display the chart title
st.subheader("Top 10 Strongest Earthquakes")

# Display the earthquake details
st.dataframe(strongest_df)
# Get the number of tsunami and non-tsunami earthquakes
cursor.execute("""
    SELECT tsunami, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY tsunami
""")

# Get the tsunami results from MySQL
tsunami_data = cursor.fetchall()

# Create a DataFrame for the chart
tsunami_df = pd.DataFrame(
    tsunami_data,
    columns=["Tsunami", "Earthquake Count"]
)

# Change 0 and 1 into readable names
tsunami_df["Tsunami"] = tsunami_df["Tsunami"].map({
    0: "No Tsunami",
    1: "Tsunami"
})

# Display the chart title
st.subheader("Tsunami vs Non-Tsunami Earthquakes")

# Display the tsunami chart
st.bar_chart(
    tsunami_df.set_index("Tsunami")
)