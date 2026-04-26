import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

DATA_PATH = os.path.join("data", "gestures.csv")
MODEL_PATH = os.path.join("models", "gesture_model.pkl")
EXPECTED_COLUMNS = 64

os.makedirs("models", exist_ok=True)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Training data not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, header=None)
df = df.dropna()

if df.empty:
    raise ValueError(f"No usable rows found in {DATA_PATH}")

if df.shape[1] != EXPECTED_COLUMNS:
    raise ValueError(
        f"Expected {EXPECTED_COLUMNS} columns per sample "
        f"(label + 21 hand landmarks * 3), got {df.shape[1]}"
    )

X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values

class_counts = pd.Series(y).value_counts()
if len(class_counts) < 2:
    raise ValueError("At least two gesture classes are required for training")

if class_counts.min() < 2:
    low_sample_classes = ", ".join(class_counts[class_counts < 2].index.astype(str))
    raise ValueError(f"Need at least 2 samples per gesture. Too few samples for: {low_sample_classes}")

le = LabelEncoder()
y_enc = le.fit_transform(y)

n_classes = len(le.classes_)
test_count = max(n_classes, int(np.ceil(len(df) * 0.2)))
test_count = min(test_count, len(df) - n_classes)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_enc,
    test_size=test_count,
    random_state=42,
    stratify=y_enc,
)

model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

acc = model.score(X_test, y_test) * 100
print(f"\nAccuracy: {acc:.1f}%")
print("\nDetailed report:")
labels = np.arange(n_classes)
print(classification_report(
    y_test,
    model.predict(X_test),
    labels=labels,
    target_names=le.classes_,
    zero_division=0,
))

with open(MODEL_PATH, "wb") as f:
    pickle.dump((model, le), f)

print(f"\nModel saved to {MODEL_PATH}")
print("Gestures trained:", list(le.classes_))
