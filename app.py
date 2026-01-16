import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Setting up the page
st.set_page_config(page_title="Mental Health Worldwide - Interactive Dashboard", page_icon='brain',layout="centered")
st.title(":brain: Mental Health Worldwide")

# Load the data
df = pd.read_csv('mental_health_data.csv')


# DATA CLEANING, FILTERING AND AGGREGATION

# Boolean filters
df['is_treatment_gap'] = (df['Mental_Health_History'] == 'Yes') & (df['treatment'] == 'No')
df['is_stress'] = df['Growing_Stress'] == 'Yes'
df['is_taboo'] = df['mental_health_interview'] == 'No'
df['is_mood_high'] = df['Mood_Swings'] == 'High'
df['is_coping_struggles'] = df['Coping_Struggles'] == 'Yes'
df['is_social_weakness'] = df['Social_Weakness'] == 'Yes'
df['is_family_history'] = df['family_history'] == 'Yes'

# Grouping by country and calculating each index
choropleth_df = df.groupby('Country').agg(
    Count=('Country', 'size'),
    Treatment_Gap=('is_treatment_gap', 'mean'),
    Stress=('is_stress', 'mean'),
    Taboo=('is_taboo', 'mean'),
    Mood_Volatability=('is_mood_high', 'mean'),
    Coping_Struggles=('is_coping_struggles', 'mean'),
    Social_Weakness=('is_social_weakness', 'mean'),
    Family_History=('is_family_history', 'mean')
).reset_index()

# Converting to percentages
cols_to_fix = choropleth_df.columns[2:]
choropleth_df[cols_to_fix] = choropleth_df[cols_to_fix] * 100

# Grouping by gender and calculating each index
donut_df = df.groupby('Gender').agg(
    Count=('Country', 'size'),
    Treatment_Gap=('is_treatment_gap', 'mean'),
    Stress=('is_stress', 'mean'),
    Taboo=('is_taboo', 'mean'),
    Mood_Volatability=('is_mood_high', 'mean'),
    Coping_Struggles=('is_coping_struggles', 'mean'),
    Social_Weakness=('is_social_weakness', 'mean'),
    Family_History=('is_family_history', 'mean')
).reset_index()

# Converting to percentages
donut_df[cols_to_fix] = donut_df[cols_to_fix] * 100

# Grouping by occupation and calculating each index
bar_df = df.groupby('Occupation').agg(
    Count=('Country', 'size'),
    Treatment_Gap=('is_treatment_gap', 'mean'),
    Stress=('is_stress', 'mean'),
    Taboo=('is_taboo', 'mean'),
    Mood_Volatability=('is_mood_high', 'mean'),
    Coping_Struggles=('is_coping_struggles', 'mean'),
    Social_Weakness=('is_social_weakness', 'mean'),
    Family_History=('is_family_history', 'mean')
).reset_index()

# Converting to percentages
bar_df[cols_to_fix] = bar_df[cols_to_fix] * 100



# VISUALIZATION AND FUNCTIONALITY

# Dictionary for connecting front-end to back-end
indicator_map = {
    "Treatment Gap": "Treatment_Gap",
    "Growing Stress": "Stress",
    "Social Taboo": "Taboo",
    "Mood Volatility": "Mood_Volatability",
    "Coping Struggles": "Coping_Struggles",
    "Social Weakness": "Social_Weakness",
    "Family History": "Family_History"
}

# Add a side bar for category selection
st.sidebar.header("Filter by Index")
selection = st.sidebar.selectbox("Select Index below",
                           list(indicator_map.keys()),
                           index=0  # default index = Treatment Gap
                           )

# Mapping the user selection to the real index
idx = indicator_map[selection]

# Row 1: World Map Choropleth - Visualization and functionality

# Create a title for the choropleth
st.subheader("World Map ")


# create the choropleth figure
fig = px.choropleth(
    choropleth_df, 
    locations="Country",
    locationmode="country names",
    color=idx,
    labels={idx: f"{selection} Index"},
    title=f"Distribution of {selection} Index Across the World", 
    hover_name='Country',
    hover_data={'Country':False, 'Count':True},
    color_continuous_scale="Reds",
)
fig.update_layout(coloraxis_colorbar_ticksuffix="%")

# display figure in dashboard
st.plotly_chart(fig, use_container_width=True)

# Row 3 - separate into 2 columns
col1, col2 = st.columns((2))

# Row 3 Column 1: Gender donut chart
with col1:
    #formatted_states = ", ".join(state_list)
    st.subheader(" Male vs Female")

    fig = px.pie(
        donut_df, 
        values=idx,    
        names='Gender',    
        hole=0.4,
        hover_name='Gender',
        hover_data = {'Gender':False, 'Count':True},
        title=f"{selection} Index Between Genders",
        color_discrete_sequence=px.colors.qualitative.Set1 # Επιλογή χρωμάτων
        )
    
    st.plotly_chart(fig, use_container_width=True)

# Row 3 Column 2: Profession Bar Chart
with col2:
    st.subheader("Occupations")

    fig = px.bar(
        bar_df, 
        x='Occupation', 
        y=idx,
        labels={'Mood_Volatability': 'Mood Volatability Index'},
        text_auto='.2f',
        title=f"{selection} Index Across Occupations",
        color='Occupation', 
        color_discrete_sequence=px.colors.qualitative.Set1
        )
    
    fig.update_layout(
    xaxis={'categoryorder':'total descending'},
    showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# Row 3: Raw Data Sample + button

st.subheader("Raw Data Sample")
st.download_button("Download Raw Data", data=df.to_csv(), file_name="mental_health_data.csv")
st.dataframe(df.head())

