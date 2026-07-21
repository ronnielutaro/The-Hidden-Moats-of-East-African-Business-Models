"""Data Transformer Pipeline for East African Business Models.

Loads relational tables from CSVs, conducts feature engineering,
and generates the unified master analytic dataset.
"""
import pandas as pd
import numpy as np
import os

def run_transform():
    # Resolve directory paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    companies_file = os.path.join(base_dir, 'companies.csv')
    operations_file = os.path.join(base_dir, 'operations.csv')
    lifespans_file = os.path.join(base_dir, 'lifespans.csv')
    funding_file = os.path.join(base_dir, 'funding_rounds.csv')
    events_file = os.path.join(base_dir, 'pivots_and_events.csv')
    
    # Load raw relational datasets
    print("Loading raw relational datasets...")
    df_comp = pd.read_csv(companies_file)
    df_ops = pd.read_csv(operations_file)
    df_life = pd.read_csv(lifespans_file)
    df_fund = pd.read_csv(funding_file)
    df_events = pd.read_csv(events_file)
    
    # Feature Engineering Layer
    print("Conducting feature engineering...")
    
    # 1. Aggregate Funding Statistics
    df_fund_agg = df_fund.groupby('company_id').agg(
        total_funding_usd=('amount_usd', 'sum'),
        funding_rounds_count=('round_type', 'count')
    ).reset_index()
    
    # 2. Extract Event-Based Counts
    pivot_counts = df_events[df_events['event_type'] == 'Pivot'].groupby('company_id').size().reset_index(name='pivot_count')
    expansion_counts = df_events[df_events['event_type'] == 'Expansion'].groupby('company_id').size().reset_index(name='expansion_count')
    restructure_counts = df_events[df_events['event_type'] == 'Restructure'].groupby('company_id').size().reset_index(name='restructure_count')
    
    # Merge Event-Based Counts
    df_events_agg = pd.DataFrame({'company_id': df_comp['company_id']})
    df_events_agg = df_events_agg.merge(pivot_counts, on='company_id', how='left').fillna({'pivot_count': 0})
    df_events_agg = df_events_agg.merge(expansion_counts, on='company_id', how='left').fillna({'expansion_count': 0})
    df_events_agg = df_events_agg.merge(restructure_counts, on='company_id', how='left').fillna({'restructure_count': 0})
    
    # Join Master Dataset
    print("Consolidating tables on company_id...")
    master = df_comp.merge(df_ops, on='company_id', how='left')
    master = master.merge(df_life, on='company_id', how='left')
    master = master.merge(df_fund_agg, on='company_id', how='left').fillna({'total_funding_usd': 0, 'funding_rounds_count': 0})
    master = master.merge(df_events_agg, on='company_id', how='left')
    
    # Derived Feature Engineering
    # Funding efficiency index (funding per year of operational lifespan)
    # Adding small epsilon to avoid divide-by-zero if lifespan is 0
    master['funding_per_year_usd'] = master['total_funding_usd'] / (master['lifespan_years'] + 1e-5)
    
    # Has pivoted boolean indicator
    master['has_pivoted'] = master['pivot_count'] > 0
    
    # Save target file
    out_file = os.path.join(base_dir, 'master_analytic_dataset.csv')
    master.to_csv(out_file, index=False)
    print(f"Success! Relational database transformed and written to: {out_file}")

if __name__ == '__main__':
    run_transform()
