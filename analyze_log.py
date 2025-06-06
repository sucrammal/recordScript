#!/usr/bin/env python3
"""
Analyze cooking action logs generated by the interactive recording script.
Example analysis of the timestamped action data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def analyze_log(log_file="cooking_actions_log.csv"):
    """Analyze the action log CSV file."""
    
    if not os.path.exists(log_file):
        print(f"❌ Log file not found: {log_file}")
        print("Run the interactive recording first to generate data.")
        return
    
    print(f"📊 Analyzing action log: {log_file}")
    print("=" * 50)
    
    # Load the CSV data
    df = pd.read_csv(log_file)
    
    # Basic statistics
    print(f"📋 Total logged entries: {len(df)}")
    print(f"🎬 Video file: {df['video_filename'].iloc[0] if len(df) > 0 else 'N/A'}")
    
    # Filter actual actions (exclude session and phase transitions)
    actions = df[~df['action_category'].isin(['session', 'phase_transition'])]
    
    if len(actions) == 0:
        print("⚠️  No cooking actions found in log")
        return
    
    print(f"\n🥄 Cooking Actions Analysis:")
    print(f"   Total actions: {len(actions)}")
    print(f"   Action categories: {actions['action_category'].nunique()}")
    print(f"   Average duration: {actions['duration_seconds'].mean():.2f}s")
    print(f"   Total action time: {actions['duration_seconds'].sum():.2f}s")
    
    # Category breakdown
    print(f"\n📊 Action Categories:")
    for category in actions['action_category'].unique():
        count = len(actions[actions['action_category'] == category])
        avg_duration = actions[actions['action_category'] == category]['duration_seconds'].mean()
        total_duration = actions[actions['action_category'] == category]['duration_seconds'].sum()
        print(f"   {category}: {count} actions, avg {avg_duration:.1f}s, total {total_duration:.1f}s")
    
    # Action description breakdown
    print(f"\n🎯 Precise Action Labels:")
    for action_desc in sorted(actions['action_description'].unique()):
        count = len(actions[actions['action_description'] == action_desc])
        avg_duration = actions[actions['action_description'] == action_desc]['duration_seconds'].mean()
        category = actions[actions['action_description'] == action_desc]['action_category'].iloc[0]
        print(f"   {action_desc}: {count} times, avg {avg_duration:.1f}s ({category})")
    
    # Repetition analysis
    print(f"\n🔄 Repetition Analysis:")
    for category in actions['action_category'].unique():
        cat_actions = actions[actions['action_category'] == category]
        max_reps = cat_actions['repetition_number'].max()
        print(f"   {category}: {max_reps} repetitions")
    
    # Timeline analysis
    if len(actions) > 1:
        print(f"\n⏱️  Timeline:")
        print(f"   First action: {actions['start_time_seconds'].min():.1f}s")
        print(f"   Last action: {actions['end_time_seconds'].max():.1f}s")
        print(f"   Total span: {actions['end_time_seconds'].max() - actions['start_time_seconds'].min():.1f}s")
    
    # Generate summary for ML use
    print(f"\n🤖 Machine Learning Dataset Summary:")
    print(f"   Video segments: {len(actions)} labeled actions")
    print(f"   Action categories: {list(actions['action_category'].unique())}")
    print(f"   Precise actions: {list(sorted(actions['action_description'].unique()))}")
    print(f"   Balanced dataset: {'Yes' if actions['action_category'].value_counts().std() < 2 else 'No'}")
    
    # Show sample data
    print(f"\n📋 Sample Action Entries:")
    sample_actions = actions[['action_category', 'action_description', 'repetition_number', 'start_time_seconds', 'end_time_seconds', 'duration_seconds']].head()
    print(sample_actions.to_string(index=False))
    
    return df, actions

def create_timeline_plot(actions, save_path="action_timeline.png"):
    """Create a timeline visualization of actions."""
    if len(actions) == 0:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Color map for different categories
    categories = actions['action_category'].unique()
    colors = plt.cm.Set3(range(len(categories)))
    color_map = dict(zip(categories, colors))
    
    # Plot each action as a horizontal bar
    for i, (_, action) in enumerate(actions.iterrows()):
        plt.barh(i, action['duration_seconds'], 
                left=action['start_time_seconds'],
                color=color_map[action['action_category']],
                alpha=0.7,
                label=action['action_category'] if action['action_category'] not in plt.gca().get_legend_handles_labels()[1] else "")
    
    plt.xlabel('Time (seconds)')
    plt.ylabel('Action Index')
    plt.title('Cooking Actions Timeline')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    try:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"📈 Timeline plot saved to: {save_path}")
    except Exception as e:
        print(f"⚠️  Could not save plot: {e}")
    
    # Show plot if running interactively
    try:
        plt.show()
    except:
        pass

def export_for_ml(actions, output_file="ml_dataset.csv"):
    """Export cleaned data for machine learning."""
    if len(actions) == 0:
        return
    
    # Create ML-ready dataset
    ml_data = actions[['action_category', 'action_description', 'start_time_seconds', 'end_time_seconds', 'duration_seconds', 'video_filename']].copy()
    
    # Add both category and precise action labels
    ml_data['category_label'] = ml_data['action_category']  # Broad category (pan_manipulation, food_cooking, etc.)
    ml_data['action_label'] = ml_data['action_description']  # Precise action (add-pan, stir, remove-food, etc.)
    
    # Add frame numbers for video processing (assuming FPS from video filename or default to 10)
    ml_data['video_start_frame'] = (ml_data['start_time_seconds'] * 10).round().astype(int)  # Assuming 10 FPS
    ml_data['video_end_frame'] = (ml_data['end_time_seconds'] * 10).round().astype(int)
    
    # Reorder columns for clarity
    ml_data = ml_data[['video_filename', 'category_label', 'action_label', 'start_time_seconds', 'end_time_seconds', 
                       'duration_seconds', 'video_start_frame', 'video_end_frame']]
    
    ml_data.to_csv(output_file, index=False)
    print(f"🤖 ML dataset exported to: {output_file}")
    print(f"   Ready for training with {len(ml_data)} labeled segments")
    print(f"   Categories: {sorted(ml_data['category_label'].unique())}")
    print(f"   Actions: {sorted(ml_data['action_label'].unique())}")

def main():
    """Main analysis function."""
    log_file = "cooking_actions_log.csv"
    
    # Allow custom log file as argument
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    
    print("🔍 Cooking Action Log Analyzer")
    print("=" * 40)
    
    # Run analysis
    result = analyze_log(log_file)
    if result is None:
        return
    
    df, actions = result
    
    # Create visualizations (requires matplotlib)
    try:
        create_timeline_plot(actions)
    except ImportError:
        print("📈 Install matplotlib for timeline visualization: pip install matplotlib")
    except Exception as e:
        print(f"⚠️  Could not create timeline plot: {e}")
    
    # Export ML dataset
    export_for_ml(actions)
    
    print(f"\n✅ Analysis complete!")
    print(f"Use this data for:")
    print(f"   • Training action recognition models")
    print(f"   • Video segmentation for datasets")
    print(f"   • Temporal behavior analysis")
    print(f"   • Quality control of recorded sessions")

if __name__ == "__main__":
    main() 