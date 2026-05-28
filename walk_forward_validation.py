import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from feature_engineering import create_features

def run_walk_forward_validation(data):
    df = create_features(data)
    print(len(df))
    feature_columns = ["returns", "ma_short", "ma_long", "volatility", "momentum"]
    x = df[feature_columns]
    y = df["target"]
    train_size = 100
    test_size = 20
    accuracies = []
    for start in range(0, len(df)-train_size - test_size, test_size):
        train_end = start + train_size
        test_end = train_end + test_size
        x_train = x.iloc[start:train_end]
        y_train = y.iloc[start:train_end]
        x_test = x.iloc[train_end:test_end]
        y_test = y.iloc[train_end:test_end]
        model = RandomForestClassifier(n_estimators=100,max_depth = 5, random_state=42)
        model.fit(x_train, y_train)
        prediction = model.predict(x_test)
        accuracy = accuracy_score(y_test, prediction)
        accuracies.append(accuracy)
        print(f"\nWondow Accuracy: "
              f"{accuracy:.4f}"
        )
        average_accuracy = np.mean(accuracies)
        print(f"\nAverage Walk Forward Accuracy: "
              f"{average_accuracy:.4f}"
        )

