#!/usr/bin/env python3
"""
Data preprocessing script - Run this to prepare all data before starting the dashboard
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_processor import DataProcessor
from nlp_analyzer import NLPAnalyzer, RegulationScorer
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main preprocessing pipeline"""
    
    project_dir = Path(__file__).parent
    data_dir = project_dir / 'data'
    parent_data_dir = project_dir.parent
    
    # Create data directory
    data_dir.mkdir(exist_ok=True)
    
    logger.info("=" * 80)
    logger.info("Starting AI Policy Dashboard Data Preprocessing")
    logger.info("=" * 80)
    
    # Initialize data processor
    processor = DataProcessor(str(parent_data_dir))
    
    # Load AGORA data
    logger.info("\n[1/6] Loading AGORA dataset...")
    if processor.load_agora_data():
        logger.info("✓ AGORA data loaded successfully")
    else:
        logger.error("✗ Failed to load AGORA data")
        return False
    
    # Load opinion data
    logger.info("\n[2/6] Loading generative AI opinion data...")
    if processor.load_opinion_data():
        logger.info("✓ Opinion data loaded successfully")
    else:
        logger.warning("⚠ Opinion data not available (optional)")
    
    # Clean documents
    logger.info("\n[3/6] Cleaning policy documents...")
    if processor.clean_documents():
        logger.info("✓ Documents cleaned successfully")
    else:
        logger.error("✗ Failed to clean documents")
        return False
    
    # Clean opinions
    if processor.opinions_df is not None:
        logger.info("\n[4/6] Cleaning opinion data...")
        if processor.clean_opinions():
            logger.info("✓ Opinions cleaned successfully")
        else:
            logger.warning("⚠ Failed to clean opinions")
    else:
        logger.info("\n[4/6] Skipping opinion cleaning (no data)")
    
    # Merge data
    logger.info("\n[5/6] Merging policy data with metadata...")
    if processor.merge_policy_data():
        logger.info("✓ Data merged successfully")
    else:
        logger.error("✗ Failed to merge data")
        return False
    
    # Export processed data
    logger.info("\n[6/6] Exporting processed data...")
    processor.export_processed_data(str(data_dir))
    logger.info("✓ Data exported successfully")
    
    # Run NLP analysis
    logger.info("\n" + "=" * 80)
    logger.info("Running NLP Analysis...")
    logger.info("=" * 80)
    
    if processor.documents_df is not None and len(processor.documents_df) > 0:
        df = processor.documents_df
        
        # Sentiment analysis on opinions
        if processor.opinions_df is not None and len(processor.opinions_df) > 0:
            logger.info("\n[NLP-1] Performing sentiment analysis...")
            analyzer = NLPAnalyzer()
            sentiments = analyzer.sentiment_analysis(processor.opinions_df['full_text'].head(500))
            
            sentiments_df = pd.concat([processor.opinions_df.head(500).reset_index(drop=True), sentiments], axis=1)
            sentiments_df.to_csv(data_dir / 'sentiment_analysis.csv', index=False)
            logger.info("✓ Sentiment analysis completed and saved")
        
        # Topic modeling
        logger.info("\n[NLP-2] Running topic modeling...")
        analyzer = NLPAnalyzer()
        texts = df['full_text'].fillna('').values[:1000]  # Use first 1000 for speed
        lda_matrix, topics_dict = analyzer.topic_modeling(texts, n_topics=10)
        
        # Save topics to CSV
        topics_list = []
        for topic_id, (topic_name, words) in enumerate(topics_dict.items()):
            topics_list.append({
                'Topic': topic_name,
                'Top_Words': ', '.join(words)
            })
        
        topics_df = pd.DataFrame(topics_list)
        topics_df.to_csv(data_dir / 'topics.csv', index=False)
        logger.info("✓ Topic modeling completed and saved")
        
        # Extract keywords
        logger.info("\n[NLP-3] Extracting keywords...")
        keywords = analyzer.extract_keywords(texts, n_keywords=20)
        keywords_df = pd.DataFrame(keywords, columns=['Keyword', 'TF-IDF_Score'])
        keywords_df.to_csv(data_dir / 'keywords.csv', index=False)
        logger.info("✓ Keywords extracted and saved")
        
        # Calculate maturity scores
        logger.info("\n[NLP-4] Calculating policy maturity scores...")
        scorer = RegulationScorer()
        maturity_scores = scorer.calculate_maturity_score(df)
        maturity_scores.to_csv(data_dir / 'maturity_scores.csv', index=False)
        logger.info("✓ Maturity scores calculated and saved")
        
        # Regulatory intensity
        logger.info("\n[NLP-5] Analyzing regulatory intensity...")
        intensity = scorer.regulatory_intensity(df)
        intensity_df = pd.DataFrame(list(intensity.items()), columns=['Domain', 'Document_Count'])
        intensity_df.to_csv(data_dir / 'regulatory_intensity.csv', index=False)
        logger.info("✓ Regulatory intensity analysis completed and saved")
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("PREPROCESSING COMPLETED SUCCESSFULLY!")
    logger.info("=" * 80)
    
    if processor.documents_df is not None:
        print(f"\n📊 Summary Statistics:")
        print(f"  • Total Policy Documents: {len(processor.documents_df)}")
        print(f"  • Unique Authorities: {processor.documents_df['Authority'].nunique()}")
        print(f"  • Average Document Length: {processor.documents_df['full_text'].str.len().mean():.0f} characters")
        print(f"  • Total Opinions: {len(processor.opinions_df) if processor.opinions_df is not None else 0}")
    
    print(f"\n✓ Processed data saved to: {data_dir}")
    print(f"\n🚀 Next step: Run the dashboard with:")
    print(f"   streamlit run app.py")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
