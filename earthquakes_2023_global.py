# -*- coding: utf-8 -*-
"""Earthquakes-2023-Global.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IYcnJ9WWtT1CTalm6H9TVKFmvO2fX_s0

# **Data Visualization Activity**

## **Part 1 - Course 8 Module 1 & 2 Activity**

---
### **0. Instruction**

Using a dataset of your choice, create a visualization of the data using the tool assigned to your group. Try to implement using various libraries/packages; matplotlib, seaborn, plotly. Explain how your group approached your implementation and what you can gather about the data from your visualizations. Is this tool the most appropriate for representing/analyzing your selected dataset?

Resources for exploring Plotly packages:
https://plotly.com/python/plotly-express/

---
### **1. Import important libraries and dataset**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

!pip install pywaffle
from pywaffle import Waffle
!pip install geopandas folium
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
!pip install wordcloud
from wordcloud import WordCloud, STOPWORDS

import re

!pip install dash
import dash
from dash import dcc, html, Input, Output
import io
import base64


df = pd.read_csv("https://drive.usercontent.google.com/u/0/uc?id=19RC3uFny9DFVBeZfbXPJKkpfTlkmwkc5")
df.head()

"""---
### **2. Data Summary**


"""

df.describe()

df.info()

df.columns

"""---
### **3. Cleaning Data**

#### **a. Remove Missing Values**
"""

df.isnull().sum()

df.dropna(inplace=True)

df.isnull().sum()

"""#### **b. Remove Duplicate Rows**"""

df.duplicated().sum()

df.drop_duplicates(inplace=True)

df.duplicated().sum()

"""#### **c. Remove Irrelevant Columns**"""

df.drop(columns=df.columns.difference(['time', 'latitude', 'longitude', 'depth', 'mag', 'place']), inplace=True)
df.head()

"""#### **d. Convert Data Types**"""

# The 'time' column is parsed as datetime
df['time'] = pd.to_datetime(df['time'])
df.head()

"""---
### **4. Feature Engineering**

#### **a. Create New Columns**
"""

df['region'] = df['place'].str.extract(r'\s*([^,]*|[^,]+)$')
df

"""---
### **5. Data Visualization**

#### **a. Data Aggregation and Grouping**
"""

# Group by region and month then count the total number of earthquakes
region_monthly_counts = df.groupby(['region', pd.Grouper(key='time', freq='MS')]).size().reset_index(name='count')
region_monthly_counts

# Extract month and year which are necessary for the charts below and reassign it to time column
region_monthly_counts['time'] = region_monthly_counts['time'].dt.strftime('%Y-%m')

# Reorder column names in Data Frame
region_monthly_counts = region_monthly_counts[['time', 'region', 'count']]
region_monthly_counts

# Calculate total earthquakes of top 5 regions
top_regions_counts = region_monthly_counts.groupby('region')['count'].sum().nlargest(5)
top_regions_counts

top_regions = top_regions_counts.index.tolist()
top_regions

# Filter data for top 5 regions
filtered_data = region_monthly_counts[region_monthly_counts['region'].isin(top_regions)]
filtered_data

region_data = filtered_data[filtered_data['region'] == 'Indonesia']
region_data

"""#### **b. Plot Area Charts**

##### **Matplotlib**
"""

# Create area chart using Matplotlib
plt.figure(figsize=(14, 7))

for region in top_regions:
    region_data = filtered_data[filtered_data['region'] == region]  # Get 12 data points (12 months) for each region
    plt.plot(region_data['time'], region_data['count'], label=region)
    plt.fill_between(region_data['time'], region_data['count'], alpha=0.3)

plt.title("Monthly Earthquake Counts by Top 5 Regions")
plt.xlabel("Date")
plt.ylabel("Number of Earthquakes")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

"""##### **Seaborn**"""

# Create an area chart using Seaborn
plt.figure(figsize=(14, 7))

for region in top_regions:
    region_data = filtered_data[filtered_data['region'] == region]
    sns.lineplot(x='time', y='count', data=region_data, label=region)  # Use sns.lineplot for area chart
    plt.fill_between(region_data['time'], region_data['count'], alpha=0.3)  # Fill area

plt.title("Monthly Earthquake Counts by Top 5 Regions")
plt.xlabel("Date")
plt.ylabel("Number of Earthquakes")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

"""##### **Plotly**"""

# Create an area chart using Plotly
fig_area_chart = go.Figure()

for region in top_regions:
    region_data = filtered_data[filtered_data['region'] == region]
    fig_area_chart.add_trace(go.Scatter(
        x=region_data['time'],
        y=region_data['count'],
        fill='tozeroy',           # Fill to zero on y-axis
        name=region              # Assign region name
    ))

fig_area_chart.update_layout(
    title="Monthly Earthquake Counts by Top 5 Regions",
    xaxis_title="Date",
    yaxis_title="Number of Earthquakes",
    xaxis_tickangle=-45
)

fig_area_chart.show()

"""---
## **Part 2 - Course 8 Module 3 Activity**

---
### **0. Instruction**

In the same groups and using the same datasets you selected in Part 1, choose one or two charts from the list below that are better for visualizing your chosen dataset or help tell the story hidden in your sample.

* Word Clouds
* Seaborn & Waffle charts
* Regression Plots
* Visualizing Geospatial Data - Folium, maps with markers & Choropleth maps
<br><br/>

_Resources for exploring word cloud packages:_

https://medium.com/mlearning-ai/wordclouds-with-python-c287887acc8b

https://www.geeksforgeeks.org/generating-word-cloud-python/

https://python-charts.com/part-whole/waffle-chart-matplotlib/

https://towardsdatascience.com/how-to-create-beautiful-waffle-charts-for-data-visualisation-in-python-e9760a3f8594

---
### **1. Count Plot**
"""

# Create the count plot with the top 5 regions and adjust aesthetics
fig_count_plot = plt.figure(figsize=(12, 6))
ax = sns.countplot(
    x=df['region'],
    order=top_regions,
    edgecolor="black",
    linewidth=1.5,
    legend=False,    # Set legend to False to avoid redundant legend
    dodge=False     # Prevent bars from being grouped (for single-color bars)
)

# Set individual bar colors
palette = sns.color_palette("viridis", n_colors=len(top_regions))
for i, bar in enumerate(ax.patches):
    bar.set_facecolor(palette[i])

plt.title("Earthquake Counts by Top 5 Regions", fontsize=16, pad=20)
plt.xlabel("Region")
plt.ylabel("Number of Earthquakes")
plt.tight_layout()
plt.show()

"""---
### **2. Word Cloud**
"""

text = ' '.join(df['place'].astype(str).tolist())
my_stopwords=set(STOPWORDS)
my_stopwords.update(["km","S","W","SW","SSW","WSW","WNW","NW","NNW","E","N","NE","SE","SSE","ENE","ESE","NNE"])

# Create a WordCloud object
wordcloud = WordCloud(
    width=400,
    height=400,
    background_color='Lightblue',
    stopwords=my_stopwords,
    min_font_size=10,
    colormap='viridis'
).generate(text)

# Display the generated image:
fig_word_cloud = plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Frequent Earthquake Locations", fontsize=16, pad=20)
plt.tight_layout(pad=0)
plt.show()

"""---
### **3. Waffle Chart**
"""

# Set up the Waffle chart figure
fig_waffle_plot = plt.figure(
    FigureClass=Waffle,
    figsize=(10, 6),
    rows=20, columns=30,
    values=top_regions_counts.values,
    cmap_name='tab20',
    legend = {
      'labels': [f"{k} ({v})" for k, v in zip(top_regions_counts.index,top_regions_counts.values)],
      'loc': 'upper left',
      'bbox_to_anchor':(1.05,1)
    }
)

plt.title("Earthquake Proportions by Region", fontsize=16, pad=20)
plt.show()

"""---
## **Part 3 - Course 8 Module 4 Activity**

---
### **0. Instruction**

In the same groups and using the same datasets that you selected in Part 1&2, implement a simple dashboard.

_Resources for exploring Plotly/Dash packages:_

* https://medium.com/plotly/introducing-dash-5ecf7191b503

* https://medium.com/swlh/dashboards-in-python-3-advanced-examples-for-dash-beginners-and-everyone-else-b1daf4e2ec0a

* https://medium.com/swlh/dashboards-in-python-3-advanced-examples-for-dash-beginners-and-everyone-else-b1daf4e2ec0a

* https://github.com/ucg8j/awesome-dash

* https://dash.plotly.com/

---
### **1. Dashboard**
"""

buf = io.BytesIO()

# Save Count Plot as image
fig_count_plot.savefig(buf, format='png', bbox_inches='tight')
buf.seek(0)
count_plot_img_base64 = base64.b64encode(buf.read()).decode('utf-8')
buf.truncate(0)  # Clear buffer contents
buf.seek(0)      # Reset pointer to the start

# Save Word Cloud as image
fig_word_cloud.savefig(buf, format='png', bbox_inches='tight')
buf.seek(0)
wordcloud_img_base64 = base64.b64encode(buf.read()).decode('utf-8')
buf.truncate(0)  # Clear buffer contents
buf.seek(0)      # Reset pointer to the start

# Save Waffle Chart as image
fig_waffle_plot.savefig(buf, format='png', bbox_inches='tight')
buf.seek(0)
waffle_img_base64 = base64.b64encode(buf.read()).decode('utf-8')

buf.close()  # Done -> Close the buffer

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#f8f9fa',  # Light gray background
        'padding': '20px',
        'fontFamily': 'Arial, sans-serif'
    },
    children=[
        html.H1("Earthquake Data Dashboard", style={'textAlign': 'center'}),

        # Area Chart
        html.Div([
            html.H2("Area Chart:"),
            dcc.Graph(id='area-chart', figure=fig_area_chart)
        ]),

        # Count Plot
        html.Div([
            html.H2("Count Plot:"),
            html.Img(src=f'data:image/png;base64,{count_plot_img_base64}', style={'width': '60%', 'height': 'auto'})
        ]),

        # Word Cloud
        html.Div([
            html.H2("Word Cloud:"),
            html.Img(src=f'data:image/png;base64,{wordcloud_img_base64}', style={'width': '60%', 'height': 'auto'})
        ]),

        # Waffle Chart
        html.Div([
            html.H2("Waffle Chart:"),
            html.Img(src=f"data:image/png;base64,{waffle_img_base64}", style={'width': '60%', 'height': 'auto'})
        ])
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)

"""<br><br/>

---
### **Comments**
"""

# from google.colab import files
# uploaded = files.upload()

# from google.colab import drive

# # Step 1: Mount Google Drive
# drive.mount('/content/drive')

# # Step 2: Access your file
# file_path = '/content/drive/My Drive/Colab Notebooks/earthquakes_2023_global.csv'  # Change this to your file's path

#dfpv=df.pivot_table(index=['time', 'latitude', 'longitude', 'depth', 'mag', 'place'],aggfunc='size')
#dfpv

# Comparison of approaches for extracting 'region' from 'place':

# Feature	          Approach 1 (apply with lambda)	                      Approach 2 (str.extract)
# Performance	      Generally slower for large datasets                   Generally faster for large datasets
# Readability	      Can be less readable due to the lambda function       More concise and readable
# Handling no       match	Assigns None	                                  Assigns NaN
# Flexibility	      More flexible for complex logic                       More limited in terms of logic

# Recommendation:
#   - For simple regex extraction, which extracts the first captured group, and large datasets,
#     `str.extract` is preferred due to its performance and readability.
#   - For complex logic or custom handling of no matches, `apply` with lambda
#     might be more suitable.

# # Method 1:
# df['region'] = df['place'].apply(
#     lambda x: re.search(r'\s*([^,]*|[^,]+)$', x).group(1)
#       if re.search(r'\s*([^,]*|[^,]+)$', x)
#       else None
# )

# # Method 2:
# df['region'] = df['place'].str.extract(r'\s*([^,]*|[^,]+)$')

# df

# # Group by day and count earthquakes
# daily_counts = df.resample('D', on='time').size()
# daily_counts

# # Filter data for top 5 regions
# # Method #1
# filtered_data = region_monthly_counts[region_monthly_counts['region'].isin(top_regions)]
# filtered_data

# # Method #2:
# mask = [region in top_regions for region in region_monthly_counts['region']]
# filtered_data = region_monthly_counts[mask]
# filtered_data

"""##### **Data Series Conversion**"""

# # Convert the series to a DataFrame for clarity
# daily_counts_df = daily_counts.reset_index()
# daily_counts_df.columns = ['day', 'number_of_earthquakes']
# daily_counts_df

# # Plot area chart
# plt.figure(figsize=(14, 7))
# plt.plot(daily_counts_df['day'], daily_counts_df['number_of_earthquakes'], color="Green", linewidth=1.5)
# plt.fill_between(daily_counts.index, daily_counts, color="Yellow", alpha=0.5)
# plt.title("Daily Earthquake Counts")
# plt.xlabel("Date")
# plt.ylabel("Number of Earthquakes")
# plt.show()

# --------------------------------------

# df_grouped = df.groupby('time')['mag'].mean().reset_index()
# sns.lineplot(x='time', y='mag', data=df_grouped)
# plt.fill_between(df_grouped['time'], df_grouped['mag'], alpha=0.3)  # Fill area under the line
# plt.title("Area Plot of Earthquakes")
# plt.xlabel("Time")
# plt.ylabel("Average Magnitude")
# plt.show()

# --------------------------------------

# # Create an area chart using Seaborn
# sns.set(style='whitegrid')
# plt.figure(figsize=(14, 7))
# sns.lineplot(
#     data=daily_counts_df,
#     x='day',
#     y='number_of_earthquakes',
#     color="blue",
#     linewidth=1.5,
#     label='Number of Earthquakes',
# ).fill_between(daily_counts.index, daily_counts, color="orange", alpha=0.3)

# # Filter for earthquakes with magnitude greater than 5
# filtered_df = df[df['mag'] > 5]

# # Customize the plot
# plt.title('Daily Golbal Earthquake Counts')
# plt.xlabel('Date')
# plt.ylabel('Number of Earthquakes')
# plt.xticks(rotation=45)
# plt.tight_layout()

# # Show the plot
# plt.show()

# --------------------------------------

# # Create an interactive area chart using Plotly
# fig = px.area(
#     daily_counts_df,
#     x='day',
#     y='number_of_earthquakes',
#     title='<b>Daily Global Earthquake Counts</b>',
#     labels={'day': 'Date', 'number_of_earthquakes': 'Number of Earthquakes'},
#     template='plotly_white',
#     color_discrete_sequence=['red'],
# )

# # Customize layout
# fig.update_traces(fillcolor="lightblue")
# fig.update_layout(
#     xaxis_title='Date',
#     yaxis_title='Number of Earthquakes',
#     xaxis=dict(showgrid=True, gridcolor='lightgray',tickangle=45),
#     yaxis=dict(showgrid=True,gridcolor='lightgray'),
#     title=dict(font=dict(size=22)),
#     hovermode='x unified',
#     font=dict(family="Arial", size=14),
#     plot_bgcolor="lightgray",  # Set plot background color
#     paper_bgcolor="white"  # Set paper (outside plot area) background color
# )

# # Show the chart
# fig.show()