import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Ed-TechLMS KPIs Dashboard",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        right: 10px;
        font-size: 12px;
        color: #888888;
    }
    .header-author {
        font-size: 12px;
        color: #888888;
        margin-bottom: 20px;
    }
    /* Custom styling for feature buttons */
    div[data-testid="stHorizontalBlock"] {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 5px;
        margin: 3px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    div[data-testid="stHorizontalBlock"]:hover {
        background-color: #e0e2e6;
    }
    .feature-button {
        text-align: center;
        padding: 8px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .feature-button.selected {
        background-color: #1f77b4;
        color: white;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 20px 0;
    }
    [data-testid="stMetric"] {
        background-color: transparent !important;
        padding: 0 !important;
    }
    [data-testid="stMetricValue"] {
        text-align: center;
    }
    div[data-testid="column"] {
        background-color: transparent !important;
        padding: 0 !important;
    }
    .metric-row {
        display: flex;
        justify-content: space-around;
        margin: 30px 0;
        width: 100%;
        padding: 0 10%;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 8px;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('lms_user_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

# Load the data
df = load_data()

# Main page
st.title("LMS KPIs Dashboard")
st.markdown('<p class="header-author">By Siddharth Negi</p>', unsafe_allow_html=True)

# Sidebar with custom buttons
st.sidebar.markdown("## Product Features")

# Define features
features = ['Notification', 'LiveClass', 'Classroom', 'Curriculum', 
           'ShortCourses', 'Masterclass', 'BookMentor', 'DoubtSession',
           'Assignments', 'Resources', 'Recordings', 'CodingWindow',
           'QuestionBank', 'HelpTicket', 'ReferFriend']

# Create session state to store selected feature if it doesn't exist
if 'selected_feature' not in st.session_state:
    st.session_state.selected_feature = features[0]

# Create custom buttons for each feature
for feature in features:
    # Create a container for each button
    button_container = st.sidebar.container()
    
    # Check if this feature is selected
    is_selected = st.session_state.selected_feature == feature
    
    # Create the button with conditional styling
    if button_container.button(
        feature,
        key=f"btn_{feature}",
        use_container_width=True,
        type="primary" if is_selected else "secondary"
    ):
        st.session_state.selected_feature = feature
        st.rerun()

# Use the selected feature from session state
selected_feature = st.session_state.selected_feature

# Calculate metrics for selected feature
feature_lower = selected_feature.lower()
avg_duration = df[f'{feature_lower}_duration'].mean()
median_duration = df[f'{feature_lower}_duration'].median()
conversion_rate = df[f'{feature_lower}_conversion'].mean() * 100
dropoff_rate = df[f'{feature_lower}_dropoff'].mean() * 100
avg_nps = df[f'{feature_lower}_nps'].mean()

# First row of metrics
st.markdown(
    f"""
    <div class="metric-row">
        <div>
            <div class="metric-value">{avg_duration:.2f}</div>
            <div class="metric-label">Average Duration (mins)</div>
        </div>
        <div>
            <div class="metric-value">{median_duration:.2f}</div>
            <div class="metric-label">Median Duration (mins)</div>
        </div>
        <div>
            <div class="metric-value">{conversion_rate:.2f}%</div>
            <div class="metric-label">Conversion Rate</div>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

# Second row of metrics
st.markdown(
    f"""
    <div class="metric-row">
        <div>
            <div class="metric-value">{dropoff_rate:.2f}%</div>
            <div class="metric-label">Drop-off Rate</div>
        </div>
        <div>
            <div class="metric-value">{avg_nps:.2f}</div>
            <div class="metric-label">Average NPS</div>
        </div>
        <div></div>
    </div>
    """, 
    unsafe_allow_html=True
)

# Create multi-line chart
st.subheader("Metrics Over Time")

# Prepare data for the multi-line chart
daily_metrics = df.groupby('date').agg({
    f'{feature_lower}_duration': 'mean',
    f'{feature_lower}_conversion': 'mean',
    f'{feature_lower}_dropoff': 'mean',
    f'{feature_lower}_nps': 'mean'
}).reset_index()

# Create figure with secondary y-axis
fig = go.Figure()

# Add traces with customized hover templates
fig.add_trace(
    go.Scatter(
        x=daily_metrics['date'], 
        y=daily_metrics[f'{feature_lower}_duration'],
        name='Duration (mins)', 
        line=dict(color='#1f77b4'),
        hovertemplate='Duration: %{y:.1f} mins<extra></extra>'
    )
)

fig.add_trace(
    go.Scatter(
        x=daily_metrics['date'], 
        y=daily_metrics[f'{feature_lower}_conversion'] * 100,
        name='Conversion Rate (%)', 
        line=dict(color='#2ca02c'),
        hovertemplate='Conversion Rate: %{y:.1f}%<extra></extra>'
    )
)

fig.add_trace(
    go.Scatter(
        x=daily_metrics['date'], 
        y=daily_metrics[f'{feature_lower}_dropoff'] * 100,
        name='Drop-off Rate (%)', 
        line=dict(color='#d62728'),
        hovertemplate='Drop-off Rate: %{y:.1f}%<extra></extra>'
    )
)

fig.add_trace(
    go.Scatter(
        x=daily_metrics['date'], 
        y=daily_metrics[f'{feature_lower}_nps'],
        name='NPS', 
        line=dict(color='#9467bd'),
        hovertemplate='NPS: %{y:.1f}<extra></extra>'
    )
)

# Update layout
fig.update_layout(
    title=f'Metrics Trend for {selected_feature}',
    xaxis_title='Date',
    yaxis_title='Value',
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown('<p class="footer">By Siddharth Negi</p>', unsafe_allow_html=True) 