"""
AI Policy Trends Dashboard - Core Modules

This package contains the core functionality for data processing,
NLP analysis, and dashboard utilities.
"""

__version__ = '1.0.0'
__author__ = 'AI Policy Analytics Team'

from .data_processor import DataProcessor
from .nlp_analyzer import NLPAnalyzer, RegulationScorer
from .utils import SessionState, load_data

__all__ = [
    'DataProcessor',
    'NLPAnalyzer',
    'RegulationScorer',
    'SessionState',
    'load_data'
]
