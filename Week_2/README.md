# Data Classification Using AI - Project 2 (Advanced)

Welcome to **Project 2** of the **DecodeLabs — Industrial Training Kit (Batch 2026)**.

This project introduces foundational Machine Learning classification concepts. It builds upon the basic KNN classifier by integrating industry-standard practices including Cross-Validation, Model Serialization, Data Visualization, and Model Comparison.

## Features Checklist

- **[x] Cross-Validation:** Replaced a simple test set evaluation with `GridSearchCV` (5-Fold Cross-Validation) to rigorously find the optimal `K` value, preventing overfitting.
- **[x] Visualizations:** Uses `matplotlib` and `seaborn` to automatically generate and save two analytical plots:
  - `elbow_curve.png`: Shows how CV accuracy varies with `K`.
  - `confusion_matrix.png`: A beautiful heatmap of the final model's predictions vs. actuals.
- **[x] Algorithm Comparison:** Trains a `DecisionTreeClassifier` alongside KNN to demonstrate model comparison on the exact same dataset.
- **[x] Model Serialization:** Utilizes `joblib` to save the trained KNN model and `StandardScaler` to disk (`.pkl` files), simulating a production-ready model pipeline.
- **[x] Safe Inference:** Adds input validation (`try-except` blocks, length checking) to ensure new data samples contain exactly the right number of features before attempting predictions.

## Prerequisites

Make sure you have Python installed, along with the required scientific packages. Install them via pip:

```bash
pip install scikit-learn matplotlib seaborn joblib
```

## How to Run

Execute the script from your terminal:

```bash
python Project_2.py
```

After running, check your `Week_2` folder for the newly generated `.png` plot images and `.pkl` model files!
