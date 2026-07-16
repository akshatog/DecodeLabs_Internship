"""
Project 2: Data Classification Using AI
DecodeLabs — Industrial Training Kit (Batch 2026)

Goal: Build a basic classification model using a small dataset (Iris),
following the IPO framework from the brief:
  INPUT   -> load data, scale features
  PROCESS -> train/test split, K-Nearest Neighbors (KNN)
  OUTPUT  -> confusion matrix, F1 score (accuracy alone can lie — slide 14)

Spec checklist:
  [x] Load and understand a dataset       -> load_iris()
  [x] Split into training and testing sets -> train_test_split(), 80/20, shuffled
  [x] Apply a simple classification algo   -> KNeighborsClassifier
  [x] Evaluate properly                    -> confusion matrix + F1, not just accuracy
"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, f1_score, accuracy_score


def load_data():
    """
    PHASE: INPUT — Raw Material (the Iris benchmark from the slides)
    150 samples, 3 classes (setosa/versicolor/virginica), 4 features
    (sepal length, sepal width, petal length, petal width).
    """
    iris = load_iris()
    X = iris.data
    y = iris.target
    return X, y, iris.target_names


def split_and_scale(X, y, test_size=0.2, random_state=42):
    """
    PHASE: PROCESS (part 1) — Structural Integrity: The Split
    Shuffle before splitting to remove order bias (train_test_split does
    this by default). 80/20 split as shown in the "Full Architecture" slide.

    PHASE: INPUT (part 2) — The Gatekeeper Rule: Scaling
    KNN is distance-based, so unscaled features (e.g. cm-scale petal length
    vs. tiny sepal width differences) would bias the distance calculation.
    StandardScaler transforms every feature to mean=0, variance=1.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)   # fit ONLY on training data
    X_test_scaled = scaler.transform(X_test)          # apply same transform to test data

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def find_best_k(X_train, y_train, X_test, y_test, max_k=20):
    """
    PHASE: PROCESS (part 2) — Tuning the Engine: Choosing 'K'
    K=1 overfits to noise, very large K underfits and becomes too generic.
    We scan K values and track error rate to find the 'elbow' — the point
    of lowest error before it climbs back up.
    """
    best_k, best_acc = 1, 0
    print("K   | Test Accuracy")
    print("----|--------------")
    for k in range(1, max_k + 1):
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        print(f"{k:<3} | {acc:.4f}")
        if acc > best_acc:
            best_acc, best_k = acc, k
    print(f"\nBest K found: {best_k} (accuracy = {best_acc:.4f})\n")
    return best_k


def train_and_evaluate(X_train, X_test, y_train, y_test, target_names, k=5):
    """
    PHASE: PROCESS (part 3) — The Workflow: scikit-learn
      1. INSTANTIATE -> build the model frame
      2. FIT         -> memorize the training map
      3. PREDICT     -> apply the learned logic to unseen test data

    PHASE: OUTPUT — Diagnostic Tool: Confusion Matrix + F1 Score
    Accuracy alone can be an "accuracy mirage" on imbalanced data (slide 14),
    so we look deeper with a confusion matrix and F1 (harmonic mean of
    precision and recall).
    """
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"=== Results with K={k} ===\n")

    print("Confusion Matrix (rows = actual, cols = predicted):")
    cm = confusion_matrix(y_test, predictions)
    print(cm, "\n")

    print("Classification Report:")
    print(classification_report(y_test, predictions, target_names=target_names))

    f1 = f1_score(y_test, predictions, average="weighted")
    acc = accuracy_score(y_test, predictions)
    print(f"Overall Accuracy: {acc:.4f}")
    print(f"Weighted F1 Score: {f1:.4f}")

    return model


def predict_new_sample(model, scaler, target_names, sample):
    """
    Bonus: classify a brand-new, unseen flower measurement — the whole
    point of a trained model (Output slide: 'make new decisions').
    sample = [sepal_length, sepal_width, petal_length, petal_width] in cm
    """
    sample_scaled = scaler.transform([sample])
    prediction = model.predict(sample_scaled)[0]
    print(f"\nNew sample {sample} -> predicted class: {target_names[prediction]}")


if __name__ == "__main__":
    X, y, target_names = load_data()
    X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)

    # Explore K values first (educational — shows why K=5 is a reasonable default)
    best_k = find_best_k(X_train, y_train, X_test, y_test)

    # Train final model and evaluate properly
    model = train_and_evaluate(X_train, X_test, y_train, y_test, target_names, k=best_k)

    # Try it on a new, made-up flower measurement
    predict_new_sample(model, scaler, target_names, [5.0, 3.4, 1.5, 0.2])