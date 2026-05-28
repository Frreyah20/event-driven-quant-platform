'''
#Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from feature_engineering import create_features
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def train_ml_model(data):
    df = create_features(data)
    feature_columns = ["returns", "ma_short", "ma_long", "volatility", "momentum"] #predictors variable
    x = df[feature_columns]
    y = df["target"]
    split_index = int(len(df) * 0.7)
    x_train = x.iloc[:split_index]
    x_test = x.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]
    model = LogisticRegression()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)
    print(f"ML Model Accuracy: {accuracy:.4%}")
    print("\nConfusion Matrix:")
    print(cm)
    plt.figure(figsize=(6,8))
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.colorbar()
    plt.show()
    return model
'''
'''
#Random Forest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from feature_engineering import create_features
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def train_ml_model(data):
    df = create_features(data)
    feature_columns = ["returns", "ma_short", "ma_long", "volatility", "momentum"] #predictors variable
    x = df[feature_columns]
    y = df["target"]
    split_index = int(len(df) * 0.7)
    x_train = x.iloc[:split_index]
    x_test = x.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]
    model = RandomForestClassifier(n_estimators=100,max_depth=5,random_state=42)
    # n_estimators = no.of trees, max_depth = complexity limit, random_state = reproducibility
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    prediction_probabilities = (model.predict_proba(x_test))
    bullish_probabilities = prediction_probabilities[:, 1]
    print("\nSample Prediction Probabilities:")
    print(bullish_probabilities[:10])
    accuracy = accuracy_score(y_test, predictions)
    feature_importances = model.feature_importances_ #returns importance score for each feature
    print("\nFeature Importances:")
    for feature, importance in zip(feature_columns, feature_importances):
        print(f"{feature}: {importance:.4%}")
    plt.figure(figsize=(10, 5))
    plt.bar(
        feature_columns,
        feature_importances
    )
    plt.title("Feature Importance")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12, 5))
    plt.plot(bullish_probabilities)
    plt.title("Bullish Prediction Probabilities")
    plt.xlabel("Time")
    plt.ylabel("Probability")
    plt.grid(True)
    plt.show()

    cm = confusion_matrix(y_test, predictions)
    print(f"ML Model Accuracy: {accuracy:.4%}")
    print("\nConfusion Matrix:")
    print(cm)
    plt.figure(figsize=(6,8))
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.colorbar()
    plt.show()
    return model
'''
#XGBoost
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from feature_engineering import create_features
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def train_ml_model(data):
    df = create_features(data)
    feature_columns = ["returns", "ma_short", "ma_long", "volatility", "momentum"] #predictors variable
    x = df[feature_columns]
    y = df["target"]
    split_index = int(len(df) * 0.7)
    x_train = x.iloc[:split_index]
    x_test = x.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]
    model = XGBClassifier(n_estimators=100,max_depth=4,learning_rate=0.05,random_state=42)
    # n_estimators = no.of trees, max_depth = complexity limit, random_state = reproducibility, learning rate = update aggressiveness
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    prediction_probabilities = (model.predict_proba(x_test))
    bullish_probabilities = prediction_probabilities[:, 1]
    print("\nSample Prediction Probabilities:")
    print(bullish_probabilities[:10])
    accuracy = accuracy_score(y_test, predictions)
    feature_importances = model.feature_importances_ #returns importance score for each feature
    print("\nFeature Importances:")
    for feature, importance in zip(feature_columns, feature_importances):
        print(f"{feature}: {importance:.4%}")
    plt.figure(figsize=(10, 5))
    plt.bar(
        feature_columns,
        feature_importances
    )
    plt.title("Feature Importance")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12, 5))
    plt.plot(bullish_probabilities)
    plt.title("Bullish Prediction Probabilities")
    plt.xlabel("Time")
    plt.ylabel("Probability")
    plt.grid(True)
    plt.show()

    cm = confusion_matrix(y_test, predictions)
    print(f"ML Model Accuracy: {accuracy:.4%}")
    print("\nConfusion Matrix:")
    print(cm)
    plt.figure(figsize=(6,8))
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.colorbar()
    plt.show()
    return model
