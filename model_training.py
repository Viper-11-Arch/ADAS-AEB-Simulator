import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv('Data_Set/risk_dataset.csv')
X = data[["throttle_change", "speed_change", "distance"]]
Y = data[["risk_flag"]]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

model = LogisticRegression()
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)
print(classification_report(Y_test, Y_pred))

sample = [[40,20,8]]
prob = model.predict_proba(sample)[0][1]
pred = int(prob >= 0.5)

print("ML Prediction:", pred)
print("ML Confidence:",prob)

#joblib.dump(model,"risk_model.pkl")
print("risk_model exported")
