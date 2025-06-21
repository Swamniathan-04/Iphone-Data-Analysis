#!/usr/bin/env python
# coding: utf-8

# In[300]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd


# In[301]:


df = pd.read_csv('Your dataset path')
df.head(5)


# In[249]:


print(df.describe())
print('\n\nRATING SCORE STATS:\n\n') 
df['ratingScore'].describe()


# In[250]:


print(df.info())


# In[251]:


print(df['reviewDescription'].describe(),'\n\n')
print(df['reviewDescription'].info())


# In[252]:


# reviewDescription Total Null Values
print(df['reviewDescription'].isnull().sum())


# In[253]:


df['reviewDescription'].head(5)


# In[11]:


# Function to extract the required fields and clean up '(PRODUCT)'
def extract_info(variant):
    # Find service provider if present, otherwise set to 'Unlocked'
    service_provider_match = re.search(r"Service Provider: ([\w\s]+)", variant)
    
    # Match color before 'Size:' (without needing 'Color:' or 'Colour:' prefix)
    color_match = re.search(r"([\w\s]+)(?=Size:)", variant)
    
    # Match size after 'Size:'
    size_match = re.search(r"Size: (\d+GB|\d+ GB)", variant)
    
    # Extract values or use defaults
    service_provider = service_provider_match.group(1) if service_provider_match else 'Unlocked'
    
    # Extract color and clean it up (remove (PRODUCT) or other unnecessary parts)
    color = color_match.group(1).strip() if color_match else ''
    clean_color = re.sub(r'\(PRODUCT\)\s?', '', color).strip()  # Clean '(PRODUCT)' if present
    
    # Extract size
    size = size_match.group(1).strip() if size_match else ''
    
    return pd.Series([service_provider, clean_color, size])

# Apply the function to split the variant column
df[['Service Provider', 'Color', 'Size']] = df['variant'].apply(extract_info)

# Drop the original 'variant' column
df = df.drop(columns=['variant'])

# Display the resulting DataFrame
print(df.head(1645))


# In[12]:


# delete column 'variant' and rename date column to 'review date'
df = df.drop(columns=['reviewUrl','reviewedIn']).rename(columns={'date': 'Review Date', 'country' : 'Reviewed country'})
print(df.head(4))


# In[254]:


missing_values = df.isnull().sum()
print(f"Missing values:\n{missing_values}")


# In[255]:


df.info()


# In[256]:


# changed the values of Product Asin to Original Product
df


# In[257]:


df[df['Reviewed country'] == 'Japan'].head(5)


# In[258]:


df[df['Reviewed country'] == 'United Arab Emirates'].head(5)


# In[259]:


df[df['Reviewed country'] == 'Egypt']


# In[260]:


# view Unique Column names
df['Reviewed country'].unique()


# In[261]:


# return service provider of all Unlocked and size of all 512 GB
df[df['Service Provider'] == 'Unlocked']
df[df['Size'] == '512 GB']


# In[262]:


# get a brief view Finally for Visuaalization
df.info()


# In[306]:


# Create the histogram
fig = px.histogram(
    df, 
    x='Reviewed country', 
    color='isVerified',
    title='Count of Verified and Non-Verified Reviews by Country',
    labels={'isVerified': 'Verified Review'},
    barmode='group',  # 'group' for side-by-side bars
    height=600,
    opacity = 0.6,
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Plotly
)


# Show the figure
fig.show()

# Create the histogram
fig = px.histogram(
    df, 
    x='Service Provider', 
    color='isVerified',
    title='Count of Verified and Non-Verified Reviews by Service Providers',
    labels={'isVerified': 'Verified Review'},
    barmode='group',  # 'group' for side-by-side bars
    height=600,
    opacity = 0.6,
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# Show the figure
fig.show()


# In[264]:


df['Review Date'] = pd.to_datetime(df['Review Date'], format='%d-%m-%Y', errors='coerce')

# Extract the year
df['Year'] = df['Review Date'].dt.year

# Count reviews per year
yearly_counts = df['Year'].value_counts().sort_index()

# Create a DataFrame for plotting
yearly_counts_df = yearly_counts.reset_index()
yearly_counts_df.columns = ['Year', 'Review Count']

# Create interactive line plot using Plotly
fig = px.line(yearly_counts_df, x='Year', y='Review Count', 
              title='Review Count by Year', 
              markers=True, 
              color_discrete_sequence=px.colors.qualitative.Plotly)

# Customize the layout
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Review Count',
    xaxis_title_font=dict(color='black', size=15),
    yaxis_title_font=dict(color='black', size=15),
    template='plotly_white'
)

# Show the plot
fig.show()


# In[265]:


fig_express = px.histogram(df, x='Color', y='ratingScore', 
                            color='Color', 
                            title='Rating Scores by Color (Plotly Express)',
                            labels={'ratingScore': 'Rating Score', 'Color': 'Color'},
                            barmode='overlay',
                            text_auto=True,
                            height = 600)

# Show the Plotly Express figure
fig_express.show()


# In[266]:


# pie chart
product_count = df['Product'].value_counts().reset_index()
product_count.columns = ['Product', 'Count']

# Create pie chart with white text inside
fig = px.pie(product_count, names='Product', values='Count', title='Percentage of Products Reviewed', opacity = 0.8)

# Update the text inside the pie chart to white
fig.update_traces(textinfo='percent+label', insidetextfont=dict(color='white'))

fig.update_layout(width=1100, height=600, title_x=0.5, title_xanchor='center')

# Display the pie chart
fig.show()


# In[307]:


# Create the histogram
fig = px.histogram(
    df, 
    x='Service Provider', 
    color='Product',
    title='Count of Verified and Non-Verified Reviews by Product',
    labels={'isVerified': 'Verified Review'},
    barmode='group',  # 'group' for side-by-side bars
    height=600,
    opacity = 0.6,
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# Show the figure
fig.show()


# In[309]:


# Create the histogram
fig = px.histogram(
    df, 
    x='Product',
    color='Size',
    title='Count of Verified and Non-Verified Reviews by Storage Size',
    labels={'isVerified': 'Verified Review'},
    barmode='group',  # 'group' for side-by-side bars
    height=600,
    opacity = 0.6,
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# Show the figure
fig.show()

# Create the histogram
fig = px.histogram(
    df, 
    x='Product',
    color='Color',
    title='Count of Verified and Non-Verified Reviews by Storage Size',
    labels={'isVerified': 'Verified Review'},
    barmode='group',  # 'group' for side-by-side bars
    height=600,
    opacity = 0.6,
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# Show the figure
fig.show()


# In[274]:


# pie chart
product_count = df['Reviewed country'].value_counts().reset_index()
product_count.columns = ['Reviewed country', 'Count']

# Create pie chart with white text inside
fig = px.pie(product_count, names='Reviewed country', values='Count', title='Percentage of Products Reviewed', opacity = 0.8)

# Update the text inside the pie chart to white
fig.update_traces(textinfo='percent+label', insidetextfont=dict(color='white'))

fig.update_layout(width=1100, height=600, title_x=0.5, title_xanchor='center')

# Display the pie chart
fig.show()


# In[310]:


# Create the histogram
fig = px.histogram(
    df, 
    x='Reviewed country',
    color='Product',
    title='Count of Verified and Non-Verified Reviews by Storage Size',
    labels={'isVerified': 'Verified Review'},
    barmode='group',  # 'group' for side-by-side bars
    height=600,
    opacity = 0.6,
    text_auto=True,
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# Show the figure
fig.show()


# In[284]:


df['Review Date'] = pd.to_datetime(df['Review Date'])

# Group by 'Reviewed country' and 'Review Date' and calculate the mean rating score
heatmap_data = df.groupby(['Reviewed country', 'Review Date'])['ratingScore'].mean().reset_index()

# Create a heatmap with swapped axes
heatmap_pivot = heatmap_data.pivot(index="Review Date", columns="Reviewed country", values="ratingScore")

# Create the heatmap using imshow
fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Reviewed Country", y="Review Date", color="Average Rating"),
    color_continuous_scale="Viridis"
)

# Update layout
fig.update_layout(title='Heatmap of Average Ratings by Review Date and Country', xaxis_title='Reviewed Country', yaxis_title='Review Date', height = 600)

# Show the heatmap
fig.show()


# In[ ]:




