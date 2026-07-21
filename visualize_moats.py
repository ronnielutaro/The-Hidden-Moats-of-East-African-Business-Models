import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for a premium look
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

def main():
    # 1. Load the master dataset
    csv_path = 'dataset/master_analytic_dataset.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    df = pd.read_csv(csv_path)
    print("Dataset loaded successfully:")
    print(df[['company_name', 'primary_model', 'proximity_to_transaction', 'supply_chain_visibility']])
    
    # Convert ordinal scales to numeric for plotting
    df['proximity_to_transaction'] = df['proximity_to_transaction'].astype(int)
    df['supply_chain_visibility'] = df['supply_chain_visibility'].astype(int)
    df['estimated_scale_tier'] = df['estimated_scale_tier'].astype(int)
    
    # Seed for reproducible jittering
    np.random.seed(42)
    df['prox_jittered'] = df['proximity_to_transaction'] + np.random.uniform(-0.15, 0.15, size=len(df))
    df['vis_jittered'] = df['supply_chain_visibility'] + np.random.uniform(-0.15, 0.15, size=len(df))
    
    # 2. Create the figure
    fig, ax = plt.subplots(figsize=(11, 9), dpi=300)
    
    # Define color palette based on route to market operations
    # Asset-Heavy vs Asset-Light
    palette = {'Asset-Heavy': '#E76F51', 'Asset-Light': '#2A9D8F'}
    
    # Define sizes based on estimated scale tier (with some scaling)
    sizes = df['estimated_scale_tier'] * 250
    
    # 3. Scatter plot
    scatter = sns.scatterplot(
        data=df,
        x='prox_jittered',
        y='vis_jittered',
        hue='route_to_market_ops',
        palette=palette,
        size=sizes,
        sizes=(200, 800),
        legend='brief',
        alpha=0.85,
        edgecolor='black',
        linewidth=1.5,
        ax=ax
    )
    
    # 4. Annotate company names
    for i in range(df.shape[0]):
        row = df.iloc[i]
        # Default offset
        x_offset = 0.10
        y_offset = 0.02
        
        # Adjust offsets dynamically to prevent label overlap clashes at high density points (e.g. 5, 5)
        if row['company_name'] == 'Lipa Later':
            y_offset = -0.16
            x_offset = 0.05
        elif row['company_name'] == 'MTN MoMo':
            y_offset = 0.10
            x_offset = -0.6
        elif row['company_name'] == 'Airtel Money':
            y_offset = -0.15
            x_offset = -0.6
        elif row['company_name'] == 'SafeBoda':
            y_offset = 0.12
            x_offset = 0.05
        elif row['company_name'] == 'Kopo Kopo':
            y_offset = -0.12
            x_offset = 0.08
        elif row['company_name'] == 'BasiGo':
            x_offset = -0.5
            y_offset = 0.12
        elif row['company_name'] == 'Rocket Health':
            y_offset = -0.15
            x_offset = 0.08
        elif row['company_name'] == 'Twiga Foods':
            y_offset = 0.10
            x_offset = 0.05
        elif row['company_name'] == 'Wasoko':
            y_offset = -0.12
            x_offset = -0.5
        elif row['company_name'] == 'Sendy':
            y_offset = 0.10
            x_offset = -0.5
            
        ax.text(
            row['prox_jittered'] + x_offset,
            row['vis_jittered'] + y_offset,
            row['company_name'],
            horizontalalignment='left',
            size='small',
            color='#264653',
            weight='bold'
        )
        
    # 5. Set axis labels and limits
    ax.set_xlabel('Proximity to Cash Transaction (1 = Far, 5 = Direct/Mobile Money Rail)', labelpad=15)
    ax.set_ylabel('Supply Chain Visibility (1 = Deep Black Hole, 5 = Real-Time Stream)', labelpad=15)
    ax.set_title('East African Business Models: The Transaction vs. Visibility Matrix', pad=20, weight='bold')
    
    # Set limits with some padding
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    
    # Set discrete ticks
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([1, 2, 3, 4, 5])
    
    # Annotate zones to add strategic depth (The "Hidden Moats" zones)
    # Zone 1: High Transaction, High Visibility (The Digital Giants)
    ax.axvspan(4, 5.5, ymin=0.6, ymax=1.0, color='#2A9D8F', alpha=0.04)
    ax.text(4.75, 4.8, 'Digital\nControl Room', color='#1D6F66', fontsize=10, style='italic', weight='semibold', ha='center')
    
    # Zone 2: Low Transaction, Low Visibility (Traditional Heavy)
    ax.axvspan(0.5, 3.5, ymin=0.0, ymax=0.5, color='#E76F51', alpha=0.04)
    ax.text(2.0, 1.3, 'Traditional Logistics\n(Asset-Heavy Moat)', color='#B14A33', fontsize=10, style='italic', weight='semibold', ha='center')
    
    # Highlight the "Supply Chain Visibility Black Hole"
    ax.annotate(
        'The Visibility Black Hole\n(Traditional FMCG Trap)',
        xy=(3, 1),
        xytext=(1.5, 2.3),
        arrowprops=dict(facecolor='#264653', shrink=0.08, width=1.5, headwidth=6),
        color='#264653',
        weight='semibold',
        bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.2)
    )

    # 6. Customize legend
    handles, labels = ax.get_legend_handles_labels()
    new_handles = []
    new_labels = []
    
    for h, l in zip(handles, labels):
        if l in ['route_to_market_ops', 'estimated_scale_tier']:
            continue
        if l in ['Asset-Heavy', 'Asset-Light']:
            new_handles.append(h)
            new_labels.append(l + ' Ops')
            
    ax.legend(new_handles, new_labels, loc='upper left', frameon=True, facecolor='white', edgecolor='#E5E5E5')
    
    plt.tight_layout()
    
    # Save the output image
    output_png = 'cohort_1_moats_matrix.png'
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    print(f"Beautiful bubble chart generated and saved to {output_png}!")

if __name__ == '__main__':
    main()
