import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

# Load dataset
df = pd.read_csv("data/health_dataset.csv")

X = df.drop("health_score", axis=1)
y = df["health_score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline: Scaling + Regression
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print("MAE:", round(mae, 2))

# Save model
with open("ml/model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ Model trained and saved")
