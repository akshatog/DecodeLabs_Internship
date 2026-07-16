# Data Classification Using AI - Project 2

Welcome to **Project 2** of the **DecodeLabs — Industrial Training Kit (Batch 2026)**.

This project introduces fundamental concepts of Machine Learning by building a basic classification model. Using the classic Iris dataset, it follows the **IPO (Input-Process-Output)** framework to train a K-Nearest Neighbors (KNN) classifier and properly evaluate its performance.

## Features Checklist

As per the project specification, the following requirements are met:

- **[x] Load Dataset:** Uses `scikit-learn` to load and understand the Iris dataset (150 samples, 4 features, 3 classes).
- **[x] Train/Test Split:** Splits the data into training (80%) and testing (20%) sets with shuffling and stratification to ensure reliable evaluation.
- **[x] Apply Classification Algorithm:** Implements the K-Nearest Neighbors (KNN) algorithm and dynamically finds the best `K` value.
- **[x] Evaluate Properly:** Moves beyond simple accuracy by utilizing a Confusion Matrix, Classification Report, and F1 Score to properly diagnose model performance without falling for the "accuracy mirage".

## How It Works (IPO Framework)

1. **INPUT Phase:**
   - **Data Loading:** The Iris dataset is loaded (`load_iris()`).
   - **Scaling (The Gatekeeper):** Features are standardized using `StandardScaler` so that features with larger numeric ranges (like petal length) don't unfairly bias the distance-based KNN algorithm.

2. **PROCESS Phase:**
   - **Splitting:** The dataset is split into an 80/20 train-test ratio.
   - **Tuning the Engine:** The script explores different values for `K` (number of neighbors) to find the optimal point where the model neither overfits nor underfits.
   - **Workflow:** The model frame is instantiated, fit (trained) to memorize the map, and then applied to predict on unseen test data.

3. **OUTPUT Phase:**
   - **Diagnostics:** The predictions are evaluated using a Confusion Matrix (actual vs. predicted) and a weighted F1 Score to provide a holistic and accurate view of model performance.
   - **Inference:** The trained model is then used to classify a completely new, hypothetical flower measurement, demonstrating its practical capability to make new decisions.

## Prerequisites

Make sure you have Python installed along with the `scikit-learn` package. You can install the required dependency via pip:

```bash
pip install scikit-learn
```

## How to Run

Execute the script from your terminal:

```bash
python Project_2.py
```
