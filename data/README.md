# 📊 Data Directory

This directory contains all data files, datasets, and evaluation results in an organized structure.

## 📁 Directory Structure

```
data/
├── datasets/           # Ground truth and training datasets
│   ├── ml_dataset.csv         # Main ground truth dataset
│   └── cooking_actions_log.csv # Recording session logs
├── sample_videos/      # Sample/test videos for evaluation
│   └── README.md              # Video usage instructions
└── results/            # Evaluation outputs and analysis results
    ├── classification_result.txt        # Example log file
    ├── classification_result_timeline.log  # Example timeline
    ├── action_timeline.png             # Visualization
    └── cooking_actions_recording.mp4   # Example recording
```

## 📋 Dataset Descriptions

### `datasets/ml_dataset.csv`

**Ground truth dataset for evaluation**

Contains labeled action segments for performance comparison:

-   `action_label`: Specific action (add-food, remove-lid, etc.)
-   `start_time_seconds`: Action start time
-   `end_time_seconds`: Action end time
-   `duration_seconds`: Action duration
-   `video_filename`: Source video file

**Usage:**

```bash
cd evaluation/
python3 extract_and_align_classifier.py logs.txt
# Automatically loads ../data/datasets/ml_dataset.csv for comparison
```

### `datasets/cooking_actions_log.csv`

**Recording session metadata**

Generated by interactive recording sessions:

-   Timestamped action labels
-   Action categories and descriptions
-   Video filenames and metadata
-   Session information

## 🎥 Sample Videos

Place your evaluation videos in `sample_videos/` directory:

```bash
# Copy your videos
cp /path/to/your/videos/*.mp4 data/sample_videos/

# Run evaluation
cd evaluation/
python3 automate_evaluation.py --video-dir ../data/sample_videos
```

**Supported formats:** `.mp4`, `.avi`, `.mov`, `.mkv`

## 📊 Results Directory

Evaluation outputs are automatically saved here:

### **Per-Video Results**

-   `videoname_timestamp.log` - Raw viam-server logs
-   `videoname_timestamp.analysis.txt` - Detailed performance analysis
-   `videoname_timestamp_timeline.log` - Extracted classification timeline

### **Summary Reports**

-   `evaluation_results_timestamp.json` - Complete evaluation summary
-   Cross-video performance metrics
-   Aggregate statistics and recommendations

### **Example Results Structure**

```
results/evaluation_20250611_120000/
├── video1_20250611_120001.log
├── video1_20250611_120001.analysis.txt
├── video2_20250611_120035.log
├── video2_20250611_120035.analysis.txt
└── evaluation_results_20250611_120000.json
```

## 🔄 Data Flow

```
Recording → sample_videos/ → Evaluation → results/
                ↓                ↓
            datasets/        Comparison with
         (ground truth)     ground truth data
```

### **For Recording:**

1. Use `recording/` tools to capture videos
2. Videos saved to `sample_videos/` for evaluation
3. Action logs saved to `datasets/` for ground truth

### **For Evaluation:**

1. Videos from `sample_videos/` processed automatically
2. Results compared against `datasets/ml_dataset.csv`
3. Outputs saved to `results/` with timestamps

## 🛠️ Data Management

### **Adding New Videos**

```bash
# Copy videos to sample directory
cp /path/to/new/videos/*.mp4 data/sample_videos/

# Or specify custom directory in evaluation
python3 automate_evaluation.py --video-dir /custom/path/to/videos
```

### **Updating Ground Truth**

```bash
# Update the ground truth dataset
cp new_ml_dataset.csv data/datasets/ml_dataset.csv

# Evaluation will automatically use updated ground truth
```

### **Cleaning Results**

```bash
# Remove old evaluation results (optional)
rm -rf data/results/evaluation_older_timestamp/

# Keep recent results for comparison
ls -la data/results/
```

## 📈 Integration

### **With Recording Tools**

```bash
# Record videos directly to data directory
cd recording/
OUTPUT_DIR="../data/sample_videos" python3 record_rgb_interactive.py
```

### **With Evaluation Pipeline**

```bash
# Automated evaluation of all data
cd evaluation/
python3 automate_evaluation.py \
    --video-dir ../data/sample_videos \
    --output-dir ../data/results/evaluation_$(date +%Y%m%d_%H%M%S)
```

### **With External Tools**

```python
import json
import pandas as pd

# Load evaluation results
with open('data/results/evaluation_results_timestamp.json') as f:
    results = json.load(f)

# Load ground truth
gt_data = pd.read_csv('data/datasets/ml_dataset.csv')

# Integrate with your analysis pipeline...
```

## 📋 File Formats

### **Ground Truth CSV**

```csv
video_filename,action_label,start_time_seconds,end_time_seconds,duration_seconds
video1.mp4,add-food,15.2,18.4,3.2
video1.mp4,flip,25.1,28.3,3.2
```

### **Evaluation Results JSON**

```json
{
  "timestamp": "2025-06-11T12:00:00",
  "machine_id": "de6836af-05f6-4ff4-a067-8d18ac0f6495",
  "videos": [...],
  "summary": {
    "total_detections": 25,
    "overall_acceptance_rate": 85.2,
    "avg_confidence_across_videos": 78.5
  }
}
```
