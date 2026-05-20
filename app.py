import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("data/zomato_final.csv")

st.set_page_config(
    page_title="Zomato Restaurant Intelligence System",
    page_icon="images/Zomato.png",
    layout="wide"
)
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "images/Zomato.png",
        width=200
    )
st.title(" Zomato Restaurant Recommendation System")

st.write(
    "Get restaurant recommendations based on cuisine, rating, budget and online ordering."
)

# Sidebar filters
st.sidebar.header("Restaurant Filters")

# Create cuisine list
cuisine_list = sorted(
    set(
        cuisine.strip()
        for cuisines in df['cuisines'].dropna()
        for cuisine in str(cuisines).split(',')
    )
)

cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    cuisine_list
)

# Location dropdown

location_list = sorted(
    df['location']
    .dropna()
    .unique()
)

location = st.sidebar.selectbox(
    "Select Location",
    ["Any"] + list(location_list)
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    1.0,
    5.0,
    4.0
)

max_cost = st.sidebar.slider(
    "Maximum Cost for Two",
    100,
    3000,
    1000
)

online_order = st.sidebar.selectbox(
    "Online Ordering",
    ["Any", "Yes", "No"]
)

# Recommendation logic
filtered = df[
    (df['cuisines'].str.contains(
        cuisine,
        case=False,
        na=False
    ))
    &
    (df['rate'] >= min_rating)
    &
    (df['approx_cost(for two people)'] <= max_cost)
]

# Apply location filter
if location != "Any":
    
    filtered = filtered[
        filtered['location'] == location
    ]

if online_order != "Any":
    filtered = filtered[
        filtered['online_order'] == online_order
    ]

# Sort best restaurants first
filtered = filtered.sort_values(
    by=['rate','votes'],
    ascending=False
)

# Keep only best occurrence of restaurant
filtered = filtered.drop_duplicates(
    subset=['name','location'],
    keep='first'
)


st.subheader("Recommended Restaurants")

st.subheader("🍽️ Top Restaurant Recommendations")

top_results = filtered.head(20)

if filtered.empty:
    st.warning(
        "No restaurants found. Try changing filters."
    )

else:

    top_results = filtered.head(10)

    for index,row in top_results.iterrows():

        st.markdown(f"""
### {row['name']}

📍 Location: {row['location']}

🍜 Cuisine: {row['cuisines']}

⭐ Rating: {row['rate']}

🗳 Votes: {row['votes']}

💰 Cost for two: ₹{row['approx_cost(for two people)']}

---
""")