
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="Student Stress Dashboard", layout="wide")

# Optional: Add image header (place 'your_image.jpg' in the same folder) 
st.image('stress photo.jpg', use_container_width=True)

st.title("Student Stress & Mental Health Dashboard")

# Load dataset
df = pd.read_csv('StressLevelDataset.csv')

# -------------------------------------------
# Violin Plot: Anxiety Level by Academic Performance
st.header("1. Anxiety Level by Academic Performance")
fig1 = px.violin(
    df,
    x='academic_performance',
    y='anxiety_level',
    box=True,
    points='all',
    color_discrete_sequence=['#FF9800']
)
fig1.update_layout(
    xaxis_title='Academic Performance',
    yaxis_title='Anxiety Level'
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------
# Bar Plot: Average Anxiety by Study Load
st.header("2. Average Anxiety by Study Load")
bar_data = df.groupby('study_load')['anxiety_level'].mean().reset_index()
fig2 = px.bar(
    bar_data,
    x='study_load',
    y='anxiety_level',
    color='anxiety_level',
    color_continuous_scale='purples',
    labels={'anxiety_level': 'Avg Anxiety Level', 'study_load': 'Study Load'}
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------
# Bar Plot: Headache by Living Conditions
st.header("3. Average Headache by Living Conditions")
avg = df.groupby('living_conditions')['headache'].mean().reset_index()
fig3 = px.bar(
    avg, x='living_conditions', y='headache',
    title='Average Headache Levels by Living Conditions',
    labels={'living_conditions':'Living Conditions','headache':'Avg Headache Level'},
    color='headache', color_continuous_scale='oranges'
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------
# Scatter Plot: Self Esteem vs Depression
st.header("4. Self Esteem vs Depression (Colored by Peer Pressure)")
fig4 = px.scatter(
    df,
    x='self_esteem',
    y='depression',
    color='peer_pressure',
    title='Depression vs Self Esteem',
    labels={'self_esteem': 'Self Esteem', 'depression': 'Depression'},
    opacity=0.7,
    color_discrete_sequence=px.colors.sequential.Teal
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------
# Pie Charts: Depression Levels by Peer Pressure
st.header("5. Depression Levels by Peer Pressure (Pie Charts)")

# Categorize depression
df['depression_level'] = df['depression'].apply(lambda x: 'High' if x >= 7 else 'Low')

# Get unique levels
peer_levels = df['peer_pressure'].unique()
colors = {'High': '#FF6347', 'Low': '#ADD8E6'}

fig, axes = plt.subplots(1, len(peer_levels), figsize=(5 * len(peer_levels), 5))

for i, level in enumerate(sorted(peer_levels)):
    group = df[df['peer_pressure'] == level]['depression_level'].value_counts()
    axes[i].pie(
        group,
        labels=group.index,
        autopct='%1.1f%%',
        colors=[colors[label] for label in group.index],
        startangle=90,
        explode=[0.05 if label == 'High' else 0 for label in group.index]
    )
    axes[i].set_title(f'Peer Pressure: {level}')

st.pyplot(fig)
