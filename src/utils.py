import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import logging

logger = logging.getLogger(__name__)


@st.cache_resource
def load_data():
    """Load and cache processed data"""
    data_dir = Path(__file__).parent.parent / 'data'
    
    data = {}
    try:
        if (data_dir / 'processed_documents.csv').exists():
            data['documents'] = pd.read_csv(data_dir / 'processed_documents.csv')
        if (data_dir / 'processed_opinions.csv').exists():
            data['opinions'] = pd.read_csv(data_dir / 'processed_opinions.csv')
        if (data_dir / 'merged_policy_data.csv').exists():
            data['merged'] = pd.read_csv(data_dir / 'merged_policy_data.csv')
    except Exception as e:
        logger.error(f"Error loading data: {e}")
    
    return data


def format_large_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{int(num)}"


def get_color_by_sentiment(sentiment):
    """Get color based on sentiment"""
    sentiment_colors = {
        'Positive': '#2ecc71',
        'Negative': '#e74c3c',
        'Neutral': '#95a5a6',
        'Enabling': '#3498db',
        'Restrictive': '#e67e22',
    }
    return sentiment_colors.get(sentiment, '#95a5a6')


def truncate_text(text, max_length=100):
    """Truncate text to max length"""
    if len(str(text)) > max_length:
        return str(text)[:max_length] + "..."
    return text


def create_metric_card(title, value, delta=None, delta_color="off"):
    """Create a custom metric card"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(title, value, delta=delta, delta_color=delta_color)


def filter_dataframe(df, filters):
    """Apply filters to dataframe"""
    result = df.copy()
    
    for column, values in filters.items():
        if column in result.columns and values:
            result = result[result[column].isin(values)]
    
    return result


def safe_get_column(df, column_name, default=None):
    """Safely get column from dataframe"""
    if column_name in df.columns:
        return df[column_name]
    return default if default is not None else pd.Series([None] * len(df))


def get_date_range(df, date_column):
    """Get date range from dataframe"""
    if date_column not in df.columns:
        return None, None
    
    dates = pd.to_datetime(df[date_column], errors='coerce')
    dates = dates.dropna()
    
    if len(dates) == 0:
        return None, None
    
    return dates.min(), dates.max()


def calculate_growth_rate(values):
    """Calculate growth rate from values"""
    if len(values) < 2 or values[0] == 0:
        return 0
    return ((values[-1] - values[0]) / values[0]) * 100


def get_top_items(series, n=10):
    """Get top n items from a series"""
    return series.value_counts().head(n)


def export_to_csv(df, filename="export.csv"):
    """Export dataframe to CSV"""
    csv = df.to_csv(index=False)
    return csv


def create_pie_chart_data(df, column):
    """Prepare data for pie chart"""
    data = df[column].value_counts()
    return data


class SessionState:
    """Manage session state"""
    
    @staticmethod
    def init_session_state():
        """Initialize session state variables"""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Home'
        if 'filters' not in st.session_state:
            st.session_state.filters = {}
    
    @staticmethod
    def set_filter(filter_key, filter_value):
        """Set a filter"""
        if 'filters' not in st.session_state:
            st.session_state.filters = {}
        st.session_state.filters[filter_key] = filter_value
    
    @staticmethod
    def get_filter(filter_key, default=None):
        """Get a filter value"""
        if 'filters' not in st.session_state:
            return default
        return st.session_state.filters.get(filter_key, default)
    
    @staticmethod
    def clear_filters():
        """Clear all filters"""
        st.session_state.filters = {}
