# Import Streamlit to create the web application

import streamlit as st

# Import MySQL connector to connect Python with MySQL
import mysql.connector

# Import Pandas to display SQL results as tables
import pandas as pd
# Import Plotly for interactive charts
import plotly.express as px

# Display the project title
st.title("Global Seismic Trends")

# Display the project description
st.write("Data-Driven Earthquake Insights")

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Uwais@2012",
    database="global_seismic_trends"
)

# Check whether the database connection is successful
if connection.is_connected():
    st.success("MySQL database connected successfully!")

# Create a cursor to execute SQL queries
cursor = connection.cursor()
# Display the dashboard heading
st.header("📊 Earthquake Dashboard")

# Display a short description
st.write("Interactive overview of global earthquake activity based on USGS data.")

# -------------------- KPI CARDS --------------------

# Get the total number of earthquakes
cursor.execute("""
    SELECT COUNT(*)
    FROM earthquakes
""")
total_earthquakes = cursor.fetchone()[0]

# Get the highest earthquake magnitude
cursor.execute("""
    SELECT MAX(mag)
    FROM earthquakes
""")
highest_magnitude = cursor.fetchone()[0]

# Get the deepest earthquake
cursor.execute("""
    SELECT MAX(depth_km)
    FROM earthquakes
""")
deepest_earthquake = cursor.fetchone()[0]

# Get the total number of tsunami events
cursor.execute("""
    SELECT COUNT(*)
    FROM earthquakes
    WHERE tsunami = 1
""")
tsunami_events = cursor.fetchone()[0]

# Create four dashboard columns
col1, col2, col3, col4 = st.columns(4)

# Display total earthquakes
col1.metric("🌍 Total Earthquakes", f"{total_earthquakes:,}")

# Display highest magnitude
col2.metric("💥 Highest Magnitude", f"{highest_magnitude:.1f}")

# Display deepest earthquake
col3.metric("⬇️ Deepest (km)", f"{deepest_earthquake:,.1f}")

# Display tsunami events
col4.metric("🌊 Tsunami Events", f"{tsunami_events:,}")


# -------------------- YEARLY TREND --------------------

# Display yearly earthquake trend heading
st.subheader("📈 Earthquakes by Year")

# Get yearly earthquake counts
cursor.execute("""
    SELECT year, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY year
    ORDER BY year
""")

# Get yearly results
results = cursor.fetchall()

# Convert results into a DataFrame
yearly_df = pd.DataFrame(
    results,
    columns=["Year", "Earthquake Count"]
)

# Create an interactive line chart
fig_year = px.line(
    yearly_df,
    x="Year",
    y="Earthquake Count",
    markers=True,
    title="Earthquake Activity by Year"
)

# Display the chart
st.plotly_chart(fig_year, use_container_width=True)


# -------------------- MONTHLY DISTRIBUTION --------------------

# Display monthly analysis heading
st.subheader("📅 Earthquakes by Month")

# Get monthly earthquake counts
cursor.execute("""
    SELECT month, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY month
    ORDER BY month
""")

# Get monthly results
results = cursor.fetchall()

# Convert results into a DataFrame
monthly_df = pd.DataFrame(
    results,
    columns=["Month", "Earthquake Count"]
)

# Create an interactive bar chart
fig_month = px.bar(
    monthly_df,
    x="Month",
    y="Earthquake Count",
    title="Earthquake Distribution by Month"
)

# Display the chart
st.plotly_chart(fig_month, use_container_width=True)


# -------------------- SHALLOW VS DEEP --------------------

# Display depth analysis heading
st.subheader("📏 Shallow vs Deep Earthquakes")

# Get earthquake counts by depth category
cursor.execute("""
    SELECT depth_category, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY depth_category
""")

# Get depth results
results = cursor.fetchall()

# Convert results into a DataFrame
depth_df = pd.DataFrame(
    results,
    columns=["Depth Category", "Earthquake Count"]
)

# Create a pie chart
fig_depth = px.pie(
    depth_df,
    names="Depth Category",
    values="Earthquake Count",
    title="Shallow vs Deep Earthquakes"
)

# Display the chart
st.plotly_chart(fig_depth, use_container_width=True)


# -------------------- TOP COUNTRIES --------------------

# Display country analysis heading
st.subheader("🌍 Top 10 Countries by Earthquake Count")

# Get top countries by earthquake count
cursor.execute("""
    SELECT country, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY country
    ORDER BY earthquake_count DESC
    LIMIT 10
""")

# Get country results
results = cursor.fetchall()

# Convert results into a DataFrame
country_df = pd.DataFrame(
    results,
    columns=["Country", "Earthquake Count"]
)

# Create a horizontal bar chart
fig_country = px.bar(
    country_df,
    x="Earthquake Count",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Earthquake Count"
)

# Display the chart
st.plotly_chart(fig_country, use_container_width=True)


# -------------------- TSUNAMI ANALYSIS --------------------

# Display tsunami analysis heading
st.subheader("🌊 Tsunami vs Non-Tsunami Earthquakes")

# Get tsunami and non-tsunami counts
cursor.execute("""
    SELECT
        CASE
            WHEN tsunami = 1 THEN 'Tsunami'
            ELSE 'No Tsunami'
        END AS tsunami_status,
        COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY tsunami
""")

# Get tsunami results
results = cursor.fetchall()

# Convert results into a DataFrame
tsunami_df = pd.DataFrame(
    results,
    columns=["Tsunami Status", "Earthquake Count"]
)

# Create a pie chart
fig_tsunami = px.pie(
    tsunami_df,
    names="Tsunami Status",
    values="Earthquake Count",
    title="Tsunami vs Non-Tsunami Events"
)

# Display the chart
st.plotly_chart(fig_tsunami, use_container_width=True)


# -------------------- MAGNITUDE TYPE --------------------

# Display magnitude analysis heading
st.subheader("📊 Average Magnitude by Magnitude Type")

# Get average magnitude for each magnitude type
cursor.execute("""
    SELECT
        magType,
        AVG(mag) AS average_magnitude
    FROM earthquakes
    GROUP BY magType
    ORDER BY average_magnitude DESC
""")

# Get magnitude type results
results = cursor.fetchall()

# Convert results into a DataFrame
magtype_df = pd.DataFrame(
    results,
    columns=["Magnitude Type", "Average Magnitude"]
)

# Create a bar chart
fig_magtype = px.bar(
    magtype_df,
    x="Magnitude Type",
    y="Average Magnitude",
    title="Average Magnitude by Magnitude Type"
)

# Display the chart
st.plotly_chart(fig_magtype, use_container_width=True)


# -------------------- STRONGEST EARTHQUAKES --------------------

# Display strongest earthquakes heading
st.subheader("🏆 Top 10 Strongest Earthquakes")

# Get the strongest earthquakes
cursor.execute("""
    SELECT
        id,
        time,
        country,
        place,
        mag,
        depth_km
    FROM earthquakes
    ORDER BY mag DESC
    LIMIT 10
""")

# Get strongest earthquake results
results = cursor.fetchall()

# Convert results into a DataFrame
strongest_df = pd.DataFrame(
    results,
    columns=[
        "ID",
        "Time",
        "Country",
        "Place",
        "Magnitude",
        "Depth (km)"
    ]
)

# Display the strongest earthquakes
st.dataframe(
    strongest_df,
    use_container_width=True
)


# -------------------- SEPARATOR --------------------

# Add a separator before SQL analysis
st.divider()

# Display the SQL analysis heading
st.header("🔎 SQL Analysis")
# Display the SQL analysis heading


# Display Question 1
st.subheader("What are the top 10 strongest earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT id, time, country, place, mag, depth_km
    FROM earthquakes
    ORDER BY mag DESC
    LIMIT 10
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["ID", "Time", "Country", "Place", "Magnitude", "Depth (km)"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 2
st.subheader("What are the top 10 deepest earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT id, time, country, place, depth_km, mag
    FROM earthquakes
    ORDER BY depth_km DESC
    LIMIT 10
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["ID", "Time", "Country", "Place", "Depth (km)", "Magnitude"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 3
st.subheader("Which shallow earthquakes have magnitude greater than 7.5?")

# Run the SQL query
cursor.execute("""
    SELECT id, time, country, place, depth_km, mag
    FROM earthquakes
    WHERE depth_km < 50
    AND mag > 7.5
    ORDER BY mag DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["ID", "Time", "Country", "Place", "Depth (km)", "Magnitude"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 5
st.subheader("What is the average magnitude for each magnitude type?")

# Run the SQL query
cursor.execute("""
    SELECT magType, AVG(mag) AS average_magnitude
    FROM earthquakes
    GROUP BY magType
    ORDER BY average_magnitude DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Magnitude Type", "Average Magnitude"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 6
st.subheader("Which year had the most earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT year, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY year
    ORDER BY earthquake_count DESC
    LIMIT 1
""")

# Get the result from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the result
results_df = pd.DataFrame(
    results,
    columns=["Year", "Earthquake Count"]
)

# Display the result in Streamlit
st.dataframe(results_df)
# Display Question 7
st.subheader("Which month had the most earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT month, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY month
    ORDER BY earthquake_count DESC
    LIMIT 1
""")

# Get the result from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the result
results_df = pd.DataFrame(
    results,
    columns=["Month", "Earthquake Count"]
)

# Display the result in Streamlit
st.dataframe(results_df)
# Display Question 8
st.subheader("Which day of the week had the most earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT day_of_week, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY day_of_week
    ORDER BY earthquake_count DESC
    LIMIT 1
""")

# Get the result from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the result
results_df = pd.DataFrame(
    results,
    columns=["Day of Week", "Earthquake Count"]
)

# Display the result in Streamlit
st.dataframe(results_df)
# Display Question 9
st.subheader("How many earthquakes occurred during each hour of the day?")

# Run the SQL query
cursor.execute("""
    SELECT HOUR(time) AS hour_of_day, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY HOUR(time)
    ORDER BY hour_of_day
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Hour of Day", "Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 10
st.subheader("Which is the most active reporting network?")

# Run the SQL query
cursor.execute("""
    SELECT net, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY net
    ORDER BY earthquake_count DESC
    LIMIT 1
""")

# Get the result from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the result
results_df = pd.DataFrame(
    results,
    columns=["Reporting Network", "Earthquake Count"]
)

# Display the result in Streamlit
st.dataframe(results_df)
# Display Question 11
st.subheader("Which 5 places have the highest number of earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT place, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY place
    ORDER BY earthquake_count DESC
    LIMIT 5
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Place", "Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 14
st.subheader("How many earthquakes were reviewed vs automatic?")

# Run the SQL query
cursor.execute("""
    SELECT status, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY status
    ORDER BY earthquake_count DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Status", "Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 15
st.subheader("What is the count of earthquakes by earthquake type?")

# Run the SQL query
cursor.execute("""
    SELECT type, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY type
    ORDER BY earthquake_count DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Earthquake Type", "Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 16
st.subheader("What is the number of earthquakes by data type?")

# Run the SQL query
cursor.execute("""
    SELECT types, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY types
    ORDER BY earthquake_count DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Data Type", "Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 18
st.subheader("Which events have high station coverage (nst > 100)?")

# Run the SQL query
cursor.execute("""
    SELECT id, time, country, place, nst
    FROM earthquakes
    WHERE nst > 100
    ORDER BY nst DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["ID", "Time", "Country", "Place", "Station Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 19
st.subheader("How many tsunamis were triggered per year?")

# Run the SQL query
cursor.execute("""
    SELECT year, COUNT(*) AS tsunami_count
    FROM earthquakes
    WHERE tsunami = 1
    GROUP BY year
    ORDER BY year
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Year", "Tsunami Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 20
st.subheader("What is the count of earthquakes by depth category?")

# Run the SQL query
cursor.execute("""
    SELECT depth_category, COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY depth_category
    ORDER BY earthquake_count DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Depth Category", "Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 21
st.subheader("What are the top 5 countries with the highest average magnitude?")

# Run the SQL query
cursor.execute("""
    SELECT country, AVG(mag) AS average_magnitude
    FROM earthquakes
    GROUP BY country
    ORDER BY average_magnitude DESC
    LIMIT 5
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Country", "Average Magnitude"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 22
st.subheader("Which countries experienced both shallow and deep earthquakes within the same month?")

# Run the SQL query
cursor.execute("""
    SELECT country, year, month
    FROM earthquakes
    GROUP BY country, year, month
    HAVING COUNT(DISTINCT depth_category) = 2
    ORDER BY country, year, month
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Country", "Year", "Month"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 23
st.subheader("What is the year-over-year growth rate in the total number of earthquakes globally?")

# Run the SQL query
cursor.execute("""
    SELECT
        year,
        COUNT(*) AS earthquake_count,
        ROUND(
            (
                (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year))
                / LAG(COUNT(*)) OVER (ORDER BY year)
            ) * 100,
            2
        ) AS growth_rate_percent
    FROM earthquakes
    GROUP BY year
    ORDER BY year
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Year", "Earthquake Count", "Growth Rate (%)"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 24
st.subheader("What are the 3 most seismically active regions?")

# Run the SQL query
cursor.execute("""
    SELECT
        country,
        COUNT(*) AS earthquake_count,
        ROUND(AVG(mag), 2) AS average_magnitude
    FROM earthquakes
    GROUP BY country
    ORDER BY earthquake_count DESC, average_magnitude DESC
    LIMIT 3
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Country", "Earthquake Count", "Average Magnitude"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 25
st.subheader("What is the average depth of earthquakes within ±5° latitude of the equator?")

# Run the SQL query
cursor.execute("""
    SELECT
        country,
        ROUND(AVG(depth_km), 2) AS average_depth_km
    FROM earthquakes
    WHERE latitude BETWEEN -5 AND 5
    GROUP BY country
    ORDER BY average_depth_km DESC
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Country", "Average Depth (km)"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 26
st.subheader("Which countries have the highest ratio of shallow to deep earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT
        country,
        SUM(CASE WHEN depth_category = 'Shallow' THEN 1 ELSE 0 END) AS shallow_count,
        SUM(CASE WHEN depth_category = 'Deep' THEN 1 ELSE 0 END) AS deep_count,
        ROUND(
            SUM(CASE WHEN depth_category = 'Shallow' THEN 1 ELSE 0 END)
            / NULLIF(SUM(CASE WHEN depth_category = 'Deep' THEN 1 ELSE 0 END), 0),
            2
        ) AS shallow_to_deep_ratio
    FROM earthquakes
    GROUP BY country
    HAVING deep_count > 0
    ORDER BY shallow_to_deep_ratio DESC
    LIMIT 10
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Country", "Shallow Count", "Deep Count", "Shallow-to-Deep Ratio"]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 27
st.subheader("What is the average magnitude difference between earthquakes with tsunami alerts and those without?")

# Run the SQL query
cursor.execute("""
    SELECT
        AVG(CASE WHEN tsunami = 1 THEN mag END) AS average_magnitude_with_tsunami,
        AVG(CASE WHEN tsunami = 0 THEN mag END) AS average_magnitude_without_tsunami,
        AVG(CASE WHEN tsunami = 1 THEN mag END)
        - AVG(CASE WHEN tsunami = 0 THEN mag END) AS magnitude_difference
    FROM earthquakes
""")

# Get the result from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the result
results_df = pd.DataFrame(
    results,
    columns=[
        "Average Magnitude With Tsunami",
        "Average Magnitude Without Tsunami",
        "Magnitude Difference"
    ]
)

# Display the result in Streamlit
st.dataframe(results_df)
# Display Question 28
st.subheader("Which events have the lowest data reliability?")

# Run the SQL query
cursor.execute("""
    SELECT
        id,
        time,
        country,
        place,
        gap,
        rms,
        ROUND((gap + rms) / 2, 2) AS average_error_margin
    FROM earthquakes
    WHERE gap IS NOT NULL
    AND rms IS NOT NULL
    ORDER BY average_error_margin DESC
    LIMIT 10
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=[
        "ID",
        "Time",
        "Country",
        "Place",
        "Gap",
        "RMS",
        "Average Error Margin"
    ]
)

# Display the results in Streamlit
st.dataframe(results_df)
# Display Question 30
st.subheader("Which countries have the highest frequency of deep-focus earthquakes?")

# Run the SQL query
cursor.execute("""
    SELECT
        country,
        COUNT(*) AS deep_earthquake_count
    FROM earthquakes
    WHERE depth_km > 300
    GROUP BY country
    ORDER BY deep_earthquake_count DESC
    LIMIT 10
""")

# Get the results from MySQL
results = cursor.fetchall()

# Create a DataFrame to display the results
results_df = pd.DataFrame(
    results,
    columns=["Country", "Deep Earthquake Count"]
)

# Display the results in Streamlit
st.dataframe(results_df)