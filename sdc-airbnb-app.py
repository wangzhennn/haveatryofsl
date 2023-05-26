!pip install seaborn
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('http://data.insideairbnb.com/denmark/hovedstaden/copenhagen/2022-06-24/visualisations/listings.csv')
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    df['last_review'] = pd.to_datetime(df['last_review']).fillna(pd.Timestamp('1970-01-01'))
    df = df.drop(['neighbourhood_group', 'license'], axis=1)
    # Calculate IQR
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1

    # Define Bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
    return df

df = load_data()


# Sidebar
st.sidebar.header('Filters')
price_min, price_max = st.sidebar.slider('Price range', int(df['price'].min()), int(df['price'].max()), (int(df['price'].min()), int(df['price'].max())))
neighbourhoods = st.sidebar.multiselect('Neighbourhood', df['neighbourhood'].unique())
room_types = st.sidebar.multiselect('Room type', df['room_type'].unique())

# Filter data
df_filtered = df[(df['price'] >= price_min) & (df['price'] <= price_max)]
if neighbourhoods:
    df_filtered = df_filtered[df_filtered['neighbourhood'].isin(neighbourhoods)]
if room_types:
    df_filtered = df_filtered[df_filtered['room_type'].isin(room_types)]

# Main
st.title('Airbnb Copenhagen')

# 1. Price Analysis
st.header('Price Distribution')
fig, ax = plt.subplots()
sns.histplot(df_filtered['price'], kde=True, ax=ax)
st.pyplot(fig)

# 2. Neighbourhood Analysis
st.header('Price Distribution by Neighbourhood')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='neighbourhood', y='price', data=df_filtered, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# 3. Room Type Analysis
st.header('Room Type Counts')
fig, ax = plt.subplots()
sns.countplot(x='room_type', data=df_filtered, ax=ax)
st.pyplot(fig)

st.header('Price Distribution by Room Type')
fig, ax = plt.subplots()
sns.boxplot(x='room_type', y='price', data=df_filtered, ax=ax)
st.pyplot(fig)

# 5. Geographical Analysis
st.header('Geographical Distribution of Listings')
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(x='longitude', y='latitude', hue='price', data=df_filtered, alpha=0.5, ax=ax)
st.pyplot(fig)

# 6. Make a map (Easy)

st.map(df_filtered)
