"""
Generate professional graphs for AI benchmark results
Creates publication-ready charts for presentation slides
"""

import csv
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    """Load benchmark data from CSV"""
    data = {'depths': [], 'minimax_time': [], 'alphabeta_time': [], 
            'speedup': [], 'minimax_nodes': [], 'alphabeta_nodes': [], 'nodes_saved': []}
    
    with open('ai_benchmark_results.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['depths'].append(int(row['Depth']))
            data['minimax_time'].append(float(row['Minimax_Time_Sec']))
            data['alphabeta_time'].append(float(row['AlphaBeta_Time_Sec']))
            data['speedup'].append(float(row['Speedup']))
            data['minimax_nodes'].append(int(row['Minimax_Nodes']))
            data['alphabeta_nodes'].append(int(row['AlphaBeta_Nodes']))
            data['nodes_saved'].append(float(row['Nodes_Saved_Percent']))
    
    return data

def create_timing_comparison():
    """Graph 1: Side-by-side timing comparison - shows Alpha-Beta stays fast"""
    data = load_data()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(data['depths']))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, data['minimax_time'], width, label='Minimax', color='#ff7f7f', alpha=0.8)
    bars2 = ax.bar(x + width/2, data['alphabeta_time'], width, label='Alpha-Beta', color='#7fbf7f', alpha=0.8)
    
    ax.set_xlabel('Search Depth', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Move Computation Time: Minimax vs Alpha-Beta Pruning', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(data['depths'])
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}s', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}s', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('timing_comparison.png', dpi=300, bbox_inches='tight')
    print("📊 Created: timing_comparison.png")

def create_speedup_chart():
    """Graph 2: Speedup line chart - shows exponential improvement"""
    data = load_data()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(data['depths'], data['speedup'], marker='o', linewidth=3, markersize=8, 
            color='#2E86C1', markerfacecolor='#F39C12')
    
    ax.set_xlabel('Search Depth', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speedup Factor (x times faster)', fontsize=12, fontweight='bold')
    ax.set_title('Alpha-Beta Pruning Performance Advantage', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for i, (depth, speedup) in enumerate(zip(data['depths'], data['speedup'])):
        ax.annotate(f'{speedup}x faster', 
                   (depth, speedup), 
                   textcoords="offset points", 
                   xytext=(0,15), 
                   ha='center', 
                   fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    ax.set_ylim(0, max(data['speedup']) + 1)
    plt.tight_layout()
    plt.savefig('speedup_chart.png', dpi=300, bbox_inches='tight')
    print("📊 Created: speedup_chart.png")

def create_nodes_comparison():
    """Graph 3: Node evaluation comparison - shows pruning efficiency"""
    data = load_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Left: Node counts
    x = np.arange(len(data['depths']))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, data['minimax_nodes'], width, label='Minimax', color='#ff7f7f', alpha=0.8)
    bars2 = ax1.bar(x + width/2, data['alphabeta_nodes'], width, label='Alpha-Beta', color='#7fbf7f', alpha=0.8)
    
    ax1.set_xlabel('Search Depth', fontweight='bold')
    ax1.set_ylabel('Average Nodes Evaluated', fontweight='bold')
    ax1.set_title('Nodes Evaluated Comparison', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(data['depths'])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold', rotation=90)
    
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold', rotation=90)
    
    # Right: Pruning efficiency
    ax2.bar(data['depths'], data['nodes_saved'], color='#27AE60', alpha=0.8)
    ax2.set_xlabel('Search Depth', fontweight='bold')
    ax2.set_ylabel('Nodes Saved (%)', fontweight='bold')
    ax2.set_title('Alpha-Beta Pruning Efficiency', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add percentage labels
    for depth, saved in zip(data['depths'], data['nodes_saved']):
        ax2.text(depth, saved + 1, f'{saved:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('nodes_comparison.png', dpi=300, bbox_inches='tight')
    print("📊 Created: nodes_comparison.png")

def create_summary_dashboard():
    """Graph 4: Combined dashboard - perfect for single slide"""
    data = load_data()
    
    fig = plt.figure(figsize=(16, 10))
    
    # Top left: Timing
    ax1 = plt.subplot(2, 2, 1)
    x = np.arange(len(data['depths']))
    width = 0.35
    ax1.bar(x - width/2, data['minimax_time'], width, label='Minimax', color='#E74C3C', alpha=0.8)
    ax1.bar(x + width/2, data['alphabeta_time'], width, label='Alpha-Beta', color='#27AE60', alpha=0.8)
    ax1.set_title('Computation Time', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Time (seconds)', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(data['depths'])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Top right: Speedup
    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(data['depths'], data['speedup'], 'o-', linewidth=3, markersize=8, color='#3498DB')
    ax2.set_title('Performance Improvement', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Speedup (x times faster)', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    for depth, speedup in zip(data['depths'], data['speedup']):
        ax2.text(depth, speedup + 0.1, f'{speedup}x', ha='center', fontweight='bold')
    
    # Bottom left: Node counts (log scale)
    ax3 = plt.subplot(2, 2, 3)
    ax3.bar(x - width/2, data['minimax_nodes'], width, label='Minimax', color='#E74C3C', alpha=0.8)
    ax3.bar(x + width/2, data['alphabeta_nodes'], width, label='Alpha-Beta', color='#27AE60', alpha=0.8)
    ax3.set_title('Nodes Evaluated', fontweight='bold', fontsize=12)
    ax3.set_ylabel('Nodes (log scale)', fontweight='bold')
    ax3.set_yscale('log')
    ax3.set_xticks(x)
    ax3.set_xticklabels(data['depths'])
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Bottom right: Efficiency
    ax4 = plt.subplot(2, 2, 4)
    bars = ax4.bar(data['depths'], data['nodes_saved'], color='#F39C12', alpha=0.8)
    ax4.set_title('Pruning Efficiency', fontweight='bold', fontsize=12)
    ax4.set_ylabel('Nodes Saved (%)', fontweight='bold')
    ax4.set_xlabel('Search Depth', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    for bar, saved in zip(bars, data['nodes_saved']):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{saved:.1f}%', ha='center', fontweight='bold')
    
    plt.suptitle('Connect4 AI: Minimax vs Alpha-Beta Pruning Analysis', 
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('summary_dashboard.png', dpi=300, bbox_inches='tight')
    print("📊 Created: summary_dashboard.png")

def main():
    print("🎨 Generating Professional Graphs...")
    
    create_timing_comparison()     # Perfect for showing Alpha-Beta stays fast
    create_speedup_chart()        # Shows exponential improvement
    create_nodes_comparison()     # Demonstrates pruning efficiency  
    create_summary_dashboard()    # Everything in one slide
    
    print("\n🎉 All graphs created successfully!")
    print("\n📈 Recommended for presentation:")
    print("  • summary_dashboard.png - Single comprehensive slide")
    print("  • speedup_chart.png - Shows dramatic performance gains")
    print("  • timing_comparison.png - Clear side-by-side comparison")
    print("  • nodes_comparison.png - Proves algorithmic efficiency")

if __name__ == "__main__":
    main()