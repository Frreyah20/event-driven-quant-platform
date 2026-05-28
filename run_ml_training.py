import pandas as pd
from ml_model import train_ml_model

# ---------------------------------------------------
# Load dataset
# ---------------------------------------------------
data = pd.read_csv("data/AAPL_data.csv")

# ---------------------------------------------------
# Train ML model
# ---------------------------------------------------
model = train_ml_model(data)