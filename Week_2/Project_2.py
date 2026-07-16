"""
Project 2: Data Classification Using AI (Advanced)
DecodeLabs — Industrial Training Kit (Batch 2026)

Goal: Build a classification model (Iris), with cross-validation, 
model serialization, visualizations, and model comparison.
"""

import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report, f1_score, accuracy_score


def load_data():
    iris = load_iris()
    return iris.data, iris.target, iris.target_names


def split_and_scale(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def find_best_k_cv(X_train, y_train, max_k=20):
    """Uses GridSearchCV with 5-fold cross validation to find the best K."""
    print("Running 5-Fold Cross-Validation for KNN...")
    param_grid = {'n_neighbors': range(1, max_k + 1)}
    grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, scoring='accuracy')
    grid.fit(X_train, y_train)
    
    best_k = grid.best_params_['n_neighbors']
    print(f"Best K found via CV: {best_k} (CV Accuracy = {grid.best_score_:.4f})")
    
    # Save the Elbow Curve plot
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_k + 1), grid.cv_results_['mean_test_score'], marker='o', linestyle='dashed')
    plt.title('KNN: Cross-Validation Accuracy vs. K Value (Elbow Method)')
    plt.xlabel('Number of Neighbors (K)')
    plt.ylabel('CV Mean Accuracy')
    plt.grid(True)
    plt.savefig('elbow_curve.png')
    plt.close()
    print("-> Saved 'elbow_curve.png'")
    
    return best_k


def train_and_evaluate_knn(X_train, X_test, y_train, y_test, target_names, k):
    print(f"\n--- Training Final KNN Model (K={k}) ---")
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")
    print(f"KNN Accuracy: {acc:.4f} | Weighted F1: {f1:.4f}")
    
    # Save Confusion Matrix Heatmap
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
    plt.title(f'KNN Confusion Matrix (K={k})')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig('confusion_matrix.png')
    plt.close()
    print("-> Saved 'confusion_matrix.png'")
    
    return model


def train_and_evaluate_tree(X_train, X_test, y_train, y_test):
    """Compare KNN against a Decision Tree Classifier."""
    print("\n--- Training Decision Tree (Comparison) ---")
    tree = DecisionTreeClassifier(random_state=42)
    tree.fit(X_train, y_train)
    predictions = tree.predict(X_test)
    
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")
    print(f"Decision Tree Accuracy: {acc:.4f} | Weighted F1: {f1:.4f}")
    return tree


def save_artifacts(model, scaler):
    """Save the trained model and scaler to disk."""
    joblib.dump(model, 'knn_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("\n-> Saved 'knn_model.pkl' and 'scaler.pkl' to disk.")


def predict_new_sample(target_names, sample):
    """Load artifacts and predict safely with input validation."""
    if not isinstance(sample, list) or len(sample) != 4:
        raise ValueError("Invalid Input: Sample must be a list of exactly 4 numerical measurements.")
        
    try:
        model = joblib.load('knn_model.pkl')
        scaler = joblib.load('scaler.pkl')
    except FileNotFoundError:
        print("Error: Model or scaler files not found. Train them first.")
        return

    sample_scaled = scaler.transform([sample])
    prediction = model.predict(sample_scaled)[0]
    print(f"\nInference on {sample} -> Predicted Class: {target_names[prediction]}")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore") # hide minor warnings for clean output
    
    X, y, target_names = load_data()
    X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)
    
    # 1. Hyperparameter tuning with CV + Visualization
    best_k = find_best_k_cv(X_train, y_train)
    
    # 2. Train final KNN and plot confusion matrix
    knn_model = train_and_evaluate_knn(X_train, X_test, y_train, y_test, target_names, best_k)
    
    # 3. Compare with Decision Tree
    train_and_evaluate_tree(X_train, X_test, y_train, y_test)
    
    # 4. Serialize Model
    save_artifacts(knn_model, scaler)
    
    # 5. Safe Inference
    predict_new_sample(target_names, [5.0, 3.4, 1.5, 0.2])
    
    # Example of invalid input handling
    try:
        predict_new_sample(target_names, [5.0, 3.4])
    except ValueError as e:
        print(f"\nCaught Exception intentionally: {e}")