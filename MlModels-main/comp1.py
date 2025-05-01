import pandas as pd 
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, classification_report 
)
from sklearn.linear_model import LogisticRegression 
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.svm import SVC 
from sklearn.neighbors import KNeighborsClassifier

# Load your dataset
df = pd.read_csv("water_quality_data.csv")  # Replace with your path


# Feature and target selection
X = df[['Temperature', 'pH', 'TDS', 'Turbidity']] 
y = df['Bacterial_Contamination']  # Replace with your actual label column if needed

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)


# Scale features
scaler = StandardScaler() 
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test)

# Define models
models = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True),
    "Gradient Boosting": GradientBoostingClassifier()
}

# To store results
metrics = [] 
conf_matrices = {}

# Train and evaluate models
for name, model in models.items():
    print(f"\n🔍 Training {name}...")
    model.fit(X_train_scaled, y_train) 
    y_pred = model.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label=1)
    rec = recall_score(y_test, y_pred, pos_label=1)
    f1 = f1_score(y_test, y_pred, pos_label=1)

    cm = confusion_matrix(y_test, y_pred)
    conf_matrices[name] = cm

    print(f"✅ Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1 Score: {f1:.4f}")
    print(classification_report(y_test, y_pred))

    metrics.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1 Score": f1
    })

# Show performance summary
metrics_df = pd.DataFrame(metrics).sort_values(by="Accuracy", ascending=False) 
print("\n📊 Summary of Models:") 
print(metrics_df)



# Plot confusion matrices
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10)) 
axes = axes.flatten()

class_labels = np.unique(y)

for i, (model_name, cm) in enumerate(conf_matrices.items()):
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i], cbar=False,
                xticklabels=class_labels, yticklabels=class_labels)
    axes[i].set_title(f"{model_name}") 
    axes[i].set_xlabel("Predicted Labels") 
    axes[i].set_ylabel("True Labels")

    # Merge all confusion matrices
merged_cm = np.zeros_like(next(iter(conf_matrices.values())))

for cm in conf_matrices.values():
    merged_cm += cm

# Plot the merged confusion matrix
plt.figure(figsize=(6, 5))
sns.heatmap(merged_cm, annot=True, fmt='d', cmap='Oranges',
            xticklabels=class_labels, yticklabels=class_labels)
plt.title("🧪 Merged Confusion Matrix (All Models Combined)")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.tight_layout()
plt.show()


# Hide unused subplots if any
if len(models) < len(axes): 
    for j in range(len(models), len(axes)): 
        fig.delaxes(axes[j])

plt.tight_layout() 
plt.suptitle("📉 Confusion Matrices for All Models", fontsize=16, y=1.5) 