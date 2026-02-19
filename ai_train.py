import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle

# Load dataset
data = pd.read_csv("flood_dataset_india_rf.csv")

# Encode state column
data["state_code"] = data["state"].astype("category").cat.codes
data = data.drop("state", axis=1)

# Split features & target
X = data.drop("affected", axis=1)
y = data["affected"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest Model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
score = r2_score(y_test, pred)

# Save model
pickle.dump(model, open("flood_model.pkl", "wb"))

print("✅ Random Forest model trained successfully")
print(f"📊 R² Score: {score:.2f}")