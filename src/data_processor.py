import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and prepare AI policy data from multiple sources"""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.documents_df = None
        self.authorities_df = None
        self.collections_df = None
        self.segments_df = None
        self.opinions_df = None
        self.merged_df = None
    
    def load_agora_data(self):
        """Load data from the Agora dataset"""
        logger.info("Loading AGORA dataset...")
        
        try:
            agora_path = self.data_dir / 'agora'
            
            self.documents_df = pd.read_csv(agora_path / 'documents.csv')
            self.authorities_df = pd.read_csv(agora_path / 'authorities.csv')
            self.collections_df = pd.read_csv(agora_path / 'collections.csv')
            self.segments_df = pd.read_csv(agora_path / 'segments.csv')
            
            logger.info(f"Loaded {len(self.documents_df)} documents")
            logger.info(f"Loaded {len(self.authorities_df)} authorities")
            logger.info(f"Loaded {len(self.segments_df)} segments")
            
            return True
        except Exception as e:
            logger.error(f"Error loading AGORA data: {e}")
            return False
    
    def load_opinion_data(self):
        """Load generative AI opinion data"""
        logger.info("Loading opinion dataset...")
        
        try:
            opinion_path = self.data_dir / 'generativeaiopinion.csv'
            self.opinions_df = pd.read_csv(opinion_path)
            logger.info(f"Loaded {len(self.opinions_df)} opinions")
            return True
        except Exception as e:
            logger.error(f"Error loading opinion data: {e}")
            return False
    
    def clean_documents(self):
        """Clean and preprocess documents"""
        logger.info("Cleaning documents...")
        
        if self.documents_df is None:
            return False
        
        df = self.documents_df.copy()
        
        # Handle missing values
        text_columns = ['Short summary', 'Long summary']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('')
        
        # Convert dates
        date_columns = ['Proposed date', 'Most recent activity date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Create full text column
        df['full_text'] = df.get('Long summary', '') + ' ' + df.get('Short summary', '')
        df['full_text'] = df['full_text'].str.strip()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['AGORA ID'], keep='first')
        
        self.documents_df = df
        logger.info(f"Cleaned to {len(df)} unique documents")
        return True
    
    def clean_opinions(self):
        """Clean opinion data"""
        logger.info("Cleaning opinions...")
        
        if self.opinions_df is None:
            return False
        
        df = self.opinions_df.copy()
        df['full_text'] = df['full_text'].fillna('').str.strip()
        df = df[df['full_text'].str.len() > 10]  # Remove very short texts
        df = df.drop_duplicates(subset=['full_text'], keep='first')
        
        self.opinions_df = df
        logger.info(f"Cleaned to {len(df)} unique opinions")
        return True
    
    def merge_policy_data(self):
        """Merge documents with authorities and collections"""
        logger.info("Merging policy data...")
        
        if self.documents_df is None or self.authorities_df is None:
            return False
        
        df = self.documents_df.copy()
        
        # Merge with authorities
        auth_key = None
        if 'Authority name' in self.authorities_df.columns:
            auth_key = 'Authority name'
        elif 'Name' in self.authorities_df.columns:
            auth_key = 'Name'

        if auth_key is not None:
            auth_cols = [auth_key] + [col for col in ['Jurisdiction', 'Parent authority'] if col in self.authorities_df.columns]
            auth_data = self.authorities_df[auth_cols].drop_duplicates()
            df = df.merge(auth_data, left_on='Authority', right_on=auth_key, how='left')
            if auth_key != 'Authority name':
                df = df.rename(columns={auth_key: 'Authority name'})
        
        # Add derived features
        df['document_length'] = df['full_text'].str.len()
        df['word_count'] = df['full_text'].str.split().str.len()
        df['is_policy_active'] = df.get('Primarily applies to the government', False) | df.get('Primarily applies to the private sector', False)
        
        self.merged_df = df
        logger.info("Data merged successfully")
        return True
    
    def get_summary_stats(self):
        """Get summary statistics"""
        if self.documents_df is None:
            return {}
        
        return {
            'total_documents': len(self.documents_df),
            'total_authorities': self.documents_df['Authority'].nunique() if 'Authority' in self.documents_df.columns else 0,
            'avg_document_length': self.documents_df['full_text'].str.len().mean() if 'full_text' in self.documents_df.columns else 0,
            'total_opinions': len(self.opinions_df) if self.opinions_df is not None else 0,
        }
    
    def export_processed_data(self, output_dir: str):
        """Export processed data"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if self.documents_df is not None:
            self.documents_df.to_csv(output_path / 'processed_documents.csv', index=False)
            logger.info(f"Exported documents to {output_path / 'processed_documents.csv'}")
        
        if self.merged_df is not None:
            self.merged_df.to_csv(output_path / 'merged_policy_data.csv', index=False)
            logger.info(f"Exported merged data to {output_path / 'merged_policy_data.csv'}")
        
        if self.opinions_df is not None:
            self.opinions_df.to_csv(output_path / 'processed_opinions.csv', index=False)
            logger.info(f"Exported opinions to {output_path / 'processed_opinions.csv'}")
