import pandas as pd
from walk_forward_validation import run_walk_forward_validation

data = pd.read_csv("data/AAPL_data.csv")
run_walk_forward_validation(data)